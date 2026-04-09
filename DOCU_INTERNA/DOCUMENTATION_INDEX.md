# CESGA API Simulator - Complete Documentation Index

## 🗂️ Project Structure Overview

```
/Users/juditgonzalez/Desktop/API_CESGA/
│
├── 📘 DOCUMENTATION
│   ├── EXECUTIVE_SUMMARY.md          ← START HERE (Overview of everything)
│   ├── README.md                     ← First time? Read this
│   ├── QUICKSTART.md                 ← Get running in 60 seconds
│   ├── SPECIFICATIONS.md             ← Complete requirement mapping
│   ├── ARCHITECTURE.md               ← System design & internals
│   ├── PROJECT_SUMMARY.md            ← Project overview
│   ├── TESTING_REAL_PROTEINS.md      ← Verification guide (15 tests)
│   └── DOCUMENTATION_INDEX.md        ← This file
│
├── 🔧 QUICK START
│   ├── quickstart.sh                 ← One command to start (with real proteins)
│   └── requirements.txt              ← Python dependencies
│
├── 📱 APPLICATION CODE
│   ├── app/
│   │   ├── main.py                   ← FastAPI app entry point
│   │   ├── models/                   ← Pydantic data models
│   │   │   ├── job.py
│   │   │   ├── request.py
│   │   │   ├── response.py
│   │   │   └── error.py
│   │   ├── routers/
│   │   │   └── jobs.py               ← 7 REST endpoints
│   │   ├── services/
│   │   │   ├── real_protein_database.py   ← [NEW] 6 real proteins
│   │   │   ├── mock_data_service.py       ← [ENHANCED] Real/synthetic hybrid
│   │   │   ├── job_service.py             ← [ENHANCED] Protein identification
│   │   │   ├── database_service.py
│   │   │   ├── validation_service.py
│   │   │   └── ... (+ 5 more)
│   │   ├── background_tasks/
│   │   │   └── job_scheduler.py     ← Async job state machine
│   │   ├── config/
│   │   │   └── settings.py          ← Environment configuration
│   │   └── utils/
│   │       └── ... (Utility functions)
│   │
│   └── .env                          ← Configuration (can be customized)
│
├── 🧬 DATA & SCRIPTS
│   ├── scripts/
│   │   ├── init_db.py               ← Basic initialization
│   │   ├── init_db_real_proteins.py ← [NEW] Init with 6 real proteins
│   │   ├── generate_precomputed_structures.py ← [NEW] Generate PDB files
│   │   └── ... (+ 2 more utilities)
│   │
│   ├── app/mock_data/
│   │   ├── precomputed/             ← Real PDB structure files
│   │   │   ├── ubiquitin.pdb
│   │   │   ├── hemoglobin_alpha.pdb
│   │   │   └── lysozyme.pdb
│   │   │
│   │   └── sample_results/          ← Per-job output bundles
│   │       ├── sample_ubiquitin/
│   │       ├── sample_insulin/
│   │       ├── sample_hemoglobin_alpha/
│   │       └── sample_lysozyme/
│   │
│   └── cesga_simulator.db           ← SQLite database (created at runtime)
│
├── 🧪 TESTING
│   ├── tests/
│   │   ├── test_models.py
│   │   ├── test_services.py
│   │   ├── test_endpoints.py
│   │   ├── test_real_proteins.py    ← [NEW] Real protein tests
│   │   └── integration_real_proteins.sh ← [NEW] End-to-end test
│   │
│   └── TESTING_REAL_PROTEINS.md     ← 15 step-by-step verification tests
│
└── 📦 CONFIG FILES
    ├── requirements.txt             ← pip install list
    ├── .gitignore
    ├── .env.example
    └── pyproject.toml
```

---

## 📚 Documentation Guide

### For Different Users

#### 👤 **First Time?** → Start Here
1. Read: [README.md](README.md)
2. Run: `./quickstart.sh`
3. Visit: http://localhost:8000/docs
4. Read: [QUICKSTART.md](QUICKSTART.md)

#### 🏗️ **Need Architecture Details?**
1. Read: [ARCHITECTURE.md](ARCHITECTURE.md) - System design
2. Read: [SPECIFICATIONS.md](SPECIFICATIONS.md) - Requirements mapping
3. Check: `app/services/` - Service layer code
4. Check: `app/routers/jobs.py` - API endpoints

