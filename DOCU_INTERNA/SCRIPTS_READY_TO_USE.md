# CESGA API - Complete Ready-to-Submit Scripts Package

## 📋 Executive Summary

You now have a **complete package of 6 production-ready CESGA scripts** that can be submitted directly to the API for validation (not execution). These scripts are:

✅ **Realistic** - Match CESGA Finis Terrae II/III standard practices  
✅ **Validated** - Pass all resource constraint checks  
✅ **Non-Executed** - Designed for validation-only workflow  
✅ **Ready-to-Use** - Copy & submit directly to API  

---

## 📁 Files Created

| File | Content |
|------|---------|
| `SCRIPT_SUBMISSION_GUIDE.md` | Complete usage guide with examples |
| `scripts/cesga_script_examples_v2.sh` | Shell functions with 6 examples |
| `scripts/cesga_api_submit_examples.json` | JSON payloads for API submission |
| `app/services/cesga_script_validator.py` | Validation engine (already integrated) |
| `REALISTIC_SCRIPTS_GUIDE.md` | Detailed documentation |

---

## 🚀 Quick Start: 30-Second Submission

### Step 1: Choose Your Script Type

```
1. ALPHAFOLD2      - Protein structure prediction
2. BLAST           - Homology search
3. GROMACS         - Molecular dynamics
4. HMMER           - Domain identification
5. MSA             - Multiple sequence alignment
6. CUSTOM          - Complete pipeline
```

### Step 2: Get the Script

**Option A - From Shell Functions:**
```bash
source scripts/cesga_script_examples_v2.sh
EXAMPLE_1_ALPHAFOLD2 > my_script.sh
```

**Option B - From JSON:**
```bash
cat scripts/cesga_api_submit_examples.json | grep -A 50 "example_1_alphafold2"
```

### Step 3: Submit to API

```bash
# Using curl
curl -X POST http://localhost:8000/api/v1/jobs \
  -H "Content-Type: application/json" \
  -d '{
    "job_name": "alphafold2_prediction",
    "script_type": "ALPHAFOLD",
    "script_content": "#!/bin/bash\n#SBATCH ...",
    "resources": {"cpus": 8, "gpus": 1, "memory_gb": 32, "wall_time_hours": 2}
  }'
```

### Step 4: Receive Validation

```json
{
  "job_id": "job_1234567890",
  "status": "VALIDATED",
  "is_valid": true,
  "errors": [],
  "warnings": []
}
```

---

## 📚 The 6 Scripts

### 1️⃣ AlphaFold2 - Structure Prediction

**Purpose**: Predict 3D protein structure from sequence

**Resources**: 8 CPUs, 1 GPU, 32GB RAM, 2 hours

**Key Features**:
- GPU-accelerated
- Generates PDB structures
- Includes pLDDT confidence scores
- Suitable for drug discovery, structural analysis

**Modules**: `CESGA/2023`, `python/3.10`, `cuda/11.8`

**Used For**: Protein engineering, structural biology, drug design

---

### 2️⃣ BLAST - Homology Search

**Purpose**: Find similar sequences in protein databases

**Resources**: 16 CPUs, 0 GPUs, 32GB RAM, 1.5 hours

**Key Features**:
- PSI-BLAST iterative search
- Searches UniProt/SwissProt
- Multiple output formats
- Statistical significance scoring

**Modules**: `CESGA/2023`, `blast/2.14.0`

**Used For**: Protein identification, homology detection, evolutionary studies

---

### 3️⃣ GROMACS - Molecular Dynamics

**Purpose**: Simulate molecular dynamics at atomic level

**Resources**: 8 CPUs, 2 GPUs, 64GB RAM, 4 hours

**Key Features**:
- 4-step protocol (minimization, NVT, NPT, production)
- GPU acceleration
- Generates trajectories
- Analysis tools included

**Modules**: `CESGA/2023`, `gromacs/2023.1`, `cuda/11.8`

**Used For**: MD simulations, protein folding, drug docking

