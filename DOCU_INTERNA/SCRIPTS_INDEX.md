# 🎯 CESGA API - Quick Access Index

## 📌 START HERE

You have a complete, production-ready CESGA API with realistic Slurm batch scripts ready for validation.

---

## 🚀 For Different Use Cases

### **I want to submit a script immediately**
👉 Go to: [`COPY_PASTE_EXAMPLES.md`](COPY_PASTE_EXAMPLES.md)

- Scroll to your script type (AlphaFold, BLAST, GROMACS, etc.)
- Copy the entire script
- Create JSON payload
- Submit via curl or Python

**Time to first submission: 2 minutes**

---

### **I want to understand how the API works**
👉 Go to: [`SCRIPT_SUBMISSION_GUIDE.md`](SCRIPT_SUBMISSION_GUIDE.md)

- Overview of 6 available scripts
- Resource requirements per script
- Complete workflow diagrams
- Validation checklist

**Learning time: 10-15 minutes**

---

### **I want all the technical details**
👉 Go to: [`REALISTIC_SCRIPTS_GUIDE.md`](REALISTIC_SCRIPTS_GUIDE.md)

- Deep dive into Slurm batch script structure
- 4 complete realistic examples with explanations
- Parameter validation rules
- API endpoint design

**Reference time: 20-30 minutes**

---

### **I want to extract scripts from shell functions**
👉 Use: `scripts/cesga_script_examples_v2.sh`

```bash
# Make executable and source
chmod +x scripts/cesga_script_examples_v2.sh
source scripts/cesga_script_examples_v2.sh

# Extract any example
EXAMPLE_1_ALPHAFOLD2 > my_alphafold.sh
EXAMPLE_2_BLAST_SEARCH > my_blast.sh
EXAMPLE_3_MSA > my_msa.sh
# ... etc
```

---

### **I want JSON payloads ready to use**
👉 Use: `scripts/cesga_api_submit_examples.json`

Contains all 6 scripts in JSON format:
- Complete payloads for curl/requests
- Python example code
- Validation checklist

```bash
# View all examples
cat scripts/cesga_api_submit_examples.json

# Or count them
cat scripts/cesga_api_submit_examples.json | grep '"example_' | wc -l
```

---

### **I want the big picture overview**
👉 Go to: [`SCRIPTS_READY_TO_USE.md`](SCRIPTS_READY_TO_USE.md)

- Executive summary
- All 6 scripts overview
- Resource allocation matrix
- Integration points

**Overview time: 5-10 minutes**

---

## 📁 File Organization

```
API_CESGA/
├── COPY_PASTE_EXAMPLES.md          ← Start here for quick submissions
├── SCRIPT_SUBMISSION_GUIDE.md      ← Detailed usage guide
├── SCRIPTS_READY_TO_USE.md         ← Complete overview
├── REALISTIC_SCRIPTS_GUIDE.md      ← Technical details
├── SCRIPTS_INDEX.md                ← You are here
│
├── scripts/
│   ├── cesga_script_examples_v2.sh     ← Shell functions (6 scripts)
│   └── cesga_api_submit_examples.json  ← JSON payloads ready to use
│
├── app/
│   └── services/
│       └── cesga_script_validator.py   ← Validation engine (already integrated)
│
└── [Other API files...]
```

---

## 🎓 The 6 Available Scripts

| # | Script | Purpose | CPUs | GPUs | RAM | Time |
|---|--------|---------|------|------|-----|------|
| 1 | **AlphaFold2** | Protein structure prediction | 8 | 1 | 32G | 2h |
| 2 | **BLAST** | Homology search | 16 | 0 | 32G | 1.5h |
| 3 | **GROMACS** | Molecular dynamics | 8 | 2 | 64G | 4h |
| 4 | **HMMER** | Domain identification | 8 | 0 | 16G | 45m |
| 5 | **MSA** | Multiple sequence alignment | 12 | 0 | 16G | 1h |
| 6 | **Pipeline** | Complete analysis | 16 | 1 | 64G | 6h |

---

## 💻 How to Use

### Option 1: Quickest Way (2 minutes)

```bash
# Read the copy/paste guide
cat COPY_PASTE_EXAMPLES.md

# Copy a script section
# Modify if needed
# Submit to API via curl
curl -X POST http://localhost:8000/api/v1/jobs -d '{...}'
```

### Option 2: Via Shell Functions (3 minutes)

```bash
source scripts/cesga_script_examples_v2.sh
EXAMPLE_1_ALPHAFOLD2 > my_script.sh

# Convert to JSON and submit
python3 << 'PYTHON'
import json
with open('my_script.sh') as f:
    script = f.read()
print(json.dumps({"script_content": script}))
PYTHON
```

### Option 3: Via JSON (2 minutes)

```bash
# View JSON payloads
cat scripts/cesga_api_submit_examples.json

# Extract AlphaFold2
cat scripts/cesga_api_submit_examples.json | \
  jq '.example_1_alphafold2.payload' > payload.json

# Submit it
curl -X POST http://localhost:8000/api/v1/jobs -d @payload.json
```

### Option 4: Python Requests (5 minutes)