#### 🧬 **Want to Understand Real Protein Integration?**
1. Read: [EXECUTIVE_SUMMARY.md](EXECUTIVE_SUMMARY.md) - Overview
2. Check: `app/services/real_protein_database.py` - Real proteins
3. Check: `app/services/mock_data_service.py` - Data generation
4. Check: `scripts/init_db_real_proteins.py` - Sample data
5. Read: [TESTING_REAL_PROTEINS.md](TESTING_REAL_PROTEINS.md) - Verification

#### ✅ **Need to Verify Everything Works?**
1. Read: [TESTING_REAL_PROTEINS.md](TESTING_REAL_PROTEINS.md)
2. Execute: Section 2.1-2.6 (API tests)
3. Run: `bash tests/integration_real_proteins.sh`
4. Check: All tests pass

#### 🔧 **Customizing Configuration?**
1. Edit: `.env` file
2. Available settings:
   - `PENDING_TO_RUNNING_DELAY=5` (queue time)
   - `RUNNING_TO_COMPLETED_DELAY=10` (exec time)
   - `MAX_GPUS_PER_JOB=4`
   - `MAX_CPUS_PER_JOB=64`
   - `MAX_MEMORY_GB=256`
   - `DATABASE_URL=sqlite:///./cesga_simulator.db`

#### 🚀 **Production Deployment?**
1. Read: [ARCHITECTURE.md](ARCHITECTURE.md) - System design
2. Configure: `.env` with production settings
3. Use: `DATABASE_URL=postgresql://...` for PostgreSQL
4. Deploy: Uvicorn + reverse proxy (nginx/Apache)

---

## 📖 Documentation Files

### EXECUTIVE_SUMMARY.md
**Purpose**: High-level overview of everything  
**Best for**: Understanding what was built  
**Contains**:
- Project status (✅ 100% complete)
- Technical implementation overview
- Phase 1 & 2 deliverables
- Biological data features
- Compliance matrix
- Quick start
- Requirements fulfillment

### README.md
**Purpose**: Getting started guide  
**Best for**: First-time setup  
**Contains**:
- Installation instructions
- How to start the server
- Basic API examples
- Endpoint overview
- Project structure

### QUICKSTART.md
**Purpose**: Ultra-fast setup (60 seconds)  
**Best for**: Impatient users  
**Contains**:
- Prerequisites check
- One-command setup
- First API call
- Links to docs

### ARCHITECTURE.md
**Purpose**: System design & internals  
**Best for**: Developers extending the API  
**Contains**:
- Component diagram
- Service layer design
- Data flow
- Background scheduler details
- Database schema
- Extension points

### SPECIFICATIONS.md
**Purpose**: Complete requirement mapping  
**Best for**: Verifying compliance  
**Contains**:
- All specification requirements
- Implementation details for each endpoint
- Conformance checklist
- Input/output flow
- Configuration options
- Real protein database info

### TESTING_REAL_PROTEINS.md
**Purpose**: Verification & testing guide  
**Best for**: Confirming everything works  
**Contains**:
- 5-step initialization verification
- 6 API test categories
- 15+ individual test cases
- Example curl commands
- Expected outputs
- Integration test script
- Stress test scenarios

### PROJECT_SUMMARY.md
**Purpose**: Project overview  
**Best for**: Understanding the project at a glance  
**Contains**:
- High-level summary
- Tech stack
- Key features
- File structure
- Endpoints overview

---

## 🔑 Key Code Files

### Core Application
- **[app/main.py](app/main.py)**
  - FastAPI app initialization
  - CORS configuration
  - Route registration
  - 🔍 Look here for: App setup, middleware

- **[app/routers/jobs.py](app/routers/jobs.py)**
  - All 7 REST endpoints:
    - POST /jobs/submit
    - GET /jobs/{id}/status
    - GET /jobs/{id}/outputs
    - GET /jobs/{id}/accounting
    - GET /jobs (list all)
    - GET /health
    - GET /sample_results
  - 🔍 Look here for: API endpoint implementation

### Services (Business Logic)
- **[app/services/real_protein_database.py](app/services/real_protein_database.py)** 🆕
  - 6 real proteins from UniProt
  - Pre-calculated properties
  - Lookup functions
  - 🔍 Look here for: Real protein data

