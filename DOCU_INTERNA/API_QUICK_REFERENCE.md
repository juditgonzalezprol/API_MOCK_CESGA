# CESGA API - Quick Reference Sheet

## 🚀 Getting Started (30 seconds)

```bash
cd /Users/juditgonzalez/Desktop/API_CESGA
chmod +x quickstart.sh
./quickstart.sh
# Open: http://localhost:8000/docs
```

---

## 📍 API Base URL
```
http://localhost:8000
```

---

## 📚 Documentation
| Resource | URL |
|----------|-----|
| **Interactive Docs** | http://localhost:8000/docs |
| **Swagger JSON** | http://localhost:8000/openapi.json |
| **ReDoc** | http://localhost:8000/redoc |
| **Health Check** | http://localhost:8000/health |

---

## 🔐 Authentication
None (Open API for hackathon)

---

## 📤 API Endpoints

### 1. Submit Job
```bash
curl -X POST http://localhost:8000/jobs/submit \
  -H "Content-Type: application/json" \
  -d '{
    "fasta_sequence": ">my_protein\nMKVLSPADKTNV...",
    "fasta_filename": "protein.fasta",
    "gpus": 1,
    "cpus": 8,
    "memory_gb": 16,
    "max_runtime_seconds": 3600
  }'

# Response:
# {"job_id": "job_abc123def456", "status": "PENDING"}
```

**Parameters**:
- `fasta_sequence` (string, required) - FASTA format (must start with `>`)
- `fasta_filename` (string, required) - Filename for reference
- `gpus` (int, optional, default: 0) - Number of GPUs (0-4)
- `cpus` (int, optional, default: 1) - Number of CPU cores (1-64)
- `memory_gb` (float, optional, default: 8) - Memory in GB (0-256)
- `max_runtime_seconds` (int, optional, default: 3600) - Max runtime (60-86400)

**Status Codes**:
- `200` - Job submitted successfully
- `400` - Invalid request (FASTA format, resource limits)
- `422` - Validation error

---

### 2. Check Job Status
```bash
curl http://localhost:8000/jobs/{job_id}/status | jq .

# Example with sample job:
curl http://localhost:8000/jobs/sample_ubiquitin/status | jq .
```

**Response**:
```json
{
  "job_id": "job_abc123def456",
  "status": "PENDING",
  "created_at": "2024-03-17T10:30:05.123456",
  "started_at": null,
  "completed_at": null,
  "gpus": 1,
  "cpus": 8,
  "memory_gb": 16.0,
  "max_runtime_seconds": 3600,
  "fasta_filename": "protein.fasta",
  "error_message": null
}
```

**Status Values**:
- `PENDING` - In queue, waiting to run
- `RUNNING` - Currently executing
- `COMPLETED` - Finished successfully
- `FAILED` - Error occurred
- `CANCELLED` - Cancelled by user

---

### 3. Get Job Outputs (Completed Jobs Only)
```bash
curl http://localhost:8000/jobs/{job_id}/outputs | jq .

# Example:
curl http://localhost:8000/jobs/sample_ubiquitin/outputs | jq .
```

**Response** (when COMPLETED):
```json
{
  "job_id": "job_abc123def456",
  "status": "COMPLETED",
  "protein_metadata": {
    "protein_name": "ubiquitin",
    "uniprot_id": "P0CG47",
    "pdb_id": "1UBQ",
    "match_type": "exact_match",
    "aa_count": 76,
    "molecular_weight_da": 8565,
    "data_source": "UniProt real sequence"
  },
  "structural_data": {
    "pdb_file": "HEADER...",
    "cif_file": "data_simulated...",
    "confidence": {
      "plddt_per_residue": [75.2, 80.1, 82.3, ...],
      "plddt_mean": 75.8,
      "plddt_histogram": {
        "very_high": 24,
        "high": 32,
        "medium": 15,
        "low": 5
      },
      "pae_matrix": [[0.5, 1.2, 0.8, ...], ...],
      "mean_pae": 3.2
    }
  },
  "biological_data": {
    "solubility_score": 78.5,
    "solubility_prediction": "soluble",
    "instability_index": 29.4,
    "stability_prediction": "stable",
    "alerts": [],
    "secondary_structure": {
      "alpha_helix_percent": 45.3,
      "beta_strand_percent": 22.1,
      "coil_percent": 32.6
    }
  },
  "logs": "[2024-03-17 10:30:05] Job started in Apptainer container...",
  "accounting": {
    "cpu_hours": 0.034,
    "gpu_hours": 0.017,
    "memory_gb_hours": 0.42,
    "total_wall_time_seconds": 15
  }
}
```

---

### 4. Get Job Accounting
```bash
curl http://localhost:8000/jobs/{job_id}/accounting | jq .
```

**Response**:
```json
{
  "job_id": "job_abc123def456",
  "status": "COMPLETED",
  "accounting": {
    "cpu_hours": 0.068,
    "gpu_hours": 0.034,
    "memory_gb_hours": 0.42,
    "total_wall_time_seconds": 30,
    "cpu_efficiency_percent": 85.5,
    "memory_efficiency_percent": 92.1,
    "gpu_efficiency_percent": 78.3
  }
}
```

