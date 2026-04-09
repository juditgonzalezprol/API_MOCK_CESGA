# 🧬 CESGA Real Script Examples & Validation Guide

## Understanding CESGA/Slurm Script Submission

CESGA Finis Terrae II/III uses **Slurm** (Simple Linux Utility for Resource Management) for job management.
Users submit **batch scripts** (not just FASTA sequences) with computational directives.

---

## 📋 Realistic Script Structure

### Basic Slurm Batch Script Header

```bash
#!/bin/bash
#SBATCH --job-name=protein_fold           # Job identifier
#SBATCH --ntasks=1                        # Number of parallel tasks
#SBATCH --cpus-per-task=8                 # CPUs per task
#SBATCH --mem=32G                         # Memory (32GB)
#SBATCH --time=01:00:00                   # Time limit (HH:MM:SS)
#SBATCH --partition=gpu                   # Queue/Partition (gpu, cpu, mem)
#SBATCH --gres=gpu:1                      # GPUs requested (1 GPU)
#SBATCH --output=%j.out                   # Output file (job ID)
#SBATCH --error=%j.err                    # Error file
#SBATCH --mail-type=END                   # Email notifications
#SBATCH --mail-user=user@example.com
```

### What These Parameters Mean

| Parameter | Example | Purpose | Validation |
|-----------|---------|---------|-----------|
| `--job-name` | `protein_fold` | Job identifier | Max 128 chars, alphanumeric+underscore |
| `--ntasks` | `1` | Parallel tasks | 1-128, integer |
| `--cpus-per-task` | `8` | CPUs per task | 1-128, integer, max available |
| `--mem` | `32G` | Total RAM | Numeric + unit (G/M/K), sensible max |
| `--time` | `01:00:00` | Compute time | Format HH:MM:SS, max 24h typically |
| `--partition` | `gpu` | Queue | Valid: gpu, cpu, mem, etc. |
| `--gres=gpu` | `1` | GPUs | 0-4 typically, integer |

---

## 🧬 Example 1: AlphaFold2 Protein Prediction

**Realistic CESGA job for protein structure prediction:**

```bash
#!/bin/bash
#SBATCH --job-name=alphafold2_ubiquitin
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=02:00:00
#SBATCH --partition=gpu
#SBATCH --gres=gpu:1
#SBATCH --output=alphafold2_%j.out
#SBATCH --error=alphafold2_%j.err

# Load necessary modules
module load CESGA/2023
module load python/3.10
module load cuda/11.8
module load cudnn/8.6

# Activate Python environment
source /home/user/alphafold2_env/bin/activate

# Set directories
INPUT_DIR="/home/user/structures/input"
OUTPUT_DIR="/home/user/structures/output"
DB_DIR="/gpfs/projects/csd111/databases/alphafold2"

# Input FASTA file (embedded or referenced)
cat > protein.fasta << EOF
>sp|P0CG47|UBC_HUMAN
MQIFVKTLTGKTITLEVESPDTIE NVALVENAKAKTLVKILSQDPE AGSFSQ
RNETAVKQVKVKALPDAQFEVV HSLAKWKRQTLGQHDFSAGEGL
YTHMKALRPDEDRLSPLHSVYVDQWDWERVMGDGERQFSTLKSTVEAIWAGIKAP
EOF

# Run AlphaFold2
python -m alphafold2 \
  --input_fasta=${INPUT_DIR}/protein.fasta \
  --output_dir=${OUTPUT_DIR} \
  --db_preset=full_dbs \
  --max_template_date=2023-12-01 \
  --num_multimer_predictions_per_model=5

# Convert output to standard format
if [ $? -eq 0 ]; then
    echo "AlphaFold2 completed successfully"
    # Post-processing here
else
    echo "AlphaFold2 failed" >&2
    exit 1
fi
```

**Validation Rules**:
- ✅ Must have `#!/bin/bash` header
- ✅ All `#SBATCH` directives must be before commands
- ✅ Must reference valid modules
- ✅ Protein data must be FASTA format
- ✅ Output paths must apply

