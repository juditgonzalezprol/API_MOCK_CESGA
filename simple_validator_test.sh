#!/bin/bash

# Simple test to validate CESGA scripts with the validator

PROJECT_ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

echo "=================================="
echo "CESGA Script Validator Test"
echo "=================================="
echo ""

# Test 1: AlphaFold2
echo "Test 1: AlphaFold2 Script"
echo "———————————————————————————"

SCRIPT1=$(cat << 'EOF'
#!/bin/bash
#SBATCH --job-name=alphafold2_prediction
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=02:00:00
#SBATCH --partition=gpu
#SBATCH --gres=gpu:1

module load CESGA/2023
module load python/3.10
module load cuda/11.8

python -m alphafold2 --input_fasta=input.fasta

echo "AlphaFold2 completed"
EOF
)

python3 << 'PYTHON'
import sys
sys.path.insert(0, '$PROJECT_ROOT/app/services')

from cesga_script_validator import CESGAScriptValidator, ScriptType

validator = CESGAScriptValidator()
result = validator.validate("""$SCRIPT1""", ScriptType.ALPHAFOLD)

print(f"✓ Valid: {result.is_valid}")
if result.resource_estimate:
    re = result.resource_estimate
    print(f"  CPUs: {re.get('cpus', 0)}, GPUs: {re.get('gpus', 0)}, Memory: {re.get('memory_gb', 0)}GB")
if result.errors:
    print(f"✗ Errors: {result.errors}")
if result.warnings:
    print(f"⚠ Warnings: {result.warnings}")
PYTHON

echo ""

# Test 2: BLAST
echo "Test 2: BLAST Script"
echo "———————————————————————————"

SCRIPT2=$(cat << 'EOF'
#!/bin/bash
#SBATCH --job-name=blast_search
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=16
#SBATCH --mem=32G
#SBATCH --time=01:30:00
#SBATCH --partition=cpu

module load CESGA/2023
module load blast/2.14.0

blastp -query input.fasta -db /databases/swissprot -num_threads 16

echo "BLAST completed"
EOF
)

python3 << 'PYTHON'
import sys
sys.path.insert(0, '$PROJECT_ROOT/app/services')

from cesga_script_validator import CESGAScriptValidator, ScriptType

validator = CESGAScriptValidator()
result = validator.validate("""$SCRIPT2""", ScriptType.BLAST)

print(f"✓ Valid: {result.is_valid}")
if result.resource_estimate:
    re = result.resource_estimate
    print(f"  CPUs: {re.get('cpus', 0)}, GPUs: {re.get('gpus', 0)}, Memory: {re.get('memory_gb', 0)}GB")
if result.errors:
    print(f"✗ Errors: {result.errors}")
PYTHON

echo ""

# Test 3: GROMACS with GPU
echo "Test 3: GROMACS Script"
echo "———————————————————————————"

SCRIPT3=$(cat << 'EOF'
#!/bin/bash
#SBATCH --job-name=md_simulation
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH --time=04:00:00
#SBATCH --partition=gpu
#SBATCH --gres=gpu:2

module load CESGA/2023
module load gromacs/2023.1
module load cuda/11.8

gmx mdrun -deffnm simulation

echo "MD simulation completed"
EOF
)

python3 << 'PYTHON'
import sys
sys.path.insert(0, '$PROJECT_ROOT/app/services')

from cesga_script_validator import CESGAScriptValidator, ScriptType

validator = CESGAScriptValidator()
result = validator.validate("""$SCRIPT3""", ScriptType.GROMACS)

print(f"✓ Valid: {result.is_valid}")
if result.resource_estimate:
    re = result.resource_estimate
    print(f"  CPUs: {re.get('cpus', 0)}, GPUs: {re.get('gpus', 0)}, Memory: {re.get('memory_gb', 0)}GB")
if result.errors:
    print(f"✗ Errors: {result.errors}")
PYTHON

echo ""
echo "=================================="
echo "✓ All scripts validated"
echo "=================================="