---

### 5. List All Jobs
```bash
curl http://localhost:8000/jobs | jq .
```

**Response**:
```json
{
  "jobs": [
    {
      "job_id": "sample_ubiquitin",
      "status": "COMPLETED",
      "created_at": "2024-03-17T10:00:00",
      "fasta_filename": "ubiquitin.fasta"
    },
    ...
  ],
  "total": 4
}
```

---

### 6. Get Sample Results
```bash
curl http://localhost:8000/sample_results | jq .
```

Returns list of pre-computed sample jobs with their complete outputs.

---

### 7. Health Check
```bash
curl http://localhost:8000/health | jq .

# Response:
# {"status": "ok", "timestamp": "2024-03-17T10:30:05"}
```

---

## 💾 Built-in Sample Jobs

Pre-created jobs with real protein data (all COMPLETED):

| Job ID | Protein | Aa | UniProt | PDB |
|--------|---------|-----|---------|-----|
| `sample_ubiquitin` | Ubiquitin | 76 | P0CG47 | 1UBQ |
| `sample_insulin` | Insulin | 21 | P01308 | 4MIF |
| `sample_hemoglobin_alpha` | Hemoglobin Alpha | 63 | P69905 | 1A3N |
| `sample_lysozyme` | Lysozyme | 130 | P61626 | 1LYZ |

Try immediately:
```bash
curl http://localhost:8000/jobs/sample_ubiquitin/outputs | jq '.protein_metadata'
```

---

## 🧬 Real Proteins Available for Auto-Detection

If you submit these sequences, they will be auto-detected and real properties used:

1. **Ubiquitin** (76 aa) - `P0CG47`
2. **Insulin** (21 aa) - `P01308`
3. **Hemoglobin Alpha** (63 aa) - `P69905`
4. **Lysozyme** (130 aa) - `P61626`
5. **Alpha-Amylase** (496 aa) - `P04746`
6. **Myoglobin** (153 aa) - `P02144`

---

## ⏱️ Job Lifecycle Timing

**Default Timeline** (can be configured via `.env`):

```
T=0s    → Job submitted (status: PENDING)
T=5s    → Job starts running (status: RUNNING)
T=15s   → Job completes (status: COMPLETED)
T=15s+  → Outputs available via GET /jobs/{id}/outputs
```

---

## 🔄 Example Workflow

### Step 1: Submit Job
```bash
RESPONSE=$(curl -s -X POST http://localhost:8000/jobs/submit \
  -H "Content-Type: application/json" \
  -d '{
    "fasta_sequence": ">test_protein\nMKVLSPADKTNVKAAAAVDVWFEASPMFRAVFDAAKVVMVQVSKLS",
    "fasta_filename": "test.fasta",
    "gpus": 1,
    "cpus": 4,
    "memory_gb": 8,
    "max_runtime_seconds": 1800
  }')

JOB_ID=$(echo $RESPONSE | jq -r '.job_id')
echo "Job ID: $JOB_ID"
```

### Step 2: Poll Status
```bash
while true; do
  STATUS=$(curl -s http://localhost:8000/jobs/$JOB_ID/status | jq -r '.status')
  echo "Status: $STATUS"
  
  if [ "$STATUS" == "COMPLETED" ]; then
    echo "Job completed!"
    break
  fi
  
  sleep 2
done
```

### Step 3: Get Results
```bash
curl -s http://localhost:8000/jobs/$JOB_ID/outputs | jq '.protein_metadata'
curl -s http://localhost:8000/jobs/$JOB_ID/outputs | jq '.biological_data.solubility_score'
curl -s http://localhost:8000/jobs/$JOB_ID/accounting | jq '.accounting.cpu_hours'
```

---

## 🛠️ Configuration Options (.env)

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
# Or PostgreSQL:
# DATABASE_URL=postgresql://user:password@localhost/cesga_db