```python
import requests
payload = {
    "job_name": "my_analysis",
    "script_type": "BLAST",
    "script_content": "#!/bin/bash\n#SBATCH ...",
    "resources": {"cpus": 16, "gpus": 0, "memory_gb": 32, "wall_time_hours": 1.5}
}
r = requests.post('http://localhost:8000/api/v1/jobs', json=payload)
print(r.json()['job_id'])
```

---

## ✅ Validation Process

All scripts go through this validation:

```
Script Submitted
       ↓
[1] Check shebang (#!/bin/bash)
       ↓
[2] Parse SBATCH directives
       ↓
[3] Validate resource limits (CPUs ≤ 128, GPUs ≤ 4, mem ≤ 256G)
       ↓
[4] Check modules are recognized
       ↓
[5] Detect script type (AlphaFold, BLAST, etc.)
       ↓
[6] Validate bash syntax
       ↓
✓ PASS → Return job_id, queued for execution
✗ FAIL → Return errors, request retry
```

---

## 🔍 Common Scenarios

### Scenario 1: "I want to run AlphaFold2"

1. Open [`COPY_PASTE_EXAMPLES.md`](COPY_PASTE_EXAMPLES.md)
2. Go to "EXAMPLE 1: AlphaFold2"
3. Copy the script
4. Copy the JSON payload
5. Submit via curl or Python
6. Get back job_id

**Time: 2 minutes**

---

### Scenario 2: "I want to understand the validation"

1. Read [`SCRIPT_SUBMISSION_GUIDE.md`](SCRIPT_SUBMISSION_GUIDE.md) - Section "Script Validation Checklist"
2. Read [`SCRIPTS_READY_TO_USE.md`](SCRIPTS_READY_TO_USE.md) - Section "How Validation Works"
3. Review source: `app/services/cesga_script_validator.py`

---

### Scenario 3: "I want to modify an example"

1. Extract script from [`scripts/cesga_script_examples_v2.sh`](scripts/cesga_script_examples_v2.sh)
   ```bash
   source scripts/cesga_script_examples_v2.sh
   EXAMPLE_1_ALPHAFOLD2 > my_script.sh
   ```

2. Modify CPU/memory/time in SBATCH directives

3. Update JSON payload with new resources

4. Submit to API

---

### Scenario 4: "I want to batch submit multiple scripts"

```python
import requests

scripts = [
    {"type": "ALPHAFOLD", "name": "protein_1"},
    {"type": "BLAST", "name": "search_1"},
    {"type": "GROMACS", "name": "md_sim_1"}
]

for script in scripts:
    payload = {
        "job_name": script["name"],
        "script_type": script["type"],
        "script_content": "...",  # Get from examples
        "resources": {...}
    }
    response = requests.post('http://localhost:8000/api/v1/jobs', json=payload)
    print(f"{script['name']}: {response.json()['job_id']}")
```

---

## 📞 When You Need Help

| Question | Answer Location |
|----------|-----------------|
| How do I run AlphaFold2? | [`COPY_PASTE_EXAMPLES.md`](COPY_PASTE_EXAMPLES.md#example-1-alphafold2) |
| What are the resource limits? | [`SCRIPTS_READY_TO_USE.md`](SCRIPTS_READY_TO_USE.md#resource-allocation-matrix) |
| Which SBATCH parameters are valid? | [`REALISTIC_SCRIPTS_GUIDE.md`](REALISTIC_SCRIPTS_GUIDE.md#sbatch-directives) |
| How does validation work? | [`SCRIPTS_READY_TO_USE.md`](SCRIPTS_READY_TO_USE.md#how-validation-works) |
| Can I modify the scripts? | Yes - see resource adjustment examples in any guide |
| Where's the validator code? | `app/services/cesga_script_validator.py` |

---

## 🚦 Next Steps

1. **Choose your action**:
   - Want to submit immediately? → [`COPY_PASTE_EXAMPLES.md`](COPY_PASTE_EXAMPLES.md)
   - Want to learn first? → [`SCRIPTS_READY_TO_USE.md`](SCRIPTS_READY_TO_USE.md)
   - Want details? → [`REALISTIC_SCRIPTS_GUIDE.md`](REALISTIC_SCRIPTS_GUIDE.md)

2. **Pick a script** from the 6 available

3. **Extract/copy it** from examples

4. **Customize if needed** (CPU, memory, time)

5. **Create JSON payload** with script type and resources

6. **Submit to API** via curl or Python

7. **Monitor status** with returned job_id

---

## 📊 Statistics

- **Total scripts ready**: 6
- **Total payload examples**: 6
- **Validation checks**: 6
- **Resource constraints**: 4 (CPUs, GPUs, memory, time)
- **Script types supported**: 6 (AlphaFold, BLAST, GROMACS, HMMER, MSA, Custom)
- **Modules available**: 20+
- **Lines of documentation**: 2000+

---

## 🎯 One-Page Quick Reference

```
1. I want to submit now
   → COPY_PASTE_EXAMPLES.md (2 min)

2. I want to understand
   → SCRIPTS_READY_TO_USE.md (5 min)

3. I want full details
   → REALISTIC_SCRIPTS_GUIDE.md (20 min)

4. I want to use shell functions
   → scripts/cesga_script_examples_v2.sh

5. I want JSON payloads
   → scripts/cesga_api_submit_examples.json
```

---

**Everything is ready. Pick a guide and start submitting! 🚀**

For questions about specific scripts, see the index in the guide you choose.
