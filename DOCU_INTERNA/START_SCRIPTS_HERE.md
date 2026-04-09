# 🚀 READY-TO-USE CESGA SCRIPTS - START HERE

## ⚡ 30-Second Quick Start

You have **6 production-ready CESGA Slurm batch scripts** - copy and submit them directly!

### **Step 1: Pick Your Script**

```
1. AlphaFold2      - Protein structure prediction
2. BLAST           - Find similar proteins (homology search)
3. GROMACS         - Run molecular dynamics simulations
4. HMMER           - Identify protein domains
5. MSA             - Align multiple protein sequences
6. Pipeline        - Run complete analysis (all 4 tools)
```

### **Step 2: Copy the Script**

**Option A - Open this file**: [`COPY_PASTE_EXAMPLES.md`](COPY_PASTE_EXAMPLES.md)
- Contains all 6 scripts ready to copy/paste
- Just copy the entire script section you need
- Time: 1 minute

**Option B - View all in JSON**: `scripts/cesga_api_submit_examples.json`
- All scripts in API-ready JSON format
- Copy the "script_content" field
- Time: 2 minutes

### **Step 3: Submit to API**

**Using curl:**
```bash
curl -X POST http://localhost:8000/api/v1/jobs \
  -H "Content-Type: application/json" \
  -d '{
    "job_name": "my_analysis",
    "script_type": "ALPHAFOLD",
    "script_content": "#!/bin/bash\n#SBATCH ...",
    "resources": {"cpus": 8, "gpus": 1, "memory_gb": 32, "wall_time_hours": 2}
  }'
```

**Using Python:**
```python
import requests
payload = {
    "job_name": "my_analysis",
    "script_type": "ALPHAFOLD",
    "script_content": "#!/bin/bash\n...",
    "resources": {"cpus": 8, "gpus": 1, "memory_gb": 32, "wall_time_hours": 2}
}
requests.post('http://localhost:8000/api/v1/jobs', json=payload)
```

### **Result: You Get Back**

```json
{
  "job_id": "job_1234567890",
  "status": "VALIDATED",
  "is_valid": true
}
```

---

## 📋 The 6 Scripts at a Glance

| Script | Purpose | GPU | Time | Go To |
|--------|---------|-----|------|-------|
| AlphaFold2 | 3D protein structure | 1 | 2h | COPY_PASTE_EXAMPLES.md |
| BLAST | Protein homology search | 0 | 1.5h | ↓ |
| GROMACS | Molecular dynamics | 2 | 4h | ↓ |
| HMMER | Find protein domains | 0 | 45m | ↓ |
| MSA | Align protein sequences | 0 | 1h | ↓ |
| Pipeline | All-in-one analysis | 1 | 6h | ↓ |

---

## 📚 Documentation Maps

### **I Want to DO SOMETHING** (Action-oriented)

| What | Time | Where |
|------|------|-------|
| Submit a script NOW | 2 min | [`COPY_PASTE_EXAMPLES.md`](COPY_PASTE_EXAMPLES.md) |
| Understand 6 scripts | 5 min | [`SCRIPTS_READY_TO_USE.md`](SCRIPTS_READY_TO_USE.md) |
| Learn the full workflow | 10 min | [`SCRIPT_SUBMISSION_GUIDE.md`](SCRIPT_SUBMISSION_GUIDE.md) |
| Understand validation | 15 min | [`REALISTIC_SCRIPTS_GUIDE.md`](REALISTIC_SCRIPTS_GUIDE.md) |
| Find what I need | 1 min | [`SCRIPTS_INDEX.md`](SCRIPTS_INDEX.md) |

### **I Want SPECIFIC INFORMATION** (Reference)