# Logging
LOG_LEVEL=INFO
DEBUG=False
```

---

## ❌ Error Responses

### 400 - Bad Request (Invalid FASTA)
```json
{
  "detail": "FASTA sequence must start with '>'"
}
```

### 400 - Resource Limits Exceeded
```json
{
  "detail": "Maximum GPUs per job: 4"
}
```

### 404 - Job Not Found
```json
{
  "detail": "Job not found"
}
```

### 400 - Outputs Not Available Yet
```json
{
  "detail": "Outputs only available for COMPLETED jobs"
}
```

---

## 📊 Data Types

### Solubility Score
- **0-100** scale
- `0-33`: poorly soluble
- `34-66`: moderately soluble
- `67-100`: soluble

### Instability Index
- **0-100** scale
- `<40`: stable
- `≥40`: unstable

### pLDDT (per residue confidence)
- **0-100** scale
- `90-100`: very high confidence
- `70-90`: high confidence
- `50-70`: medium confidence
- `<50`: low confidence

### PAE (Predicted Aligned Error)
- Angströms (Å)
- `<5`: very good alignment
- `5-10`: good alignment
- `>10`: poor alignment

---

## 🧪 Quick Tests

### Test 1: Sample Job Status
```bash
curl http://localhost:8000/jobs/sample_ubiquitin/status | jq '.status'
# Expected: COMPLETED
```

### Test 2: Real Protein Detection
```bash
curl http://localhost:8000/jobs/sample_ubiquitin/outputs | jq '.protein_metadata.uniprot_id'
# Expected: P0CG47
```

### Test 3: Biological Properties
```bash
curl http://localhost:8000/jobs/sample_ubiquitin/outputs | jq '.biological_data.solubility_score'
# Expected: 78.5
```

### Test 4: Structure File Exists
```bash
curl http://localhost:8000/jobs/sample_ubiquitin/outputs | jq '.structural_data.pdb_file | length'
# Expected: (large number >100)
```

### Test 5: Submit New Job
```bash
curl -X POST http://localhost:8000/jobs/submit \
  -H "Content-Type: application/json" \
  -d '{"fasta_sequence":">test\nMKVLS","fasta_filename":"test.fasta","gpus":0,"cpus":1,"memory_gb":1}' \
  | jq '.job_id'
# Expected: job_* (some ID)
```

---

## 🎯 Real Proteins Quick Submit

### Ubiquitin (76 aa)
```bash
curl -X POST http://localhost:8000/jobs/submit \
  -H "Content-Type: application/json" \
  -d '{
    "fasta_sequence": ">ubiquitin_real\nMQIFVKTLTGKTITLEVEPSDTIEN\nVKAKIQDKEGIPPDQQRLIFAGKQLEDGRTLS\nDYNIQKESTLHLVL",
    "fasta_filename": "ubiquitin.fasta",
    "gpus": 1,
    "cpus": 4,
    "memory_gb": 8
  }' | jq -r '.job_id'
```

---

## 🌐 Frontend Integration

### CORS Headers
✅ Already enabled - can call from browser JavaScript

### Example: JavaScript Fetch
```javascript
fetch('http://localhost:8000/jobs/submit', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    fasta_sequence: '>protein\nMKVLS...',
    fasta_filename: 'protein.fasta',
    gpus: 1,
    cpus: 4,
    memory_gb: 8
  })
})
.then(r => r.json())
.then(d => console.log('Job ID:', d.job_id))
```

---

## 🔍 Debugging Tips

### Enable Debug Mode
```bash
# Set in .env
DEBUG=True
LOG_LEVEL=DEBUG

# Restart server
```

### Check Database
```bash
sqlite3 cesga_simulator.db "SELECT job_id, status, created_at FROM jobs LIMIT 5;"
```

### Monitor Server Logs
```bash
# If running with:
python -m uvicorn app.main:app --reload --log-level debug
```

### Clear Database & Restart
```bash
rm cesga_simulator.db
python scripts/init_db_real_proteins.py
python -m uvicorn app.main:app --reload
```

---

## 📞 Common Questions

**Q: How long does a job take?**  
A: Default ~15 seconds (5s queue + 10s execution). Configurable.

**Q: Are the results real?**  
A: Hybrid - real for known proteins, synthetic for unknown. See `protein_metadata.data_source`.

**Q: Can I use PostgreSQL?**  
A: Yes - set `DATABASE_URL=postgresql://...` in `.env`

**Q: How many jobs can I submit?**  
A: Limited only by disk space (SQLite) or database size (PostgreSQL)

---

## 🎓 Commands Reference

```bash
# Start API
./quickstart.sh

# Or manual:
source venv/bin/activate
python -m uvicorn app.main:app --reload

# Initialize with real proteins
python scripts/init_db_real_proteins.py

# Generate PDB files
python scripts/generate_precomputed_structures.py

# Run tests
pytest tests/ -v

# Run integration test
bash tests/integration_real_proteins.sh

# View Swagger docs
open http://localhost:8000/docs

# Check database
sqlite3 cesga_simulator.db "SELECT * FROM jobs;"
```

---

## ✅ Verification Checklist

- [ ] `./quickstart.sh` completed successfully
- [ ] API running on http://localhost:8000
- [ ] Swagger UI accessible at http://localhost:8000/docs
- [ ] Sample jobs exist: `/jobs/sample_ubiquitin/status` returns COMPLETED
- [ ] New job submission works: POST /jobs/submit
- [ ] Job transitions: PENDING → RUNNING → COMPLETED
- [ ] Outputs available: `/jobs/{id}/outputs` (when COMPLETED)
- [ ] Real protein detected: protein_metadata shows UniProt ID
- [ ] All 4 sample jobs exist and accessible

---

**Quick Reference Version**: 1.0  
**Last Updated**: March 17, 2024

---

**[← Back to Documentation](DOCUMENTATION_INDEX.md)** | **[← Main README](README.md)**
