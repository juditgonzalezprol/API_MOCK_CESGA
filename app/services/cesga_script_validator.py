# CESGA Script Validation Service

"""
Validates realistic CESGA/Slurm scripts for proper formatting and resource allocation.
Does NOT execute - only validates syntax and correctness.
"""

import re
from typing import Tuple, List, Dict, Any
from dataclasses import dataclass
from enum import Enum


class ScriptType(str, Enum):
    """Types of bioinformatics scripts"""
    BLAST = "blast"
    ALPHAFOLD = "alphafold"
    GROMACS = "gromacs"
    HMMER = "hmmer"
    CUSTOM = "custom"
    FASTA = "fasta"  # Legacy - just proteins


@dataclass
class ValidationResult:
    """Result of script validation"""
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    script_type: ScriptType
    resource_estimate: Dict[str, Any]


class CESGAScriptValidator:
    """Validates CESGA Slurm batch scripts"""
    
    # Resource limits
    MAX_CPUS = 128
    MAX_GPUS = 4
    MAX_MEMORY_GB = 256
    MAX_TIME_HOURS = 24
    
    # Valid SBATCH parameters
    VALID_SBATCH_PARAMS = {
        '--job-name', '--ntasks', '--cpus-per-task', '--mem', '--time',
        '--partition', '--gres', '--output', '--error', '--mail-type',
        '--mail-user', '--nodes', '--tasks-per-node', '--constraint',
        '--array', '--dependency', '--nodelist', '--exclude'
    }
    
    # Valid partitions on CESGA
    VALID_PARTITIONS = {
        'cpu', 'gpu', 'mem', 'gpu-fat',  # Slurm partitions
        'alpha', 'beta', 'production'      # CESGA specific
    }
    
    # Common modules on CESGA
    KNOWN_MODULES = {
        'python', 'gcc', 'cuda', 'cudnn', 'blast', 'gromacs',
        'hmmer', 'mpi', 'openmpi', 'intel', 'pgi',  # Compilers
        'cesga', 'alphafold', 'tensorflow', 'pytorch'  # Applications
    }
    
    def __init__(self):
        self.errors: List[str] = []
        self.warnings: List[str] = []
        
    def validate(self, script_content: str, script_type: ScriptType = ScriptType.CUSTOM) -> ValidationResult:
        """Main validation entry point"""
        self.errors = []
        self.warnings = []
        
        if not script_content or not script_content.strip():
            return ValidationResult(
                is_valid=False,
                errors=["Script content is empty"],
                warnings=[],
                script_type=script_type,
                resource_estimate={}
            )
        
        # Step 1: Check shebang
        self._validate_shebang(script_content)
        
        # Step 2: Extract and validate SBATCH directives
        sbatch_directives = self._extract_sbatch_directives(script_content)
        sbatch_valid, sbatch_errors = self._validate_sbatch_directives(sbatch_directives)
        self.errors.extend(sbatch_errors)
        
        # Step 3: Validate script structure
        self._validate_sbatch_placement(script_content)
        
        # Step 4: Validate resources
        resources, resource_errors = self._validate_resources(sbatch_directives)
        self.errors.extend(resource_errors)
        
        # Step 5: Check modules
        modules = self._extract_modules(script_content)
        self._validate_modules(modules)
        
        # Step 6: Script-type specific validation
        self._validate_script_type(script_content, script_type)
        
        # Step 7: Syntax check
        self._validate_bash_syntax(script_content)
        
        return ValidationResult(
            is_valid=len(self.errors) == 0,
            errors=self.errors,
            warnings=self.warnings,
            script_type=script_type,
            resource_estimate=resources
        )
    
    def _validate_shebang(self, content: str) -> None:
        """Check script starts with proper shebang"""
        first_line = content.split('\n')[0] if content else ""
        if not first_line.startswith("#!/bin/bash"):
            self.errors.append("Script must start with #!/bin/bash shebang")
    
    def _extract_sbatch_directives(self, content: str) -> Dict[str, str]:
        """Extract all #SBATCH directives"""
        directives = {}
        for line in content.split('\n'):
            if line.strip().startswith('#SBATCH'):
                # Parse: #SBATCH --key=value or #SBATCH --key value
                match = re.match(r'#SBATCH\s+(--[\w-]+)(?:=(.+))?(?:\s+(.+))?', line)
                if match:
                    key = match.group(1)
                    value = match.group(2) or match.group(3) or ""
                    directives[key] = value.strip()
        return directives
    
    def _validate_sbatch_directives(self, directives: Dict[str, str]) -> Tuple[bool, List[str]]:
        """Validate SBATCH parameter names and formats"""
        errors = []
        
        for key, value in directives.items():
            # Check if parameter name is valid
            if key not in self.VALID_SBATCH_PARAMS:
                errors.append(f"Unknown SBATCH parameter: {key}. Valid: {', '.join(sorted(self.VALID_SBATCH_PARAMS)[:5])}...")
            
            # Validate specific parameters
            if key == '--partition' and value not in self.VALID_PARTITIONS:
                self.warnings.append(f"Partition '{value}' may not exist. Common: {', '.join(list(self.VALID_PARTITIONS)[:3])}")
            
            elif key == '--gres' and not self._validate_gres(value):
                errors.append(f"Invalid --gres format: {value}. Expected: 'gpu:N' (e.g., 'gpu:2')")
            
            elif key == '--time' and not self._validate_time_format(value):
                errors.append(f"Invalid --time format: {value}. Expected: HH:MM:SS")
            
            elif key in ('--cpus-per-task', '--ntasks', '--mem') and not value:
                errors.append(f"{key} requires a value")
        
        return (len(errors) == 0, errors)
    
    def _validate_gres(self, gres_value: str) -> bool:
        """Validate GPU resource specification"""
        # Valid formats: gpu:1, gpu:2, gpu:rtx2080:1
        match = re.match(r'gpu(?::[\w]+)?:\d+', gres_value)
        return match is not None
    
    def _validate_time_format(self, time_value: str) -> bool:
        """Validate HH:MM:SS format"""
        match = re.match(r'(\d{1,2}):(\d{2}):(\d{2})', time_value)
        if not match:
            return False
        hours, minutes, seconds = map(int, match.groups())
        return 0 <= hours <= 999 and 0 <= minutes < 60 and 0 <= seconds < 60
    
    def _validate_sbatch_placement(self, content: str) -> None:
        """Check that #SBATCH directives come before commands"""
        lines = content.split('\n')
        seen_command = False
        sbatch_count = 0
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            
            # Skip empty lines and comments (except SBATCH)
            if not stripped or (stripped.startswith('#') and not stripped.startswith('#SBATCH')):
                continue
            
            if stripped.startswith('#SBATCH'):
                if seen_command:
                    self.errors.append(f"Line {i+1}: #SBATCH directives must appear before any commands")
                sbatch_count += 1
            else:
                seen_command = True
        
        if sbatch_count == 0:
            self.warnings.append("No #SBATCH directives found - will use default resource allocation")
    
    def _validate_resources(self, directives: Dict[str, str]) -> Tuple[Dict[str, Any], List[str]]:
        """Validate resource allocations are within limits"""
        errors = []
        resources = {
            'cpus': 1,
            'gpus': 0,
            'memory_gb': 8,
            'time_hours': 1
        }
        
        # CPU validation
        if '--cpus-per-task' in directives:
            try:
                cpus = int(directives['--cpus-per-task'])
                if cpus > self.MAX_CPUS:
                    errors.append(f"CPUs requested ({cpus}) exceeds maximum ({self.MAX_CPUS})")
                elif cpus < 1:
                    errors.append("CPUs must be >= 1")
                else:
                    resources['cpus'] = cpus
            except ValueError:
                errors.append(f"Invalid CPU count: {directives['--cpus-per-task']}")
        
        # GPU validation
        if '--gres' in directives:
            match = re.search(r'gpu:(\d+)', directives['--gres'])
            if match:
                gpus = int(match.group(1))
                if gpus > self.MAX_GPUS:
                    errors.append(f"GPUs requested ({gpus}) exceeds maximum ({self.MAX_GPUS})")
                elif gpus < 0:
                    errors.append("GPUs must be >= 0")
                else:
                    resources['gpus'] = gpus
        
        # Memory validation
        if '--mem' in directives:
            mem_str = directives['--mem']
            match = re.match(r'(\d+)([KMG]?)B?', mem_str)
            if match:
                amount = int(match.group(1))
                unit = match.group(2) or 'M'
                # Convert to GB
                if unit == 'K':
                    amount_gb = amount / (1024 * 1024)
                elif unit == 'M':
                    amount_gb = amount / 1024
                elif unit == 'G':
                    amount_gb = amount
                else:
                    amount_gb = 0
                
                if amount_gb > self.MAX_MEMORY_GB:
                    errors.append(f"Memory ({amount_gb:.1f}GB) exceeds maximum ({self.MAX_MEMORY_GB}GB)")
                elif amount_gb < 0.1:
                    errors.append("Memory must be > 0.1 GB")
                else:
                    resources['memory_gb'] = amount_gb
            else:
                errors.append(f"Invalid memory format: {mem_str}. Use format: 32G, 16384M, etc.")
        
        # Time validation
        if '--time' in directives:
            time_str = directives['--time']
            match = re.match(r'(\d+):(\d+):(\d+)', time_str)
            if match:
                hours = int(match.group(1))
                if hours > self.MAX_TIME_HOURS:
                    errors.append(f"Time ({hours}h) exceeds maximum ({self.MAX_TIME_HOURS}h)")
                else:
                    resources['time_hours'] = hours
        
        # Sanity checks
        if resources['cpus'] > 64 and resources['memory_gb'] < 32:
            self.warnings.append(f"High CPU count ({resources['cpus']}) but low memory ({resources['memory_gb']}GB) - may be unbalanced")
        
        if resources['gpus'] > 0 and resources['cpus'] < 4:
            self.warnings.append(f"GPUs requested but few CPUs ({resources['cpus']}) - consider requesting 8+ CPUs")
        
        return resources, errors
    
    def _extract_modules(self, content: str) -> List[str]:
        """Extract module names from 'module load' statements"""
        modules = []
        for line in content.split('\n'):
            match = re.search(r'module\s+load\s+(.+)', line)
            if match:
                module_name = match.group(1).strip()
                modules.append(module_name)
        return modules
    
    def _validate_modules(self, modules: List[str]) -> None:
        """Warn about unknown modules"""
        for mod in modules:
            # Extract base name (e.g., "python/3.10" -> "python")
            base_mod = mod.split('/')[0].lower()
            if not any(known in base_mod for known in self.KNOWN_MODULES):
                self.warnings.append(f"Module '{mod}' - verify availability with CESGA")
    
    def _validate_script_type(self, content: str, script_type: ScriptType) -> None:
        """Type-specific validation"""
        if script_type == ScriptType.ALPHAFOLD:
            if 'alphafold' not in content.lower():
                self.warnings.append("Script type is AlphaFold but 'alphafold' not found in content")
        
        elif script_type == ScriptType.BLAST:
            if 'blastp' not in content and 'blastn' not in content:
                self.warnings.append("Script type is BLAST but no blastp/blastn commands found")
        
        elif script_type == ScriptType.GROMACS:
            if 'gmx' not in content and 'gromacs' not in content.lower():
                self.warnings.append("Script type is GROMACS but GMX commands not found")
        
        elif script_type == ScriptType.HMMER:
            if 'hmmer' not in content.lower() and 'hmmscan' not in content:
                self.warnings.append("Script type is HMMER but hmmer commands not found")
    
    def _validate_bash_syntax(self, content: str) -> None:
        """Basic bash syntax validation"""
        # Check for unclosed quotes
        for quote_char in ['"', "'"]:
            count = 0
            for char in content:
                if char == quote_char and (content.index(char) == 0 or content[content.index(char)-1] != '\\'):
                    count += 1
            if count % 2 != 0:
                self.warnings.append(f"Possible unclosed {quote_char} quote")
        
        # Check for unclosed parentheses
        open_parens = content.count('(') - content.count('\\(')
        close_parens = content.count(')') - content.count('\\)')
        if open_parens != close_parens:
            self.warnings.append("Mismatched parentheses")
        
        # Check for common mistakes
        if re.search(r'#!\s+/bin/bash', content):
            self.warnings.append("Shebang has space after #! - should be #!/bin/bash")


# Utility functions for API
def validate_cesga_script(script: str, script_type: str = "custom") -> ValidationResult:
    """Validate a CESGA script (API helper)"""
    try:
        script_type_enum = ScriptType[script_type.upper()]
    except KeyError:
        script_type_enum = ScriptType.CUSTOM
    
    validator = CESGAScriptValidator()
    return validator.validate(script, script_type_enum)


if __name__ == "__main__":
    # Example usage
    
    # Test script
    test_script = """#!/bin/bash
#SBATCH --job-name=test_alphafold
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=02:00:00
#SBATCH --partition=gpu
#SBATCH --gres=gpu:1

module load CESGA/2023
module load python/3.10
module load cuda/11.8

python -m alphafold2 --input_fasta=protein.fasta --output_dir=/output
"""
    
    result = validate_cesga_script(test_script, "alphafold")
    print(f"Valid: {result.is_valid}")
    print(f"Errors: {result.errors}")
    print(f"Warnings: {result.warnings}")
    print(f"Resources: {result.resource_estimate}")
