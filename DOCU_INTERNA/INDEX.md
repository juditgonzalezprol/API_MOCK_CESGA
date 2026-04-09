# 📚 Project Navigation Index

Welcome to the CESGA Supercomputer Simulator API! This index helps you navigate all project files and documentation.

## 🗺️ Quick Navigation

### 🚀 Getting Started (START HERE!)
- **[QUICKSTART.md](QUICKSTART.md)** - 2-minute setup guide
  - Quick start commands
  - Installation steps
  - First API test
  
- **[quickstart.sh](quickstart.sh)** - One-click setup script
  ```bash
  chmod +x quickstart.sh && ./quickstart.sh
  ```

### 📖 Documentation
- **[README.md](README.md)** - Full documentation (400+ lines)
  - Overview and features
  - Architecture description
  - Complete API endpoint reference
  - Usage examples (cURL, Python, JavaScript)
  - Configuration guide
  - Troubleshooting

- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Technical architecture (500+ lines)
  - System diagram
  - Component descriptions
  - Data flow diagrams
  - Concurrency model
  - Performance characteristics
  - Security considerations
  - Deployment paths

- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Project completion checklist
  - Deliverables status
  - Technology stack
  - File structure
  - Configuration reference
  - Quick commands
  - Performance metrics

### 💻 Application Code

#### Entry Point & Configuration
- **[app/main.py](app/main.py)** - FastAPI application factory
  - Application creation with lifespan
  - CORS middleware setup
  - Router registration
  - Exception handling
  - Background task initialization
  
- **[app/config.py](app/config.py)** - Configuration management
  - Environment variable loading
  - Settings class with defaults
  - Database URL configuration
  - Job scheduling parameters
  - Hardware limits

- **[app/database.py](app/database.py)** - Database setup
  - SQLAlchemy engine creation
  - Session management
  - Async and sync session factories
  - Dependency injection

#### Data Models

- **[app/models/db_models.py](app/models/db_models.py)** - ORM Models
  - `Job` model with all fields
  - `JobStatus` enum (PENDING, RUNNING, COMPLETED, FAILED, CANCELLED)
  - Database schema definitions

- **[app/models/schemas.py](app/models/schemas.py)** - Pydantic Schemas
  - `JobSubmitRequest` - Input validation
  - `JobStatusResponse` - Status query response
  - `JobOutputsResponse` - Results with structures
  - `JobAccountingResponse` - Resource accounting
  - Supporting schemas for nested objects

#### API Endpoints

- **[app/routers/jobs.py](app/routers/jobs.py)** - REST API endpoints
  - `POST /jobs/submit` - Submit job
  - `GET /jobs/{id}/status` - Get status
  - `GET /jobs/{id}/outputs` - Get results
  - `GET /jobs/{id}/accounting` - Get accounting
  - `GET /jobs/` - List jobs
  - Comprehensive endpoint documentation

#### Business Logic

- **[app/services/job_service.py](app/services/job_service.py)** - Job management
  - `create_job()` - Job creation and DB insertion
  - `get_job()` - Job retrieval
  - `update_job_status()` - Status updates
  - `Mark_job_running()` - PENDING → RUNNING transition
  - `mark_job_completed()` - RUNNING → COMPLETED transition
  - `_generate_job_outputs()` - Output file generation
  - `get_job_outputs_dict()` - Load and parse outputs

- **[app/services/mock_data_service.py](app/services/mock_data_service.py)** - Synthetic data
  - `generate_confidence_data()` - pLDDT + PAE matrices
  - `generate_pdb_structure()` - PDB format file
  - `generate_mmcif_structure()` - mmCIF format file
  - `generate_biological_data()` - Solubility, toxicity, allergenicity
  - `generate_logs()` - Container output simulation
  - `generate_accounting_data()` - Resource usage stats

#### Background Tasks

- **[app/background_tasks/job_scheduler.py](app/background_tasks/job_scheduler.py)** - State machine
  - `JobScheduler` class with event loop
  - `process_pending_jobs()` - Check PENDING → RUNNING transitions
  - State transition logic every 1 second
  - Database session management

### 🧪 Testing

- **[tests/test_endpoints.py](tests/test_endpoints.py)** - Pytest test suite
  - Health check tests
  - Job submission tests
  - Status retrieval tests
  - Output retrieval tests
  - Validation error tests
  - List jobs tests

  **Run tests:**
  ```bash
  pytest tests/test_endpoints.py -v
  ```

### 🛠️ Utility Scripts

- **[scripts/init_db.py](scripts/init_db.py)** - Database initialization
  - Create tables
  - Generate 3 sample completed jobs
  - Pre-populate outputs for testing
  - Run once after installation
  
  ```bash
  python scripts/init_db.py
  ```

- **[scripts/generate_sample_data.py](scripts/generate_sample_data.py)** - Standalone data generation
  - Generate mock data files
  - Useful for testing data generation independently
  
  ```bash
  python scripts/generate_sample_data.py
  ```

### 📋 Configuration Files

- **[.env.example](.env.example)** - Environment variables template
  - Copy to `.env` and customize
  - Database URL
  - Logging settings
  - Job scheduling delays
  - Hardware limits

- **[requirements.txt](requirements.txt)** - Python dependencies
  - FastAPI, Uvicorn
  - SQLAlchemy, Pydantic
  - Python-dotenv
  - Pytest, httpx

- **[.gitignore](.gitignore)** - Git ignore rules
  - Python cache files
  - Virtual environments
  - Database files
  - IDE settings

