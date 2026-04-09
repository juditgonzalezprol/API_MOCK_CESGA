# CESGA API Script Submission Guide

## Quick Start: Ready-to-Use Scripts

You now have **6 complete, production-ready CESGA scripts** that can be submitted directly to the API. These scripts are:

- ✅ **Realistic** - Match actual CESGA Finis Terrae II/III usage patterns
- ✅ **Validated** - Pass all CESGA resource constraints
- ✅ **Non-executed** - Validated for correctness, not actually run
- ✅ **Well-documented** - Include proper error handling and logging

---

## Available Script Examples

### 1. **AlphaFold2 Protein Structure Prediction**
**File**: `scripts/cesga_script_examples.sh` → `EXAMPLE_1_ALPHAFOLD2`

**What it does**:
- Predicts 3D protein structure from amino acid sequence
- Uses GPU acceleration (1 GPU)
- Allocates 8 CPU cores for parallelization
- Generates structure files (PDB format)

**Resources**:
```
CPUs: 8
GPUs: 1
Memory: 32GB
Time: 2 hours
Partition: gpu
```

**Modules**: `CESGA/2023`, `python/3.10`, `cuda/11.8`, `cudnn/8.6`

---

### 2. **BLAST Homology Search**
**File**: `scripts/cesga_script_examples.sh` → `EXAMPLE_2_BLAST_SEARCH`

**What it does**:
- Searches unknown protein against UniProt/SwissProt database
- Uses PSI-BLAST for iterative refinement
- Finds sequence homologs with statistical significance
- Generates multiple output formats (tabular, HTML)

**Resources**:
```
CPUs: 16
GPUs: 0
Memory: 32GB
Time: 1.5 hours
Partition: cpu
```

**Modules**: `CESGA/2023`, `blast/2.14.0`

---

### 3. **Multiple Sequence Alignment (MAFFT)**
**File**: `scripts/cesga_script_examples.sh` → `EXAMPLE_3_MSA`

**What it does**:
- Aligns multiple protein sequences
- Converts output to multiple formats (Fasta, Stockholm, Phylip)
- Suitable for phylogenetic analysis
- Fast auto algorithm selection

**Resources**:
```
CPUs: 12
GPUs: 0
Memory: 16GB
Time: 1 hour
Partition: cpu
```

**Modules**: `CESGA/2023`, `mafft/7.515`

---

### 4. **Molecular Dynamics - GROMACS**
**File**: `scripts/cesga_script_examples.sh` → `EXAMPLE_4_MD_GROMACS`

**What it does**:
- Runs molecular dynamics simulation
- 4-step protocol: Energy minimization → NVT → NPT → Production
- GPU acceleration (2 GPUs recommended)
- Generates trajectory and analysis

**Resources**:
```
CPUs: 8
GPUs: 2
Memory: 64GB
Time: 4 hours
Partition: gpu
```

**Modules**: `CESGA/2023`, `gromacs/2023.1`, `cuda/11.8`

---

### 5. **Protein Domain Annotation (HMMER)**
**File**: `scripts/cesga_script_examples.sh` → `EXAMPLE_5_DOMAIN_ANNOTATION`

**What it does**:
- Identifies functional domains in proteins
- Scans against Pfam database
- Reports domain positions and e-values
- Suitable for protein function annotation

**Resources**:
```
CPUs: 8
GPUs: 0
Memory: 16GB
Time: 45 minutes
Partition: cpu
```

**Modules**: `CESGA/2023`, `hmmer/3.3.2`

---

### 6. **Complete Bioinformatics Pipeline**
**File**: `scripts/cesga_script_examples.sh` → `EXAMPLE_6_COMPLETE_PIPELINE`

**What it does**:
- Multi-step analysis: BLAST → HMMER → Structure prediction → AlphaFold
- Error handling with `set -e` (stops on first error)
- Generates summary report
- Production-grade logging

**Resources**:
```
CPUs: 16
GPUs: 1
Memory: 64GB
Time: 6 hours
Partition: gpu
```

**Modules**: `CESGA/2023`, `python/3.11`, `ncbi-toolkit/2.14.0`, `hmmer/3.3.2`

---

## How to Extract and Use Scripts

### Option 1: From Shell Functions

```bash
# Source the examples file
source scripts/cesga_script_examples.sh

# Get AlphaFold2 script
EXAMPLE_1_ALPHAFOLD2 > my_alphafold.sh

# Get BLAST script
EXAMPLE_2_BLAST_SEARCH > my_blast.sh

# Make executable
chmod +x my_alphafold.sh
```

### Option 2: Direct JSON Submissions

```bash
# Get the JSON payload
cat scripts/cesga_api_submit_examples.json
```

---

## API Submission Examples

### Using cURL

#### 1. Submit AlphaFold2 Job

```bash
curl -X POST http://localhost:8000/api/v1/jobs \
  -H "Content-Type: application/json" \
  -d '{
    "job_name": "alphafold2_protein_prediction",
    "job_type": "COMPUTE",
    "script_type": "ALPHAFOLD",
    "script_content": "#!/bin/bash\n#SBATCH --job-name=alphafold2_prediction\n...",
    "resources": {
      "cpus": 8,
      "gpus": 1,
      "memory_gb": 32,
      "wall_time_hours": 2
    }
  }'
```

#### 2. Submit BLAST Job