---

## 🔬 Example 2: BLAST Sequence Similarity Search

**CESGA job for protein homology search:**

```bash
#!/bin/bash
#SBATCH --job-name=blast_search_proteins
#SBATCH --ntasks=4
#SBATCH --cpus-per-task=2
#SBATCH --mem=16G
#SBATCH --time=01:30:00
#SBATCH --partition=cpu
#SBATCH --output=blast_%j.out

# Load modules
module load CESGA/2023
module load blast/2.14.0

# Setup
QUERY="/home/user/queries/proteins.fasta"
DB="/databases/nr"
OUTPUT="/home/user/results/blast_results.txt"

# Run BLAST search (parallel across 4 CPUs)
blastp \
  -query ${QUERY} \
  -db ${DB} \
  -num_threads 4 \
  -evalue 1e-10 \
  -outfmt "6 qseqid sseqid pident length mismatch gapopen" \
  -out ${OUTPUT}

# Generate report
echo "Processed $(grep -c '^' ${QUERY}) sequences"
echo "Found $(wc -l < ${OUTPUT}) matches"
```

**Validation**:
- ✅ Multi-threaded configuration must match CPU request
- ✅ Database must exist on filesystem
- ✅ Output format must be valid
- ✅ Time estimate reasonable for task

---

## 🧪 Example 3: Molecular Dynamics Simulation

**GROMACS MD simulation (realistic CESGA job):**

```bash
#!/bin/bash
#SBATCH --job-name=gromacs_md_lysozyme
#SBATCH --ntasks=4
#SBATCH --cpus-per-task=2
#SBATCH --mem=64G
#SBATCH --time=04:00:00
#SBATCH --partition=gpu
#SBATCH --gres=gpu:2
#SBATCH --output=gromacs_%j.out

# Environment setup
module load CESGA/2023
module load gromacs/2023.1
module load cuda/11.8

# Preparation
WORK_DIR="/home/user/md_simulations/lysozyme"
cd ${WORK_DIR}

# Preprocessing
gmx pdb2gmx -f protein.pdb -o protein.gro -p topol.top -ff amber99sb-ildn -water tip3p << EOF
1
1
EOF

# Energy minimization
gmx grompp -f minim.mdp -c protein.gro -p topol.top -o em.tpr
gmx mdrun -deffnm em -gpu_ids 0 -nb gpu -pme gpu

# NVT equilibration (100 ps)
gmx grompp -f nvt.mdp -c em.gro -r em.gro -p topol.top -o nvt.tpr
gmx mdrun -deffnm nvt -gpu_ids 0 -nb gpu -pme gpu

# NPT equilibration (100 ps)
gmx grompp -f npt.mdp -c nvt.gro -r nvt.gro -t nvt.cpt -p topol.top -o npt.tpr
gmx mdrun -deffnm npt -gpu_ids 1 -nb gpu -pme gpu

# Production run (10 ns)
gmx grompp -f md.mdp -c npt.gro -t npt.cpt -p topol.top -o md.tpr
gmx mdrun -deffnm md -gpu_ids 0,1 -nb gpu -pme gpu -ntomp 2

# Analysis
gmx rms -f md.xtc -s md.tpr -o rmsd.xvg
echo "MD simulation completed on $(date)" >> log.txt
```

**Validation**:
- ✅ GPU count matches `-gpu_ids` specification
- ✅ Input files (*.pdb, *.mdp) must be referenced
- ✅ Memory estimate appropriate for system size
- ✅ Module dependencies declared

---

## 📊 Example 4: Bioinformatics Pipeline (Multi-tool)

**Complex workflow with multiple tools:**