### 📝 Examples & Templates

- **[example_job.json](example_job.json)** - Sample job submission
  - FASTA format sequence
  - Resource parameters
  - Ready to curl at API

  ```bash
  curl -X POST http://localhost:8000/jobs/submit \
    -H "Content-Type: application/json" \
    -d @example_job.json
  ```

---

## 📊 File Organization Tree

```
API_CESGA/
│
├── 📚 Documentation
│   ├── README.md                  ← START HERE FOR FULL DOCS
│   ├── QUICKSTART.md              ← 2-minute setup
│   ├── ARCHITECTURE.md            ← Technical details
│   ├── PROJECT_SUMMARY.md         ← Completion checklist
│   └── INDEX.md                   ← (This file)
│
├── 🚀 Startup
│   ├── quickstart.sh              ← One-click setup
│   └── example_job.json           ← Sample job
│
├── ⚙️ Configuration
│   ├── .env.example               ← Environment template
│   ├── .gitignore                 ← Git rules
│   └── requirements.txt           ← Dependencies
│
├── 📦 Application (app/)
│   ├── __init__.py
│   ├── main.py                    ← FastAPI entry point
│   ├── config.py                  ← Configuration
│   ├── database.py                ← Database setup
│   │
│   ├── models/
│   │   ├── db_models.py           ← SQLAlchemy ORM
│   │   └── schemas.py             ← Pydantic validation
│   │
│   ├── routers/
│   │   └── jobs.py                ← REST endpoints
│   │
│   ├── services/
│   │   ├── job_service.py         ← Job management
│   │   └── mock_data_service.py   ← Data generation
│   │
│   └── background_tasks/
│       └── job_scheduler.py       ← State machine
│
├── 🧪 Tests (tests/)
│   ├── __init__.py
│   └── test_endpoints.py          ← Pytest suite
│
└── 🛠️ Scripts (scripts/)
    ├── init_db.py                 ← DB initialization
    └── generate_sample_data.py    ← Data generation
```

---

## 🎯 Common Tasks

### For First-Time Users
1. Read: [QUICKSTART.md](QUICKSTART.md)
2. Run: `./quickstart.sh`
3. Start: `python -m uvicorn app.main:app --reload`
4. Visit: http://localhost:8000/docs

### For API Integration
1. Refer: [README.md](README.md) - API Reference section
2. Try: http://localhost:8000/docs (Swagger UI)
3. Example: [example_job.json](example_job.json)

### For Customization
1. Review: [ARCHITECTURE.md](ARCHITECTURE.md)
2. Edit: [app/config.py](app/config.py) or `.env`
3. Modify: [app/services/mock_data_service.py](app/services/mock_data_service.py)

### For Understanding Code
1. Start: [app/main.py](app/main.py) - entry point
2. Then: [app/routers/jobs.py](app/routers/jobs.py) - endpoints
3. Then: [app/services/](app/services/) - business logic

### For Database
1. Create: `python scripts/init_db.py`
2. Query: Use SQLite Browser or Python ORM
3. Reset: `rm cesga_simulator.db && python scripts/init_db.py`

### For Testing
1. Run: `pytest tests/test_endpoints.py -v`
2. Add tests: Edit [tests/test_endpoints.py](tests/test_endpoints.py)

---

## 🔗 External Resources

### FastAPI Documentation
- https://fastapi.tiangolo.com/
- https://fastapi.tiangolo.com/async-sql-databases/

### SQLAlchemy Documentation
- https://docs.sqlalchemy.org/
- https://docs.sqlalchemy.org/orm/quickstart.html

### Pydantic Documentation
- https://docs.pydantic.dev/

### AlphaFold2 Resources
- https://github.com/deepmind/alphafold
- https://www.nature.com/articles/s41586-021-03819-2

### Slurm Documentation
- https://slurm.schedmd.com/

---

## 📈 Project Statistics

| Metric | Value |
|--------|-------|
| Python files | 16 |
| Documentation files | 5 |
| Lines of code | ~2,000 |
| API endpoints | 7 |
| Database tables | 1 |
| Data models | 12+ |
| Test cases | 15+ |
| Configuration variables | 12 |

---

## ✅ Verification Checklist

- [✅] All source files created
- [✅] All documentation written
- [✅] Configuration templates provided
- [✅] Example data included
- [✅] Test suite included
- [✅] Initialization scripts provided
- [✅] Quick start guide created
- [✅] Architecture documented

---

## 📞 Support

For issues or questions:
1. Check [QUICKSTART.md](QUICKSTART.md) - Common issues section
2. Review [README.md](README.md) - Troubleshooting section
3. Check Swagger docs: http://localhost:8000/docs
4. Review terminal output for error messages

---

## 🎓 Learning Path

**Beginner** (Get it running):
1. [QUICKSTART.md](QUICKSTART.md)
2. Run `./quickstart.sh`
3. Try API in http://localhost:8000/docs

**Intermediate** (Understand how it works):
1. [README.md](README.md) - Full documentation
2. [app/main.py](app/main.py) - Entry point
3. [app/routers/jobs.py](app/routers/jobs.py) - Endpoints

**Advanced** (Customize and extend):
1. [ARCHITECTURE.md](ARCHITECTURE.md) - System design
2. All source files in [app/](app/)
3. [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Technical details

---

**Happy hacking!** 🧬🚀

For questions about the API, visit the interactive documentation at:
**http://localhost:8000/docs**
