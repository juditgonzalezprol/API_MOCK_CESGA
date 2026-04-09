# CESGA API Simulator - Quick Reference Guide

## 🚀 Super Quick Start (2 minutes)

```bash
# 1. Navigate to project directory
cd /Users/juditgonzalez/Desktop/API_CESGA

# 2. Make script executable and run
chmod +x quickstart.sh
./quickstart.sh

# 3. Start the server (in another terminal)
source venv/bin/activate
python -m uvicorn app.main:app --reload
```

Then visit: **http://localhost:8000/docs**

---

## 📋 Project Structure Overview

```
API_CESGA/
│
├── app/                          # Main application package
│   ├── main.py                  # FastAPI app entry point
│   ├── config.py                # Configuration management
│   ├── database.py              # SQLAlchemy ORM setup
│   │
│   ├── models/
│   │   ├── db_models.py         # SQLAlchemy ORM models (Job, JobStatus)
│   │   └── schemas.py           # Pydantic validation schemas
│   │
│   ├── routers/
│   │   └── jobs.py              # REST API endpoints (/jobs/*)
│   │
│   ├── services/
│   │   ├── job_service.py       # Job CRUD and state management
│   │   └── mock_data_service.py # Synthetic data generation
│   │
│   ├── background_tasks/
│   │   └── job_scheduler.py     # Async state machine executor
│   │
│   └── mock_data/
│       └── sample_results/      # Generated output files
│
├── scripts/
│   ├── init_db.py               # Initialize DB with sample jobs
│   └── generate_sample_data.py  # Generate standalone mock files
│
├── tests/
│   └── test_endpoints.py        # pytest test suite
│
├── requirements.txt             # Dependencies
├── .env.example                 # Environment variables template
├── .gitignore                   # Git ignore rules
├── README.md                    # Full documentation
├── quickstart.sh                # One-click setup
└── example_job.json             # Sample job submission
```

---

## 🔌 API Endpoints Quick Reference

| Method | Endpoint | Purpose |
|--------|----------|---------|
| `POST` | `/jobs/submit` | Submit new job for processing |
| `GET` | `/jobs/{job_id}/status` | Get job status and metadata |
| `GET` | `/jobs/{job_id}/outputs` | Get results (only if COMPLETED) |
| `GET` | `/jobs/{job_id}/accounting` | Get resource usage stats |
| `GET` | `/jobs/` | List all jobs (pagination supported) |
| `GET` | `/health` | Health check |
| `GET` | `/` | API info and endpoints |

---

## 📝 Typical Job Lifecycle

### Timeline (with default settings)
```
T=0s:    User submits job → Status: PENDING
T=5s:    Scheduler updates → Status: RUNNING (PENDING_TO_RUNNING_DELAY=5)
T=15s:   Scheduler updates → Status: COMPLETED (RUNNING_TO_COMPLETED_DELAY=10)
```

### State Transitions Explained
```
PENDING   Job waiting for resources (immediately after submission)
    ↓     [after PENDING_TO_RUNNING_DELAY seconds]
RUNNING   Job actively executing in container
    ↓     [after RUNNING_TO_COMPLETED_DELAY seconds]
COMPLETED Results ready for retrieval
```

---

## 🧪 Testing the API

### Via Swagger UI (Recommended)
```
http://localhost:8000/docs
```
- Interactive web interface
- Try endpoints with built-in forms
- View request/response examples

### Via Command Line (cURL)

**1. Submit a job:**
```bash
curl -X POST http://localhost:8000/jobs/submit \
  -H "Content-Type: application/json" \
  -d @example_job.json
```

Output:
```json
{
  "job_id": "job_a1b2c3d4e5f6",
  "status": "PENDING",
  "message": "Job submitted successfully"
}
```

**2. Check status immediately:**
```bash
JOB_ID="job_a1b2c3d4e5f6"
curl http://localhost:8000/jobs/$JOB_ID/status | jq .
```

Expected response:
```json
{
  "job_id": "job_a1b2c3d4e5f6",
  "status": "PENDING",
  "created_at": "2024-03-17T10:30:45.123456",
  "started_at": null,
  "completed_at": null,
  ...
}
```