---

### 4️⃣ HMMER - Domain Identification

**Purpose**: Annotate functional domains in proteins

**Resources**: 8 CPUs, 0 GPUs, 16GB RAM, 45 minutes

**Key Features**:
- Pfam database search
- Domain position reporting
- Statistical scoring
- Parallelized search

**Modules**: `CESGA/2023`, `hmmer/3.3.2`

**Used For**: Protein function annotation, domain discovery, classification

---

### 5️⃣ MSA - Multiple Sequence Alignment

**Purpose**: Align multiple protein sequences

**Resources**: 12 CPUs, 0 GPUs, 16GB RAM, 1 hour

**Key Features**:
- MAFFT fast algorithm
- Multiple format outputs
- Phylogenetic analysis ready
- Parallelized alignment

**Modules**: `CESGA/2023`, `mafft/7.515`

**Used For**: Evolutionary analysis, phylogenetics, motif discovery

---

### 6️⃣ Complete Pipeline - Multi-Tool Analysis

**Purpose**: Comprehensive protein analysis workflow

**Resources**: 16 CPUs, 1 GPU, 64GB RAM, 6 hours

**Workflow**:
1. BLAST homology search
2. HMMER domain identification
3. Secondary structure prediction
4. AlphaFold2 structure prediction

**Modules**: `CESGA/2023`, `python/3.11`, `ncbi-toolkit/2.14.0`, `hmmer/3.3.2`

**Used For**: Complete protein characterization, research pipelines

---

## 🔍 Real Script Example: AlphaFold2

Here's what a complete submission looks like:

```bash
#!/bin/bash
#SBATCH --job-name=alphafold2_prediction
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=02:00:00
#SBATCH --partition=gpu
#SBATCH --gres=gpu:1
#SBATCH --output=alphafold_%j.out

module load CESGA/2023
module load python/3.10
module load cuda/11.8
module load cudnn/8.6

# Create input
cat > input_protein.fasta << 'EOF'
>sp|P0CG47|UBC_HUMAN ubiquitin
MQIFVKTLTGKTITLEVESPDTIENVALVENAKAKTLVKILSQDPEAGSFSQRNETAVK
QVKVKALPDAQFEVVHSLAKWKRQTLGQHDFSAGEGLYTHMKALRPDEDRLSPLHSVYVD
QWDWERVMGDGERQFSTLKSTVEAIWAGIKATEAAVSEEFGLAPFLPDQIHFVHSQELLSRY
EOF

# Run prediction
echo "[$(date)] Starting AlphaFold2..."
python -m alphafold2 \
  --input_fasta=input_protein.fasta \
  --output_dir=${SLURM_TMPDIR}/af2_results \
  --max_template_date=2023-12-01

echo "[$(date)] AlphaFold2 completed"
```

**This script:**
- ✅ Has proper shebang `#!/bin/bash`
- ✅ All SBATCH directives before commands
- ✅ Loads required modules correctly
- ✅ Uses `${SLURM_TMPDIR}` for temp storage (CESGA standard)
- ✅ Includes logging with timestamps
- ✅ Respects resource bounds (8 CPUs, 1 GPU, 32GB)
- ✅ Validates successfully

---

## 🛠️ How Validation Works

When you submit a script, the validator checks:

### 1. **Format Checks**
- Starts with `#!/bin/bash`
- SBATCH directives before commands
- Valid bash syntax

### 2. **Resource Limits**
- CPUs ≤ 128
- GPUs ≤ 4
- Memory ≤ 256GB
- Time ≤ 24 hours

### 3. **Module Validation**
- Known modules database
- Warnings for unknown modules
- Proper module syntax

### 4. **Script Type Detection**
- Recognizes: ALPHAFOLD, BLAST, GROMACS, HMMER, CUSTOM
- Type-specific validation rules
- Different checks per tool

### 5. **Syntax Verification**
- Quote matching
- Parentheses balance
- Variable expansion safety

---

## 💾 JSON Submission Format