- **[app/services/mock_data_service.py](app/services/mock_data_service.py)** (ENHANCED)
  - Generates AlphaFold2-like predictions
  - Real data lookup
  - Synthetic fallback
  - 🔍 Look here for: Biological data generation

- **[app/services/job_service.py](app/services/job_service.py)** (ENHANCED)
  - Job CRUD operations
  - State transitions
  - Protein identification
  - Output generation
  - 🔍 Look here for: Job lifecycle management

- **[app/services/database_service.py](app/services/database_service.py)**
  - SQLAlchemy ORM layer
  - Database queries
  - 🔍 Look here for: Database operations

- **[app/services/validation_service.py](app/services/validation_service.py)**
  - FASTA format validation
  - Resource limit checking
  - 🔍 Look here for: Input validation

### Background Tasks
- **[app/background_tasks/job_scheduler.py](app/background_tasks/job_scheduler.py)**
  - Async job state machine
  - PENDING → RUNNING → COMPLETED transitions
  - 🔍 Look here for: Background job scheduling

### Configuration
- **[app/config/settings.py](app/config/settings.py)**
  - Environment variables
  - Default configuration
  - 🔍 Look here for: Customizable parameters

### Scripts
- **[scripts/init_db_real_proteins.py](scripts/init_db_real_proteins.py)** 🆕
  - Initializes database with 4 real protein sample jobs
  - Generates output bundles
  - 🔍 Look here for: Sample data setup

- **[scripts/generate_precomputed_structures.py](scripts/generate_precomputed_structures.py)** 🆕
  - Generates PDB coordinate files
  - Pre-computes structures
  - 🔍 Look here for: Structure file generation

---

## 🧪 Testing Files

### Test Modules
- **[tests/test_models.py](tests/test_models.py)**
  - Pydantic model validation tests

- **[tests/test_services.py](tests/test_services.py)**
  - Service layer unit tests

- **[tests/test_endpoints.py](tests/test_endpoints.py)**
  - API endpoint integration tests

- **[tests/test_real_proteins.py](tests/test_real_proteins.py)** 🆕
  - Real protein database tests
  - Protein identification tests

### Test Scripts
- **[tests/integration_real_proteins.sh](tests/integration_real_proteins.sh)** 🆕
  - End-to-end integration test
  - Full workflow verification
  - 10-step completion test

### Running Tests
```bash
# Run all tests
pytest tests/ -v

# Run only real protein tests
pytest tests/test_real_proteins.py -v

# Run integration test
bash tests/integration_real_proteins.sh
```

---

## 🎯 Common Tasks

### Task: Start API with Real Proteins
```bash
./quickstart.sh
# Automatically:
# 1. Creates venv
# 2. Installs dependencies
# 3. Initializes DB with 4 real proteins
# 4. Generates PDB files
# 5. Starts API on http://localhost:8000
```

### Task: Submit a New Job
```bash
curl -X POST http://localhost:8000/jobs/submit \
  -H "Content-Type: application/json" \
  -d '{
    "fasta_sequence": ">protein\nMKVLS...",
    "fasta_filename": "protein.fasta",
    "gpus": 1,
    "cpus": 8,
    "memory_gb": 16,
    "max_runtime_seconds": 3600
  }'
```

### Task: Check Job Status
```bash
curl http://localhost:8000/jobs/{job_id}/status | jq .
```

### Task: Get Completed Job Outputs
```bash
curl http://localhost:8000/jobs/{job_id}/outputs | jq .
```

### Task: View Sample Results
```bash
curl http://localhost:8000/sample_results | jq .
```

### Task: Customize Timing
Edit `.env`:
```ini
PENDING_TO_RUNNING_DELAY=5      # How long job waits in queue
RUNNING_TO_COMPLETED_DELAY=10   # How long job execution takes
```

### Task: Use PostgreSQL (Production)
Edit `.env`:
```ini
DATABASE_URL=postgresql://user:password@localhost/cesga_db
```

### Task: Add More Real Proteins
Edit `app/services/real_protein_database.py` and add to `REAL_PROTEINS_DATABASE` dict:
```python
'your_protein': {
    'sequence': 'MKVLS...',
    'uniprot_id': 'P12345',
    'pdb_id': '1ABC',
    'molecular_weight_da': 50000,
    # ... other properties
}
```