**3. Wait and check again (after ~10 seconds):**
```bash
curl http://localhost:8000/jobs/$JOB_ID/status | jq .status
```

Status will progress: `PENDING` → `RUNNING` → `COMPLETED`

**4. Get outputs (only when COMPLETED):**
```bash
curl http://localhost:8000/jobs/$JOB_ID/outputs | jq .structural_data
```

Returns:
```json
{
  "pdb_file": "HEADER    SIMULATED...",
  "cif_file": "data_simulated_structure...",
  "confidence": {
    "plddt_per_residue": [75.2, 80.1, ...],
    "plddt_mean": 75.8,
    "pae_matrix": [[0.5, 1.2, ...], ...]
  }
}
```

### Via Python

```python
import requests
import time

BASE_URL = "http://localhost:8000"

# Submit
job = requests.post(
    f"{BASE_URL}/jobs/submit",
    json={
        "fasta_sequence": ">protein\\nMKFSMVQVS",
        "fasta_filename": "seq.fasta",
        "gpus": 1,
        "cpus": 8,
        "memory_gb": 32.0
    }
).json()

job_id = job["job_id"]
print(f"Submitted: {job_id}")

# Poll until complete
while True:
    status = requests.get(f"{BASE_URL}/jobs/{job_id}/status").json()
    print(f"Status: {status['status']}")
    
    if status['status'] == 'COMPLETED':
        break
    time.sleep(2)

# Get results
outputs = requests.get(f"{BASE_URL}/jobs/{job_id}/outputs").json()
plddt = outputs['structural_data']['confidence']['plddt_mean']
print(f"Mean confidence (pLDDT): {plddt:.1f}")
```

---

## ⚙️ Configuration Guide

### Environment Variables (.env)

```ini
# ===== DATABASE =====
DATABASE_URL=sqlite:///./cesga_simulator.db
# For PostgreSQL: postgresql://user:password@localhost:5432/dbname

# ===== APPLICATION =====
DEBUG=True                          # Enable debug mode
LOG_LEVEL=INFO                      # DEBUG, INFO, WARNING, ERROR

# ===== JOB SCHEDULING (seconds) =====
PENDING_TO_RUNNING_DELAY=5          # Wait time before job starts
RUNNING_TO_COMPLETED_DELAY=10       # Simulated execution time

# ===== HARDWARE LIMITS =====
MAX_GPUS_PER_JOB=4                  # Max GPUs per job
MAX_CPUS_PER_JOB=64                 # Max CPUs per job
MAX_MEMORY_GB=256                   # Max memory per job

# ===== API =====
API_TITLE=CESGA Supercomputer Simulator
API_VERSION=1.0.0
```

### Key Settings Explained

| Setting | Effect | Typical Value |
|---------|--------|---------------|
| `PENDING_TO_RUNNING_DELAY` | How long job waits before executing | 5-10 seconds |
| `RUNNING_TO_COMPLETED_DELAY` | Simulated computation time | 10-60 seconds |
| `MAX_GPUS_PER_JOB` | Validation limit for GPU requests | 1-4 |
| `DATABASE_URL` | Where jobs are stored | SQLite (easy) or PostgreSQL (production) |

---

## 🔍 Output Data Explained

### Confidence Scores (structural_data.confidence)

```json
{
  "plddt_per_residue": [75.2, 80.1, 82.3, ...],  // Confidence per amino acid
  "plddt_mean": 75.8,                             // Average confidence
  "plddt_histogram": {                            // Distribution
    "very_high": 23,    // > 90
    "high": 45,         // 70-90
    "medium": 18,       // 50-70
    "low": 14           // < 50
  },
  "pae_matrix": [[0.5, 1.2, ...], ...],          // Aligned error matrix
  "mean_pae": 3.2                                 // Avg prediction error
}
```

**Interpretation:**
- **pLDDT > 90**: Very confident prediction (blue in visualizers)
- **pLDDT 70-90**: Confident (cyan)
- **pLDDT 50-70**: Medium confidence (yellow)
- **pLDDT < 50**: Low confidence (red)
- **PAE**: Lower values mean better predictions