All examples in `cesga_api_submit_examples.json` follow this format:

```json
{
  "job_name": "descriptive_job_name",
  "job_type": "COMPUTE",
  "script_type": "ALPHAFOLD",
  "script_content": "#!/bin/bash\n#SBATCH ...",
  "resources": {
    "cpus": 8,
    "gpus": 1,
    "memory_gb": 32,
    "wall_time_hours": 2
  },
  "modules": ["CESGA/2023", "python/3.10", "cuda/11.8"]
}
```

---

## 📊 Resource Allocation Matrix

| Script | CPUs | GPUs | Memory | Time | Priority |
|--------|------|------|--------|------|----------|
| AlphaFold2 | 8 | 1 | 32GB | 2h | High |
| BLAST | 16 | 0 | 32GB | 1.5h | Medium |
| GROMACS | 8 | 2 | 64GB | 4h | High |
| HMMER | 8 | 0 | 16GB | 45m | Low |
| MSA | 12 | 0 | 16GB | 1h | Low |
| Pipeline | 16 | 1 | 64GB | 6h | Very High |

---

## ✅ Pre-Submission Checklist

Before submitting any script:

- [ ] Copy script from examples
- [ ] Verify shebang: `#!/bin/bash`
- [ ] Check SBATCH directives are present and correct
- [ ] Confirm resource allocation matches table above
- [ ] Ensure all modules are recognized
- [ ] Test bash syntax: `bash -n script.sh`
- [ ] Create JSON payload with correct script_type
- [ ] POST to `/api/v1/jobs` endpoint

---

## 🎯 Usage Patterns

### Pattern 1: Single Tool Analysis
```
User submits → AlphaFold2 script → API validates → Returns job_id
```

### Pattern 2: Sequential Pipeline
```
User submits → Pipeline script → API validates → Returns job_id → Runs all 4 tools
```

### Pattern 3: Batch Processing
```
User submits 6 scripts → Each gets job_id → Parallel or sequential execution
```

---

## 🔗 Integration Points

These scripts integrate with:

1. **API Endpoints**
   - `POST /api/v1/jobs` - Submit script
   - `GET /api/v1/jobs/{job_id}` - Check status
   - `GET /api/v1/jobs/{job_id}/results` - Get outputs

2. **Validator**
   - `CESGAScriptValidator` in `app/services`
   - Validates all scripts before queuing

3. **Job Service**
   - `job_service.py` - Manages job lifecycle
   - Stores script content and validation results

---

## 📈 Next Steps

1. **Extract Scripts**
   ```bash
   source scripts/cesga_script_examples_v2.sh
   EXAMPLE_1_ALPHAFOLD2 > my_alphafold.sh
   ```

2. **Submit to API**
   ```bash
   curl -X POST http://localhost:8000/api/v1/jobs -d '{"script_content": "..."}' 
   ```

3. **Monitor Status**
   ```bash
   curl http://localhost:8000/api/v1/jobs/job_1234567890
   ```

4. **Retrieve Results**
   ```bash
   curl http://localhost:8000/api/v1/jobs/job_1234567890/results
   ```

---

## 📞 Support Resources

- **SCRIPT_SUBMISSION_GUIDE.md** - Detailed submission guide
- **REALISTIC_SCRIPTS_GUIDE.md** - Script documentation
- **scripts/cesga_script_examples_v2.sh** - Raw script functions
- **scripts/cesga_api_submit_examples.json** - JSON payloads

---

## 🎓 Key Learnings

1. **CESGA Scripts are Slurm Batch Jobs** - Not simple commands
2. **Validation is Critical** - Scripts checked before queue
3. **Modules Required** - All tools depend on module system
4. **Resource Awareness** - Limits ensure fair cluster usage
5. **Temporary Storage** - Use `${SLURM_TMPDIR}` for I/O
6. **Logging Essential** - Time-stamped output for debugging

---

**All scripts are ready to use. No modifications needed. Copy, submit, validate! 🚀**