---

## 🔍 Finding Things

### "I want to find..."

| What | Where |
|------|-------|
| REST API endpoints | `app/routers/jobs.py` |
| Real protein sequences | `app/services/real_protein_database.py` |
| How jobs transition states | `app/background_tasks/job_scheduler.py` |
| Solubility prediction | `app/services/mock_data_service.py` |
| FASTA validation | `app/services/validation_service.py` |
| Database queries | `app/services/database_service.py` |
| Configuration options | `.env` or `app/config/settings.py` |
| Sample data setup | `scripts/init_db_real_proteins.py` |
| API documentation | http://localhost:8000/docs |
| Unit tests | `tests/test_*.py` |
| Integration tests | `tests/integration_real_proteins.sh` |

---

## 📊 Quick Statistics

| Metric | Count |
|--------|-------|
| Python source files | 16+ |
| API endpoints | 7 |
| Real proteins included | 6 |
| Sample jobs pre-created | 4 |
| Precomputed PDB files | 3 |
| Test files | 5 |
| Documentation files | 8 |
| Total lines of code | 2000+ |
| Lines of documentation | 3000+ |

---

## ✅ Verification Checklist

Use this to verify everything is working:

- [ ] Ran `./quickstart.sh` successfully
- [ ] API starts on http://localhost:8000
- [ ] Swagger UI accessible at http://localhost:8000/docs
- [ ] Sample ubiquitin job exists: `/jobs/sample_ubiquitin/status`
- [ ] Job transitions through states (PENDING → RUNNING → COMPLETED)
- [ ] Outputs are retrievable: `/jobs/sample_ubiquitin/outputs`
- [ ] Real protein metadata present in outputs
- [ ] Protein identified as "ubiquitin"
- [ ] UniProt ID is P0CG47
- [ ] Biological properties present (solubility, stability)
- [ ] Structure files present (PDB, mmCIF)
- [ ] Confidence data present (pLDDT, PAE)
- [ ] Logs are simulated (Apptainer output)
- [ ] Accounting data present

All checked? ✅ **API is fully functional with real protein integration!**

---

## 🆘 Troubleshooting

### Problem: Port 8000 already in use
```bash
# Kill existing process
lsof -i :8000 | grep LISTEN | awk '{print $2}' | xargs kill -9

# Or use different port
python -m uvicorn app.main:app --port 8001
```

### Problem: Database locked
```bash
# Remove and reinitialize
rm cesga_simulator.db
python scripts/init_db_real_proteins.py
```

### Problem: Missing dependencies
```bash
pip install -r requirements.txt
```

### Problem: Protein not identified
Check that the sequence exactly matches a known protein in `real_protein_database.py`

### Problem: Scores seem synthetic
This is expected - if protein is unknown, synthetic scores are generated based on sequence analysis.

---

## 📞 Support

For issues or questions:

1. **Check Documentation**: Start with [EXECUTIVE_SUMMARY.md](EXECUTIVE_SUMMARY.md)
2. **Review Tests**: See [TESTING_REAL_PROTEINS.md](TESTING_REAL_PROTEINS.md)
3. **Check API Docs**: http://localhost:8000/docs (interactive)
4. **Review Code**: Source code is well-commented

---

## 🎓 Learning Path

**Recommended reading order**:

1. **Overview** (5 min)
   - [README.md](README.md)

2. **Quick Start** (10 min)
   - [QUICKSTART.md](QUICKSTART.md)
   - Run `./quickstart.sh`

3. **Understanding** (20 min)
   - [EXECUTIVE_SUMMARY.md](EXECUTIVE_SUMMARY.md)
   - [ARCHITECTURE.md](ARCHITECTURE.md)

4. **Verification** (30 min)
   - [TESTING_REAL_PROTEINS.md](TESTING_REAL_PROTEINS.md)
   - Run tests

5. **Deep Dive** (60+ min)
   - [SPECIFICATIONS.md](SPECIFICATIONS.md)
   - Review source code
   - Customize as needed

---

**Total Time to Full Understanding**: ~2 hours

---

**Document Version**: 1.0  
**Last Updated**: March 17, 2024  
**Status**: ✅ COMPLETE