```bash
#!/bin/bash
#SBATCH --job-name=protein_analysis_pipeline
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=16
#SBATCH --mem=64G
#SBATCH --time=03:00:00
#SBATCH --partition=gpu
#SBATCH --gres=gpu:2
#SBATCH --output=pipeline_%j.out

set -e  # Exit on any error

module load CESGA/2023
module load python/3.11
module load hmmer/3.3.2
module load blast/2.14.0

# Setup
PROTEIN_DIR="/data/proteins"
WORK_DIR="/home/user/analysis_$$"
OUTPUT_DIR="/home/user/results"

mkdir -p ${WORK_DIR}
cd ${WORK_DIR}

echo "=== Starting Protein Analysis Pipeline ==="
echo "Input: ${PROTEIN_DIR}"
echo "Timestamp: $(date)"

# Step 1: BLAST homology search
echo "Step 1: Running BLAST search..."
blastp -query ${PROTEIN_DIR}/query.fasta \
       -db /databases/swissprot \
       -num_threads 16 \
       -evalue 1e-5 \
       -outfmt 6 \
       -out homology.txt

# Step 2: Domain identification (HMM-based)
echo "Step 2: Domain identification using Pfam..."
hmmscan --cpu 16 \
        -o domains.out \
        /databases/Pfam-A.hmm \
        ${PROTEIN_DIR}/query.fasta

# Step 3: Secondary structure prediction
echo "Step 3: Predicting secondary structure..."
python << 'PYTHON_SCRIPT'
#!/usr/bin/env python3
import sys
import subprocess

# Call PSIPRED or similar
result = subprocess.run(
    ["psipred", "query.fasta"],
    capture_output=True,
    text=True
)

with open("structure.ss", "w") as f:
    f.write(result.stdout)

print(f"Secondary structure prediction complete")
PYTHON_SCRIPT

# Step 4: AlphaFold2 structure prediction
echo "Step 4: Running AlphaFold2 structure prediction..."
python -c "import alphafold; alphafold.predict('query.fasta', 'structures/')"

# Step 5: Generate summary report
echo "Step 5: Generating summary report..."
cat > summary_report.txt << EOF
Protein Analysis Report
Generated: $(date)
Query file: $(basename ${PROTEIN_DIR}/query.fasta)

Results:
- BLAST homology matches: $(wc -l < homology.txt)
- Pfam domains found: $(grep -c "^" domains.out)
- Structures predicted: $(ls structures/ | wc -l)
EOF

# Archive results
cp summary_report.txt ${OUTPUT_DIR}/
cp homology.txt ${OUTPUT_DIR}/
cp domains.out ${OUTPUT_DIR}/

echo "=== Pipeline completed successfully ==="
echo "Output directory: ${OUTPUT_DIR}"

# Cleanup
rm -rf ${WORK_DIR}
```

**Validation**:
- ✅ Input files accessible
- ✅ All modules available
- ✅ CPU count matches `cpus-per-task` and tool specifications
- ✅ Proper error handling (`set -e`)
- ✅ Database paths valid

---

## ✅ What Makes a Script "Valid" for CESGA

### Mandatory Rules
1. **Shebang**: Must start with `#!/bin/bash`
2. **SBATCH before code**: All `#SBATCH` directives before command
3. **Resource bounds**: CPU, memory, time must be reasonable
4. **Module declarations**: Required modules must be declared
5. **File paths**: Use absolute or relative paths correctly

### Recommended Practices
1. **Error handling**: Use `set -e` or check return codes
2. **Logging**: Include `echo` statements with timestamps
3. **Comments**: Explain each section
4. **Cleanup**: Remove temporary files
5. **Exit codes**: Proper error reporting

---

## 📝 Real Validation Rules for API

The API should validate:

