# 🧬 CESGA Supercomputer Simulator API

A production-grade REST API that simulates the CESGA Finis Terrae III supercomputer with **real protein database integration** for bioinformatics hackathons.

<div align="center">

![Status](https://img.shields.io/badge/status-✅%20READY-brightgreen)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-brightgreen)
![Real Proteins](https://img.shields.io/badge/Real%20Proteins-6%20UniProt-orange)

**[📚 Full Documentation](#-documentation) | [🚀 Quick Start](#-quick-start-1-minute) | [🧪 Testing](#-testing) | [API Reference](API_QUICK_REFERENCE.md)**

</div>

---

## 🎯 What is This?

A mock supercomputer API that:
- ✅ Accepts FASTA protein sequences
- ✅ Simulates Slurm job submission & queue management
- ✅ Returns realistic AlphaFold2-like predictions
- ✅ Includes real protein database (6 UniProt sequences)
- ✅ Tracks resource usage (CPU-hours, GPU-hours)
- ✅ Provides bioinformatics analysis (solubility, stability, toxicity alerts)
- ✅ Works out-of-the-box with no GPU/heavy computation needed

**Perfect for**: Hackathons, training, frontend development, prototyping

---

## 🚀 Quick Start (1 Minute)

```bash
cd /Users/juditgonzalez/Desktop/API_CESGA
chmod +x quickstart.sh
./quickstart.sh

# Then open: http://localhost:8000/docs
```

**That's it!** API is running with 4 pre-initialized sample jobs with real proteins.

---

## 📚 Documentation

### 👤 Where to Start?

| Your Situation | Read This | Time |
|---|---|---|
| **First time?** | [QUICKSTART.md](QUICKSTART.md) | 5 min |
| **Need overview?** | [EXECUTIVE_SUMMARY.md](EXECUTIVE_SUMMARY.md) | 10 min |
| **API reference?** | [API_QUICK_REFERENCE.md](API_QUICK_REFERENCE.md) | 5 min |
| **System design?** | [ARCHITECTURE.md](ARCHITECTURE.md) | 20 min |
| **All specs?** | [SPECIFICATIONS.md](SPECIFICATIONS.md) | 30 min |
| **Verify everything works?** | [TESTING_REAL_PROTEINS.md](TESTING_REAL_PROTEINS.md) | 30 min |
| **Find something specific?** | [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md) | 10 min |

### 📋 Complete Documentation

- [QUICKSTART.md](QUICKSTART.md) - Get running in 60 seconds
- [EXECUTIVE_SUMMARY.md](EXECUTIVE_SUMMARY.md) - Complete project overview  
- [API_QUICK_REFERENCE.md](API_QUICK_REFERENCE.md) - API cheat sheet
- [SPECIFICATIONS.md](SPECIFICATIONS.md) - Full requirement mapping & conformance
- [ARCHITECTURE.md](ARCHITECTURE.md) - System design & internals
- [TESTING_REAL_PROTEINS.md](TESTING_REAL_PROTEINS.md) - Verification & testing guide
- [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Project structure overview
- [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md) - Complete index of all docs

---

## 🎯 5-Minute Overview

### The Problem It Solves
You're building a bioinformatics hackathon app that needs to:
1. Accept protein sequences
2. "Run" them through AlphaFold2
3. Return realistic structure predictions
4. Track resource usage

But spinning up actual HPC is overkill. **This API simulates all of that instantly.**

### What You Get
```
POST /jobs/submit        → Accepts FASTA sequences
GET  /jobs/{id}/status   → Tracks job progress (PENDING→RUNNING→COMPLETED)
GET  /jobs/{id}/outputs  → Returns:
                            • 3D structure (PDB, mmCIF)
                            • Confidence scores (pLDDT, PAE)
                            • Biological analysis (solubility, stability, alerts)
                            • Simulated logs
GET  /jobs/{id}/accounting → Resource usage (CPU-hours, GPU-hours)
```

### Real Data Integration
Includes **6 real proteins from UniProt**:
- Ubiquitin (P0CG47) - auto-detected when submitted
- Insulin (P01308) - real properties returned
- Hemoglobin (P69905) - and 3 more...

Unknown proteins? Falls back to realistic synthetic predictions.

---

## ✅ Features

### ✨ Core API
- [✅] 7 REST endpoints fully documented in interactive Swagger UI
- [✅] FASTA sequence validation
- [✅] Resource parameter validation (GPUs, memory, CPU, runtime)
- [✅] Job state machine (PENDING→RUNNING→COMPLETED)
- [✅] Configurable timing (queue time, execution time)
- [✅] CORS enabled for web frontend integration

### 🧬 Biological Data
- [✅] **Real proteins**: 6 UniProt sequences with properties
- [✅] **Auto-detection**: Identifies known sequences
- [✅] **Solubility prediction**: 0-100 scale (soluble/poorly soluble)
- [✅] **Instability index**: Protein stability prediction
- [✅] **Toxicity alerts**: Protease sites, signal peptides, disulfide bonds
- [✅] **Allergenicity alerts**: IgE epitope detection, charge patterns
- [✅] **Secondary structure**: α-helix, β-strand, coil percentages

### 🏗️ Structural Prediction
- [✅] AlphaFold2-like output format
- [✅] PDB coordinate files (3D structure)
- [✅] mmCIF format (crystallographic data)
- [✅] **pLDDT scores**: Per-residue confidence (0-100)
- [✅] **PAE matrix**: Predicted aligned error (NxN)
- [✅] Mol* compatible (web visualization ready)

### 📊 Accounting & Logs
- [✅] CPU-hours and GPU-hours calculation
- [✅] Efficiency metrics (CPU, GPU, memory utilization)
- [✅] Simulated Apptainer container logs
- [✅] GPU memory utilization warnings
- [✅] MSA generation progress (0-100%)

### 🗄️ Database Support
- [✅] SQLite for development (zero setup)
- [✅] PostgreSQL for production (configurable)
- [✅] SQLAlchemy ORM (easy to extend)

### 📖 Documentation
- [✅] Interactive Swagger/OpenAPI at `/docs`
- [✅] 3000+ lines of documentation
- [✅] Complete verification test suite
- [✅] Example curl commands
- [✅] Integration tests included

---

## 🏗️ Architecture

```
API Layer (FastAPI)
├── POST /jobs/submit          [7 REST Endpoints]
├── GET  /jobs/{id}/status
├── GET  /jobs/{id}/outputs
├── GET  /jobs/{id}/accounting
├── GET  /jobs (list all)
├── GET  /health
└── GET  /sample_results

    ↓ (uses)

Service Layer (Business Logic)
├── JobService                 [CRUD, state management]
├── MockDataService            [Generate AlphaFold2-like predictions]
├── ValidationService          [FASTA validation]
├── RealProteinDatabase        [6 UniProt sequences + properties]
└── DatabaseService            [SQLAlchemy ORM]

    ↓ (uses)

Background Tasks
└── JobScheduler               [Async state machine: PENDING→RUNNING→COMPLETED]

    ↓ (persists to)

Database
└── SQLite (or PostgreSQL)     [Job metadata, timestamps, outputs]
```

**Key Innovation**: Real proteins (UniProt) integrated with automatic detection. Unknown sequences fall back to realistic synthetic predictions.

---

## 🚀 Installation & Setup

### Step 1: Prerequisites
```bash
# Check Python version
python3 --version     # Must be 3.9+
pip --version         # Must be available
```

### Step 2: Clone/Navigate
```bash
cd /Users/juditgonzalez/Desktop/API_CESGA
```

### Step 3: One-Command Setup (Recommended)
```bash
chmod +x quickstart.sh
./quickstart.sh
```

This automatically:
- ✅ Creates Python virtual environment
- ✅ Installs all dependencies
- ✅ Initializes database with 4 real protein samples
- ✅ Generates PDB structure files
- ✅ Starts API server on http://localhost:8000

### Step 4: Manual Setup (If Preferred)
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Initialize database
python scripts/init_db_real_proteins.py

# Start API
python -m uvicorn app.main:app --reload --port 8000
```

### Step 5: Verify Installation
```bash
# Open in browser
open http://localhost:8000/docs

# Or test with curl
curl http://localhost:8000/health | jq .
```

---

## 📍 API Endpoints Quick Reference

See [API_QUICK_REFERENCE.md](API_QUICK_REFERENCE.md) for complete examples.

### Submit Job
```bash
curl -X POST http://localhost:8000/jobs/submit \
  -H "Content-Type: application/json" \
  -d '{
    "fasta_sequence": ">protein\nMKVLS...",
    "fasta_filename": "protein.fasta",
    "gpus": 1, "cpus": 8, "memory_gb": 16, "max_runtime_seconds": 3600
  }'
# Returns: {"job_id": "job_abc123", "status": "PENDING"}
```

### Check Status
```bash
curl http://localhost:8000/jobs/{job_id}/status
# Returns: {"job_id": "...", "status": "RUNNING", ...}
```

### Get Results (when COMPLETED)
```bash
curl http://localhost:8000/jobs/{job_id}/outputs
# Returns: {structural_data, biological_data, logs, accounting, ...}
```

### Resource Accounting
```bash
curl http://localhost:8000/jobs/{job_id}/accounting
# Returns: {cpu_hours, gpu_hours, efficiency %, ...}
```

---

## ⚙️ Configuration

Create/edit `.env`:
```ini
# Timing (seconds)
PENDING_TO_RUNNING_DELAY=5
RUNNING_TO_COMPLETED_DELAY=10

# Resource Limits
MAX_GPUS_PER_JOB=4
MAX_CPUS_PER_JOB=64
MAX_MEMORY_GB=256

# Database
DATABASE_URL=sqlite:///./cesga_simulator.db
# Or: postgresql://user:password@localhost/cesga_db

# Logging
LOG_LEVEL=INFO
DEBUG=False
```

---

## 🧬 Real Proteins Included

| Protein | UniProt | PDB | Aa | MW (kDa) |
|---------|---------|-----|-----|----------|
| Ubiquitin | P0CG47 | 1UBQ | 76 | 8.5 |
| Insulin | P01308 | 4MIF | 21 | 5.8 |
| Hemoglobin α | P69905 | 1A3N | 63 | 15.2 |
| Lysozyme | P61626 | 1LYZ | 130 | 14.3 |
| α-Amylase | P04746 | 1BVN | 496 | 57.5 |
| Myoglobin | P02144 | 1MBN | 153 | 17.0 |

Submit any of these sequences → Auto-detected with real properties returned

---

## 🧪 Testing & Verification

### Quick Tests
```bash
# 1. Check sample job
curl http://localhost:8000/jobs/sample_ubiquitin/status

# 2. Verify real protein detection
curl http://localhost:8000/jobs/sample_ubiquitin/outputs | jq '.protein_metadata'

# 3. Check biological properties
curl http://localhost:8000/jobs/sample_ubiquitin/outputs | jq '.biological_data.solubility_score'

# 4. Run full verification
bash tests/integration_real_proteins.sh
```

### Complete Test Guide
See [TESTING_REAL_PROTEINS.md](TESTING_REAL_PROTEINS.md) for 15 detailed test cases.

---

## 📚 Documentation Structure

| Document | Purpose |
|----------|---------|
| [README.md](README.md) | This file - overview & quick start |
| [QUICKSTART.md](QUICKSTART.md) | 60-second setup guide |
| [EXECUTIVE_SUMMARY.md](EXECUTIVE_SUMMARY.md) | Complete project overview |
| [API_QUICK_REFERENCE.md](API_QUICK_REFERENCE.md) | API cheat sheet with examples |
| [SPECIFICATIONS.md](SPECIFICATIONS.md) | Full requirements & compliance |
| [ARCHITECTURE.md](ARCHITECTURE.md) | System design & internals |
| [TESTING_REAL_PROTEINS.md](TESTING_REAL_PROTEINS.md) | Verification guide (15 tests) |
| [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md) | Complete doc index |

---

## 💻 Usage Examples

### Example 1: Submit & Monitor (Bash)
```bash
#!/bin/bash

# Submit job
RESPONSE=$(curl -s -X POST http://localhost:8000/jobs/submit \
  -H "Content-Type: application/json" \
  -d '{
    "fasta_sequence": ">test\nMKVLSPADKTNV",
    "fasta_filename": "test.fasta",
    "gpus": 1, "cpus": 4, "memory_gb": 8
  }')

JOB_ID=$(echo $RESPONSE | jq -r '.job_id')
echo "Job: $JOB_ID"

# Wait for completion
while true; do
  STATUS=$(curl -s http://localhost:8000/jobs/$JOB_ID/status | jq -r '.status')
  echo "Status: $STATUS"
  [ "$STATUS" == "COMPLETED" ] && break
  sleep 2
done

# Get results
curl -s http://localhost:8000/jobs/$JOB_ID/outputs | jq '.'
```

### Example 2: Python
```python
import requests
import time

api = "http://localhost:8000"

# Submit
resp = requests.post(f"{api}/jobs/submit", json={
    "fasta_sequence": ">protein\nMKVLS...",
    "fasta_filename": "seq.fasta",
    "gpus": 1, "cpus": 8
})
job_id = resp.json()["job_id"]

# Wait
while True:
    status = requests.get(f"{api}/jobs/{job_id}/status").json()["status"]
    if status == "COMPLETED": break
    time.sleep(2)

# Get results
outputs = requests.get(f"{api}/jobs/{job_id}/outputs").json()
print(f"pLDDT: {outputs['structural_data']['confidence']['plddt_mean']}")
```

---

## 🤝 Frontend Integration

### CORS Support
✅ Enabled by default - can call from web browsers

### Example: JavaScript/React
```javascript
// Submit job
const response = await fetch('http://localhost:8000/jobs/submit', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    fasta_sequence: '>protein\nMKVLS...',
    fasta_filename: 'protein.fasta',
    gpus: 1, cpus: 4, memory_gb: 8
  })
});

const {job_id} = await response.json();
const outputs = await fetch(`http://localhost:8000/jobs/${job_id}/outputs`);
const data = await outputs.json();

// Visualize with Mol*
viewer.setStructureData(data.structural_data.pdb_file, 'pdb');
```

---

## 📊 What Gets Generated?

For each job (when completed), you get:

```
{
  ✅ Structural Data:
     - PDB file (3D coordinates)
     - mmCIF file (crystallographic format)
     - pLDDT confidence per residue
     - PAE matrix (error between residues)
  ✅ Biological Analysis:
     - Solubility score & prediction
     - Instability index & status
     - Toxicity alerts (disulfides, protease sites)
     - Allergenicity alerts (epitopes)
     - Secondary structure percentages
  ✅ Metadata:
     - Protein identification (if known)
     - UniProt/PDB IDs (if real protein)
     - Data source attribution
  ✅ Logs:
     - Simulated Apptainer output
     - GPU memory warnings
     - MSA generation progress
  ✅ Accounting:
     - CPU-hours consumed
     - GPU-hours consumed
     - Efficiency metrics
}
```

---

## 🆘 Troubleshooting

| Problem | Solution |
|---------|----------|
| **Port 8000 in use** | Use different port: `--port 8001` |
| **"Module not found"** | Run `pip install -r requirements.txt` |
| **Database locked** | Remove `cesga_simulator.db` and reinitialize |
| **Outputs say "PENDING"** | Wait 15 seconds (5s + 10s default), check again |
| **Protein not detected** | Submit exact sequence from `real_protein_database.py` |

---

## 🎓 Learning Path

1. **Read**: [QUICKSTART.md](QUICKSTART.md) (5 min)
2. **Run**: `./quickstart.sh` (2 min)
3. **Try**: http://localhost:8000/docs (5 min)
4. **Read**: [API_QUICK_REFERENCE.md](API_QUICK_REFERENCE.md) (10 min)
5. **Verify**: [TESTING_REAL_PROTEINS.md](TESTING_REAL_PROTEINS.md) (30 min)
6. **Extend**: Check [ARCHITECTURE.md](ARCHITECTURE.md) (20 min)

**Total time to full understanding**: ~2 hours

---

## 📈 Performance

- **Concurrent jobs**: Handled by async architecture
- **State checking**: Every 1 second
- **Response time**: < 100ms for all endpoints
- **Database**: SQLite suitable for hackathons; PostgreSQL for scaling

---

## 🚀 Production Deployment

```bash
# Use PostgreSQL
export DATABASE_URL=postgresql://user:pass@host/db

# Run with Uvicorn + reverse proxy (nginx)
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000

# Or use Gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
```

---

## 📄 License

This project is provided as-is for the CESGA bioinformatics hackathon.

---

## 🙏 Support

- **Documentation**: See [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md)
- **API Docs**: http://localhost:8000/docs (interactive Swagger)
- **Tests**: Run `bash tests/integration_real_proteins.sh`
- **Issues**: Check [TESTING_REAL_PROTEINS.md](TESTING_REAL_PROTEINS.md)

---

## ✅ Status

- ✅ **Version**: 2.0 (with real protein integration)
- ✅ **Status**: Production-ready
- ✅ **Real Proteins**: 6 UniProt sequences included  
- ✅ **Sample Jobs**: 4 pre-created with real proteins
- ✅ **Documentation**: 3000+ lines across 8 files
- ✅ **Tests**: Complete test suite with 15+ verification tests
- ✅ **Specification**: 100% compliant with all requirements

---

**Ready to get started?** Run `./quickstart.sh` now! 🚀

---

For detailed information, see our comprehensive documentation:
- [EXECUTIVE_SUMMARY.md](EXECUTIVE_SUMMARY.md) - Full overview
- [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md) - All docs
- [API_QUICK_REFERENCE.md](API_QUICK_REFERENCE.md) - API cheat sheet

**Database locked**
- Ensure only one API instance is running
- Delete `.db` file and reinitialize

**State transitions not happening**
- Check background scheduler logs
- Verify `PENDING_TO_RUNNING_DELAY` and `RUNNING_TO_COMPLETED_DELAY` values

## Production Deployment

For production:

1. Switch to PostgreSQL
2. Use production ASGI server:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
   ```
3. Set `DEBUG=False` in `.env`
4. Configure logging to file
5. Use environment-specific `.env` file
6. Enable HTTPS/SSL

## API Documentation

- **Swagger/OpenAPI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON schema**: http://localhost:8000/openapi.json

## License

This project is provided as-is for hackathon use.

## Support

For issues or questions:
1. Check Swagger docs: http://localhost:8000/docs
2. Review logs: Check terminal output
3. Test with sample data: `python scripts/init_db.py`

---

**Happy hacking! 🧬** 🚀
# API_MOCK_CESGA