### Biological Properties (biological_data)

```json
{
  "solubility_score": 72.5,           // 0-100, higher = more soluble
  "solubility_prediction": "soluble",  // "soluble" or "poorly soluble"
  "instability_index": 35.2,           // Protein stability metric
  "stability_status": "stable",        // "stable" or "unstable"
  "toxicity_alerts": [],               // Potential toxic motifs
  "allergenicity_alerts": []           // Potential allergen sequences
}
```

### Resource Accounting (accounting)

```json
{
  "cpu_hours": 6.8,                  // Total CPU-hours used
  "gpu_hours": 2.3,                  // Total GPU-hours (if applicable)
  "memory_gb_hours": 128.0,          // Memory-hours
  "total_wall_time_seconds": 1500,   // Total elapsed time
  "cpu_efficiency_percent": 85.5,    // CPU utilization %
  "memory_efficiency_percent": 92.1  // Memory utilization %
}
```

---

## 🛠️ Common Tasks

### Change Job State Timing

Edit `.env`:
```ini
PENDING_TO_RUNNING_DELAY=2       # Jobs start sooner
RUNNING_TO_COMPLETED_DELAY=30    # Longer computation simulation
```

Then restart API:
```bash
python -m uvicorn app.main:app --reload
```

### Add Pre-computed Test Data

```bash
python scripts/generate_sample_data.py
```

This creates mock files in `app/mock_data/` directory.

### Generate Fresh Database with Samples

```bash
# Delete old database
rm cesga_simulator.db

# Initialize with new samples
python scripts/init_db.py
```

### Query Database Directly

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.db_models import Job

engine = create_engine("sqlite:///cesga_simulator.db")
Session = sessionmaker(bind=engine)
db = Session()

# List all jobs
for job in db.query(Job).all():
    print(f"{job.id}: {job.status}")

db.close()
```

### Run Tests

```bash
pip install pytest
pytest tests/test_endpoints.py -v
```

---

## 🎯 Integration with Hackathon Frontend

### CORS is Enabled ✅

The API allows requests from any origin:
```python
# In app/main.py
CORSMiddleware(allow_origins=["*"])
```

### JavaScript/Fetch Example

```javascript
// Submit job
const jobData = {
  fasta_sequence: ">protein\nMKFSMVQVS...",
  fasta_filename: "seq.fasta",
  gpus: 1,
  cpus: 8,
  memory_gb: 32.0
};

const submitResponse = await fetch('/jobs/submit', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(jobData)
});

const { job_id } = await submitResponse.json();

// Poll for results
while (true) {
  const statusRes = await fetch(`/jobs/${job_id}/status`);
  const { status } = await statusRes.json();
  
  if (status === 'COMPLETED') {
    const outputRes = await fetch(`/jobs/${job_id}/outputs`);
    const outputs = await outputRes.json();
    // Use outputs in visualizer (Mol*, ChimeraX, etc.)
    break;
  }
  
  await new Promise(resolve => setTimeout(resolve, 2000));
}
```

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| Port 8000 already in use | Use different port: `--port 8001` |
| Database locked | Delete `*.db` files and reinitialize |
| State transitions not working | Check log level is INFO, verify delay settings |
| CORS errors in frontend | CORS is enabled by default for all origins |
| Import errors | Ensure venv is activated: `source venv/bin/activate` |
| Jobs never complete | Check `RUNNING_TO_COMPLETED_DELAY` value |

---

## 📚 Documentation Links

- **Full README**: [README.md](README.md)
- **API OpenAPI Schema**: http://localhost:8000/openapi.json
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 💡 Tips & Tricks

1. **Real-time Development**: Use `--reload` flag for auto-restart on file changes
2. **Faster Testing**: Set delays to 1-2 seconds in `.env`
3. **Data Inspection**: Use `app/mock_data/sample_results/{job_id}/` to view generated files
4. **Logging**: Set `LOG_LEVEL=DEBUG` for detailed trace information
5. **Database Browser**: Open `.db` with "DB Browser for SQLite" for graphical inspection

---

Made with ❤️ for bioinformatics hackathons. Happy computing! 🧬🚀