```python
def validate_cesga_script(script_content: str) -> Tuple[bool, List[str]]:
    """Validate CESGA Slurm batch script"""
    
    errors = []
    warnings = []
    
    # Check 1: Must start with shebang
    if not script_content.strip().startswith("#!/bin/bash"):
        errors.append("Script must start with #!/bin/bash")
    
    # Check 2: SBATCH directives must come before commands
    lines = script_content.split('\n')
    seen_command = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("#SBATCH"):
            if seen_command:
                errors.append("SBATCH directives must appear before any commands")
                break
        elif stripped and not stripped.startswith("#"):
            seen_command = True
    
    # Check 3: CPU/memory/time ratios sensible
    if "--cpus-per-task=128" in script_content and "--mem=1G" in script_content:
        warnings.append("Unusual: 128 CPUs but only 1GB memory - may be misconfigured")
    
    # Check 4: GPU requests meaningful
    if "--gres=gpu:8" in script_content and "--partition=cpu" in script_content:
        errors.append("GPU requested but CPU partition specified")
    
    # Check 5: Time limit reasonable
    import re
    time_match = re.search(r'--time=(\d{2}):(\d{2}):(\d{2})', script_content)
    if time_match:
        hours = int(time_match.group(1))
        if hours > 24:
            errors.append("Maximum job time is 24 hours")
    
    # Check 6: References to non-existent modules  (optional - warning only)
    modules = re.findall(r'module load (.+)', script_content)
    valid_modules = ["python", "gcc", "cuda", "blast", "gromacs", "alphafold"]
    for mod in modules:
        if not any(v in mod.lower() for v in valid_modules):
            warnings.append(f"Module '{mod}' may not be available - verify with CESGA")
    
    return (len(errors) == 0, errors, warnings)
```

---

## 🔧 Updated API Endpoint

The API should accept **either**:

1. **FASTA sequences** (existing):
   ```json
   {
     "fasta_sequence": ">protein\nMKVLS...",
     "fasta_filename": "protein.fasta"
   }
   ```

2. **Slurm batch scripts** (NEW):
   ```json
   {
     "slurm_script": "#!/bin/bash\n#SBATCH...\nblastp...",
     "script_filename": "blast_job.sh",
     "script_type": "blast|alphafold|gromacs|custom"
   }
   ```

---

## 💾 Example: API Submission of Real Script

```bash
# Submit a BLAST script
curl -X POST http://localhost:8000/jobs/submit \
  -H "Content-Type: application/json" \
  -d '{
    "script_type": "blast",
    "slurm_script": "#!/bin/bash\n#SBATCH --job-name=blast_search\n#SBATCH --cpus-per-task=8\n#SBATCH --mem=16G\nblastp -query query.fasta -db nr -num_threads 8 -out results.txt",
    "gpus": 0,
    "cpus": 8,
    "memory_gb": 16,
    "max_runtime_seconds": 3600
  }'

# Response:
{
  "job_id": "job_blast_001",
  "status": "PENDING",
  "validation": {
    "valid": true,
    "warnings": []
  }
}
```

---

## 📚 Real CESGA Script Categories

### Category 1: Structure Prediction
- AlphaFold2
- RoseTTAFold
- OmegaFold

### Category 2: Sequence Analysis
- BLAST/PSI-BLAST
- HMMER (Pfam, InterPro)
- Multiple sequence alignment (MUSCLE, MAFFT)

### Category 3: Molecular Dynamics
- GROMACS
- AMBER
- NAMD

### Category 4: Genomics
- BWA/Bowtie (alignment)
- SAMtools (processing)
- GATK (variant calling)

### Category 5: Bioinformatics Tools
- VMD (visualization)
- RELION (cryo-EM)
- Rosetta Commons

---

## 🎯 Summary: What the API Should Do

✅ **Accept FASTA inputs** (current - proteins)  
✅ **Accept Slurm scripts** (NEW - real HPC jobs)  
✅ **Validate script syntax** (NEW - check correctness)  
✅ **Check resource requests** (NEW - reasonable bounds)  
✅ **Verify SBATCH directives** (NEW - proper format)  
✅ **NOT execute** (just store and validate)  
✅ **Return validation results** (errors/warnings)  
✅ **Simulate job lifecycle** (PENDING→RUNNING→COMPLETED)

---

**Next Steps**:
1. Update API to accept `slurm_script` parameter
2. Implement validation function
3. Store scripts with job metadata
4. Return validation results

This way, hackathon participants can submit realistic CESGA scripts which get validated but don't actually execute! ✨