| Question | Answer |
|----------|--------|
| What's the AlphaFold2 script? | [`COPY_PASTE_EXAMPLES.md`](COPY_PASTE_EXAMPLES.md#example-1-alphafold2) |
| How much CPU/GPU/memory? | [`SCRIPTS_READY_TO_USE.md`](SCRIPTS_READY_TO_USE.md#resource-allocation-matrix) |
| What are the SBATCH parameters? | [`REALISTIC_SCRIPTS_GUIDE.md`](REALISTIC_SCRIPTS_GUIDE.md#sbatch-directives) |
| Show me JSON format | `scripts/cesga_api_submit_examples.json` |
| Extract a script via shell | `scripts/cesga_script_examples_v2.sh` |

---

## ✅ All 6 Scripts Ready

### **1. AlphaFold2 - Structure Prediction** 🧬

```
Purpose: Predict 3D protein structure from amino acid sequence
Resources: 8 CPUs, 1 GPU, 32GB RAM, 2 hours
For: Drug discovery, structural biology, protein engineering
```
👉 Go to: [`COPY_PASTE_EXAMPLES.md#example-1-alphafold2`](COPY_PASTE_EXAMPLES.md#example-1-alphafold2)

### **2. BLAST - Homology Search** 🔍

```
Purpose: Find similar proteins in biological databases
Resources: 16 CPUs, 0 GPUs, 32GB RAM, 1.5 hours
For: Protein identification, evolutionary studies, function annotation
```
👉 Go to: [`COPY_PASTE_EXAMPLES.md#example-2-blast-database-search`](COPY_PASTE_EXAMPLES.md#example-2-blast-database-search)

### **3. GROMACS - Molecular Dynamics** 📊

```
Purpose: Simulate molecular dynamics at atomic level
Resources: 8 CPUs, 2 GPUs, 64GB RAM, 4 hours
For: MD simulations, protein folding, drug docking, material science
```
👉 Go to: [`COPY_PASTE_EXAMPLES.md#example-3-gromacs-molecular-dynamics`](COPY_PASTE_EXAMPLES.md#example-3-gromacs-molecular-dynamics)

### **4. HMMER - Domain Identification** 🏷️

```
Purpose: Identify functional domains in proteins
Resources: 8 CPUs, 0 GPUs, 16GB RAM, 45 minutes
For: Protein annotation, domain discovery, function prediction
```
👉 Go to: [`COPY_PASTE_EXAMPLES.md#example-4-hmmer-domain-detection`](COPY_PASTE_EXAMPLES.md#example-4-hmmer-domain-detection)

### **5. MSA - Multiple Alignment** 🧵

```
Purpose: Align multiple protein sequences
Resources: 12 CPUs, 0 GPUs, 16GB RAM, 1 hour
For: Phylogenetic analysis, evolution studies, motif discovery
```
👉 Go to: [`COPY_PASTE_EXAMPLES.md#example-5-curl-submit-command`](COPY_PASTE_EXAMPLES.md#example-5-curl-submit-command)

### **6. Pipeline - Complete Analysis** 🔄

```
Purpose: Run complete bioinformatics analysis workflow
Resources: 16 CPUs, 1 GPU, 64GB RAM, 6 hours
For: Comprehensive protein characterization, research pipelines
Runs: BLAST → HMMER → Structure Prediction → AlphaFold2
```
👉 Go to: [`REALISTIC_SCRIPTS_GUIDE.md`](REALISTIC_SCRIPTS_GUIDE.md)

---

## 🎯 Common Scenarios

### **Scenario 1: "I need to predict a protein structure"**

```
1. Open: COPY_PASTE_EXAMPLES.md
2. Find: EXAMPLE 1: AlphaFold2
3. Copy: The entire script
4. Submit: Via curl or Python
5. Wait: ~2 hours for results
```

### **Scenario 2: "I need to find similar proteins"**

```
1. Open: COPY_PASTE_EXAMPLES.md
2. Find: EXAMPLE 2: BLAST Database Search
3. Copy: The entire script
4. Submit: Via curl or Python
5. Wait: ~1.5 hours for results
```

### **Scenario 3: "I need to run MD simulation"**

```
1. Open: COPY_PASTE_EXAMPLES.md
2. Find: EXAMPLE 3: GROMACS Molecular Dynamics
3. Copy: The entire script
4. Submit: Via curl or Python
5. Wait: ~4 hours for results
```

### **Scenario 4: "I need to customize resources"**

```
1. Get the base script
2. Edit these lines:
   #SBATCH --cpus-per-task=16    (was 8)
   #SBATCH --mem=64G             (was 32G)
   #SBATCH --gres=gpu:2          (was gpu:1)
   #SBATCH --time=04:00:00       (was 02:00:00)
3. Update JSON resource fields to match
4. Submit
```

---

## 💻 Three Ways to Use

### **Method 1: Copy/Paste (Fastest - 2 minutes)**

```
→ Open: COPY_PASTE_EXAMPLES.md
→ Copy: Entire script + JSON
→ Submit: Via curl/Python
✓ Done!
```

### **Method 2: Shell Functions (Still Easy - 3 minutes)**

```bash
source scripts/cesga_script_examples_v2.sh
EXAMPLE_1_ALPHAFOLD2 > my_script.sh
# Edit and submit...
```

### **Method 3: JSON Payloads (API-Ready - 2 minutes)**

```bash
cat scripts/cesga_api_submit_examples.json
# Extract and submit...
```

---

## 🔥 Real Example: 60 Seconds to Submission

```bash
# 1. Open copy/paste guide (20 seconds)
cat COPY_PASTE_EXAMPLES.md | head -50

# 2. Copy AlphaFold2 JSON payload (10 seconds)
# (see EXAMPLE 1 in the file)

# 3. Save to file (5 seconds)
cat > payload.json << 'EOF'
{
  "job_name": "protein_analysis",
  "script_type": "ALPHAFOLD",
  "script_content": "#!/bin/bash\n#SBATCH ...",
  "resources": {"cpus": 8, "gpus": 1, "memory_gb": 32, "wall_time_hours": 2}
}
EOF

# 4. Submit (15 seconds)
curl -X POST http://localhost:8000/api/v1/jobs -d @payload.json

# 5. Get result (10 seconds)
# {"job_id": "job_1234567890", "status": "VALIDATED"}

# Total: ~60 seconds! ✅
```

---

## 📖 Navigation Quick Links

**Read These In Order:**

1. **Start**: This file (you are here!)
2. **Copy/Paste**: [`COPY_PASTE_EXAMPLES.md`](COPY_PASTE_EXAMPLES.md) - Get scripts
3. **Overview**: [`SCRIPTS_READY_TO_USE.md`](SCRIPTS_READY_TO_USE.md) - Understand system
4. **Details**: [`SCRIPT_SUBMISSION_GUIDE.md`](SCRIPT_SUBMISSION_GUIDE.md) - Learn workflow
5. **Reference**: [`REALISTIC_SCRIPTS_GUIDE.md`](REALISTIC_SCRIPTS_GUIDE.md) - Technical details
6. **Help**: [`SCRIPTS_INDEX.md`](SCRIPTS_INDEX.md) - Find anything

---

## ✨ What's Included

```
✅ 6 production-ready scripts
✅ All scripts validated
✅ Shell function versions
✅ JSON payload versions
✅ Copy/paste examples
✅ Curl commands
✅ Python code
✅ Complete documentation
✅ Quick reference guides
✅ Resource allocation tables
```

---

## 🎓 Key Facts

- **All scripts are REALISTIC** - Match real CESGA usage
- **All scripts are VALIDATED** - Pass all constraint checks
- **All scripts are SAFE** - No execution, only validation
- **All scripts are READY** - Copy and submit immediately
- **All scripts are DOCUMENTED** - Clear examples for each

---

## ⚡ TL;DR

```
What do you want to do?

👉 Run now?        → Go to COPY_PASTE_EXAMPLES.md (2 min)
👉 Understand?     → Go to SCRIPTS_READY_TO_USE.md (5 min)
👉 Learn details?  → Go to SCRIPT_SUBMISSION_GUIDE.md (10 min)
👉 Get reference?  → Go to SCRIPTS_INDEX.md (1 min)
👉 Need help?      → Go to REALISTIC_SCRIPTS_GUIDE.md (20 min)
```

---

## 🚀 Next Step

**Pick ONE action:**

1. **Copy a script**
   - Open [`COPY_PASTE_EXAMPLES.md`](COPY_PASTE_EXAMPLES.md)
   - Copy your chosen script
   - Submit to API

2. **Learn the system**
   - Open [`SCRIPTS_READY_TO_USE.md`](SCRIPTS_READY_TO_USE.md)
   - Read the overview (5 minutes)
   - Then choose a script to try

3. **Get complete guide**
   - Open [`SCRIPT_SUBMISSION_GUIDE.md`](SCRIPT_SUBMISSION_GUIDE.md)
   - Follow the full workflow

---

## 📞 Common Questions

**Q: Which script should I use?**
A: See "The 6 Scripts at a Glance" above

**Q: How much CPU/GPU/memory?**
A: Check the table in SCRIPTS_READY_TO_USE.md

**Q: Can I modify the scripts?**
A: Yes! See customization examples in COPY_PASTE_EXAMPLES.md

**Q: How do I submit?**
A: See "Real Example: 60 Seconds to Submission" above

**Q: Where's the validation happening?**
A: In app/services/cesga_script_validator.py (already integrated)

---

## ✅ Checklist: Ready to Submit

- [ ] Opened a guide (COPY_PASTE_EXAMPLES.md recommended)
- [ ] Found your script type
- [ ] Copied script + JSON payload
- [ ] Modified resources if needed
- [ ] Have curl or Python requests ready
- [ ] Know your API endpoint URL
- [ ] Ready to submit!

---

**🎉 Everything is ready. Start with [`COPY_PASTE_EXAMPLES.md`](COPY_PASTE_EXAMPLES.md) and submit your first script now!** 🚀