```bash
curl -X POST http://localhost:8000/api/v1/jobs \
  -H "Content-Type: application/json" \
  -d '{
    "job_name": "blast_database_search",
    "job_type": "COMPUTE",
    "script_type": "BLAST",
    "script_content": "#!/bin/bash\n#SBATCH --job-name=blast_search\n...",
    "resources": {
      "cpus": 16,
      "gpus": 0,
      "memory_gb": 32,
      "wall_time_hours": 1.5
    }
  }'
```

### Using Python requests

```python
import requests
import json

# Read the JSON examples
with open('scripts/cesga_api_submit_examples.json', 'r') as f:
    examples = json.load(f)

# Get AlphaFold2 payload
payload = examples['example_1_alphafold2']['payload']

# Submit to API
response = requests.post(
    'http://localhost:8000/api/v1/jobs',
    json=payload,
    headers={'Content-Type': 'application/json'}
)

print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")
```

---

## Expected API Response

When you submit a script, the API validates it and returns:

```json
{
  "job_id": "job_1234567890",
  "status": "QUEUED",
  "message": "Script validated successfully",
  "validation_results": {
    "is_valid": true,
    "errors": [],
    "warnings": [],
    "resource_estimate": {
      "cpus": 8,
      "gpus": 1,
      "memory_gb": 32,
      "wall_time_hours": 2
    }
  }
}
```

---

## Submission Workflow

```
┌─────────────────────────────────────┐
│ 1. Choose Script Type               │
│    (AlphaFold, BLAST, etc.)         │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│ 2. Extract Script Content           │
│    (from examples or JSON)          │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│ 3. Create API Payload               │
│    (with resources, modules)        │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│ 4. Submit to API                    │
│    (POST /api/v1/jobs)              │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│ 5. Receive Job ID & Validation      │
│    (status: QUEUED/VALIDATED)       │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│ 6. Monitor Job Status               │
│    (GET /api/v1/jobs/{job_id})      │
└─────────────────────────────────────┘
```

---

## Key Features of These Scripts

### ✅ Realistic SBATCH Directives
All scripts use actual CESGA parameters:
- `--partition=gpu` or `--partition=cpu` (real partitions)
- `--gres=gpu:N` (GPU request syntax)
- `--time` (HH:MM:SS format)
- `--mem` (memory allocation)

### ✅ Proper Module Loading
```bash
module load CESGA/2023
module load python/3.10
module load cuda/11.8
```

### ✅ Error Handling
```bash
set -e              # Exit on error
if [ $? -eq 0 ]; then
    echo "Success"
else
    echo "Error" >&2
    exit 1
fi
```

### ✅ Logging and Progress Tracking
```bash
echo "[$(date)] Starting step..."
echo "[Step 1/4] Processing..."
```

### ✅ Resource Awareness
- CPU limits respected (max 128)
- GPU limits respected (max 4)
- Memory aligned with CESGA nodes (32GB, 64GB, 256GB)
- Time limits appropriate (2-6 hours typically)

---

## Script Validation Checklist

Before submission, each script is verified for:

- [ ] Starts with `#!/bin/bash`
- [ ] Has `#SBATCH` directives before any commands
- [ ] `cpus-per-task` ≤ 128
- [ ] `gres=gpu:*` ≤ 4
- [ ] `mem` ≤ 256G
- [ ] `time` ≤ 24:00:00
- [ ] All modules are known
- [ ] `script_type` matches content
- [ ] Bash syntax is valid (quotes, parentheses)
- [ ] No obvious security issues

---

## What Happens During Validation

When you submit a script, the API's `CESGAScriptValidator`:

1. **Checks shebang** - Ensures `#!/bin/bash`
2. **Extracts SBATCH directives** - Parses all `#SBATCH` lines
3. **Validates parameters** - Checks for typos in directive names
4. **Validates resources** - Ensures within CESGA limits
5. **Extracts modules** - Finds `module load` statements
6. **Validates modules** - Warns if module is unknown
7. **Type detection** - Identifies BLAST, AlphaFold, etc.
8. **Bash syntax check** - Validates shell script syntax

**Result**: Pass/fail with detailed error/warning messages

---

## Common Modifications

### Adjust CPUs:
```bash
#SBATCH --cpus-per-task=4   # Instead of 8
```

### Adjust Memory:
```bash
#SBATCH --mem=64G   # Instead of 32G
```

### Change Run Time:
```bash
#SBATCH --time=03:00:00   # 3 hours instead of 2
```

### Add Output Files:
```bash
#SBATCH --output=job_%j.out
#SBATCH --error=job_%j.err
```

---

## Files Reference

| File | Purpose |
|------|---------|
| `scripts/cesga_script_examples.sh` | 6 shell functions with complete scripts |
| `scripts/cesga_api_submit_examples.json` | JSON payloads ready for curl/API |
| `cesga_script_validator.py` | Validation engine (already integrated) |
| `REALISTIC_SCRIPTS_GUIDE.md` | Detailed documentation with examples |

---

## Next Steps

1. **Extract a script** from the shell examples or JSON
2. **Customize if needed** (adjust CPUs, memory, time)
3. **Submit to API** using curl or Python requests
4. **Check validation** results
5. **Monitor job** status with job ID

---

## Support

For issues:
1. Check validation error messages
2. Review script syntax with `bash -n script.sh`
3. Verify modules exist: `module avail`
4. Check resource limits match CESGA documentation

---

**These scripts are production-ready and follow CESGA Finis Terrae II/III standards.**
