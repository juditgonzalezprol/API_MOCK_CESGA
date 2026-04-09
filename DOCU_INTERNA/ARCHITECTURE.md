# CESGA API Architecture Documentation

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     HACKATHON FRONTEND                          │
│         (Web UI / Mobile App / CLI Tool)                        │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       │ HTTP/JSON
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FASTAPI APPLICATION                        │
│              (app/main.py - Lifespan Management)                │
└──────────────┬──────────────────────────────┬────────────────────┘
               │                              │
         ┌─────▼─────┐                   ┌─────▼─────┐
         │   CORS    │                   │ Background│
         │Middleware │                   │Scheduler  │
         └───────────┘                   └─────┬─────┘
               │                               │
               ▼                               ▼
    ┌──────────────────────┐    ┌──────────────────────┐
    │   REST ROUTERS      │    │  Job State Machine   │
    │  (app/routers/)     │    │(background_tasks/)  │
    │                     │    │                      │
    │ POST /jobs/submit   │    │ PENDING → RUNNING   │
    │ GET /jobs/{id}/...  │    │ RUNNING → COMPLETED│
    │                     │    │ (Async Scheduler)  │
    └────────┬────────────┘    └─────────┬───────────┘
             │                           │
             │                           │
             └───────────┬───────────────┘
                        │
                        ▼
    ┌──────────────────────────────────────┐
    │     BUSINESS LOGIC SERVICES          │
    │                                      │
    │  JobService (app/services/)         │
    │  ├─ create_job()                    │
    │  ├─ get_job()                       │
    │  ├─ Mark_job_running()              │
    │  ├─ mark_job_completed()            │
    │  └─ _generate_job_outputs()         │
    │                                      │
    │  MockDataService (app/services/)    │
    │  ├─ generate_confidence_data()      │
    │  ├─ generate_pdb_structure()        │
    │  ├─ generate_biological_data()      │
    │  └─ generate_accounting_data()      │
    └──────────────────┬───────────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
   ┌─────────┐  ┌──────────┐  ┌────────────────┐
   │DATABASE │  │FILE SYSTEM│  │CONFIGURATION  │
   │(SQLite/ │  │(mock_data/│  │(config.py/.env)
   │PosgSQL) │  │sample_   │  │                │
   │         │  │results/) │  │                │
   │Job Table│  │├─PDB     │  │                │
   │         │  │├─CIF     │  │                │
   └─────────┘  │├─JSON    │  └────────────────┘
                │└─Logs    │
                └──────────┘
```

## Component Description

### 1. **FastAPI Application (app/main.py)**
- **Purpose**: Application factory and entry point
- **Key Features**:
  - Lifespan management (startup/shutdown)
  - CORS middleware configuration
  - Router registration
  - Global exception handling
  - Background task lifecycle

**Lifecycle Events:**
```
Startup:
  1. Create database tables
  2. Start background job scheduler task
  3. Log initialization messages

Running:
  - Process HTTP requests
  - Route to appropriate handler
  - Execute background tasks

Shutdown:
  1. Cancel scheduler task
  2. Close connections
  3. Log shutdown messages
```

### 2. **REST API Routers (app/routers/jobs.py)**
- **Purpose**: Define HTTP endpoints and handle requests
- **Endpoints**:
  ```
  POST   /jobs/submit              → Create new job
  GET    /jobs/{id}/status         → Get job status
  GET    /jobs/{id}/outputs        → Get results (completed jobs only)
  GET    /jobs/{id}/accounting     → Get resource accounting
  GET    /jobs/                    → List all jobs
  GET    /health                   → Health check
  GET    /                          → API info
  ```

**Request Flow:**
```
User Request
    ↓
Router Endpoint (e.g., POST /jobs/submit)
    ↓
Input Validation (Pydantic schema)
    ↓
Service Layer (Business logic)
    ↓
Database Operations
    ↓
Response Generation
    ↓
Response to User
```

### 3. **Service Layer (app/services/)**

#### JobService (app/services/job_service.py)
- **Purpose**: Core business logic for job management
- **Methods**:
  ```python
  create_job(db, request)           # Insert job to DB
  get_job(db, job_id)               # Retrieve job record
  update_job_status(db, job_id, status)  # Update status
  Mark_job_running(db, job_id)      # PENDING → RUNNING transition
  mark_job_completed(db, job_id)    # RUNNING → COMPLETED transition
  _generate_job_outputs(job)        # Create result files
  get_job_outputs_dict(job)         # Load and parse outputs
  get_job_accounting(job)           # Load accounting data
  ```

#### MockDataService (app/services/mock_data_service.py)
- **Purpose**: Generate synthetic bioinformatics data
- **Methods**:
  ```python
  generate_confidence_data(seq_len)    # pLDDT + PAE matrices
  generate_pdb_structure(sequence)     # PDB format structure
  generate_mmcif_structure(sequence)   # mmCIF format structure
  generate_biological_data(sequence)   # Solubility, toxicity, etc.
  generate_logs()                      # Container output simulation
  generate_accounting_data(...)        # Resource usage stats
  ```

### 4. **Background Job Scheduler (app/background_tasks/job_scheduler.py)**
- **Purpose**: Manage job state transitions asynchronously
- **Architecture**: Async event loop with periodic polling

**State Transition Logic:**
```python
while running:
    # Check PENDING jobs
    if (now - job.created_at) >= PENDING_TO_RUNNING_DELAY:
        job.status = RUNNING
        job.started_at = now
        save_to_db()
    
    # Check RUNNING jobs
    if (now - job.started_at) >= RUNNING_TO_COMPLETED_DELAY:
        job.status = COMPLETED
        job.completed_at = now
        generate_outputs()
        save_to_db()
    
    await asyncio.sleep(1)  # Check every second
```

### 5. **Data Models**

#### SQLAlchemy Models (app/models/db_models.py)
```python
class Job:
    id: str                       # Unique job identifier
    fasta_sequence: str           # Input protein sequence
    fasta_filename: str           # Original filename
    gpus: int                     # GPU count requested
    cpus: int                     # CPU count requested
    memory_gb: float              # Memory requested (GB)
    max_runtime_seconds: int      # Max execution time
    status: JobStatus             # PENDING, RUNNING, COMPLETED, etc.
    created_at: datetime          # Submission timestamp
    started_at: datetime          # Start timestamp
    completed_at: datetime        # Completion timestamp
    output_pdb_path: str          # Path to PDB output
    output_cif_path: str          # Path to mmCIF output
    confidence_json_path: str     # Path to confidence data
    logs_path: str                # Path to execution logs
    biological_data_path: str     # Path to bio predictions
    accounting_data_path: str     # Path to resource accounting
    error_message: str            # For failed jobs
```

#### Pydantic Schemas (app/models/schemas.py)
- **Request**: `JobSubmitRequest` - Validates input
- **Response**: 
  - `JobSubmitResponse` - Job creation response
  - `JobStatusResponse` - Status query response
  - `JobOutputsResponse` - Results with structures/properties
  - `JobAccountingResponse` - Resource accounting

### 6. **Database Configuration (app/database.py)**
- **Engines**: Supports both SQLite (default) and PostgreSQL
- **Session Management**: Dependency injection for FastAPI
- **Models**: Base class for all ORM models

## Data Flow Diagram

### Job Submission Flow
```
┌─────────────────────────────┐
│  User sends HTTP request    │
│  POST /jobs/submit          │
│  {fasta, gpus, cpus, ...}   │
└────────────────┬────────────┘
                 │
                 ▼
         ┌───────────────────┐
         │Pydantic Validation│
         │ - FASTA format OK?│
         │ - GPUs ≤ MAX?     │
         └────────┬──────────┘
                  │
                  ▼
         ┌──────────────────────┐
         │ JobService.create_job│
         │ - Generate job_id    │
         │ - Insert to database │
         └────────┬─────────────┘
                  │
                  ▼
         ┌───────────────────┐
         │  Database update  │
         │  status = PENDING │
         └────────┬──────────┘
                  │
                  ▼
         ┌────────────────────┐
         │ Return response    │
         │ {job_id, PENDING}  │
         └────────────────────┘
```

### Job Completion Flow
```
PENDING Job
    ↓ (after PENDING_TO_RUNNING_DELAY)
Background Scheduler detects
    ↓
Mark as RUNNING (job.started_at = now)
    ↓ (after RUNNING_TO_COMPLETED_DELAY)
Background Scheduler detects
    ↓
Call job_service.mark_job_completed()
    ↓
┌─────────────────────────┐
│ _generate_job_outputs()│
│ ├─ PDB structure       │
│ ├─ mmCIF structure     │
│ ├─ Confidence scores   │
│ ├─ Biological data     │
│ ├─ Logs                │
│ └─ Accounting data     │
└────────────┬───────────┘
             ↓
    Update database
    status = COMPLETED
    Set output paths
```

## File I/O Structure

```
app/mock_data/
├── sample_results/         # Output files per job
│   ├── job_a1b2c3d4/
│   │   ├── structure.pdb
│   │   ├── structure.cif
│   │   ├── confidence.json
│   │   ├── biological_properties.json
│   │   ├── slurm_output.log
│   │   └── accounting.json
│   ├── job_e5f6g7h8/
│   │   └── [same files]
│   └── ...
│
└── [standalone mock files]
    ├── ubiquitin_confidence.json
    ├── insulin_confidence.json
    └── ...
```

## Configuration Hierarchy

```
Defaults (app/config.py)
    ↓
.env file values (override defaults)
    ↓
Environment variables (highest priority)
    ↓
Final Settings object (app.config.settings)
```

**Example:**
```ini
# .env file
DATABASE_URL=postgresql://localhost/mydb
DEBUG=False
PENDING_TO_RUNNING_DELAY=10
```

---

## Concurrency Model

### HTTP Request Handling
- **FastAPI/Uvicorn**: Async with thread pool
- **Requests handled**: Concurrently by async event loop
- **Database access**: Sync SQLAlchemy (thread-safe with connection pooling)

### Background Task Processing
- **Scheduler**: Async coroutine loop (separate from HTTP loop)
- **Job state checks**: Every 1 second
- **Database updates**: Blocking calls (acceptable for mock service)

**Concurrency Safeguards:**
```python
# Thread-safe database session
SessionLocal = sessionmaker(bind=engine)

# Multiple concurrent requests
async def handle_http_request():
    db = SessionLocal()  # New session per request
    # ... operations ...
    db.close()

# Background state machine
async def process_jobs():
    db = SessionLocal()  # Separate session
    # ... state transitions ...
    db.close()
```

## Error Handling

```
API Errors:
    404 Not Found        → Job ID doesn't exist
    400 Bad Request      → Validation failed or invalid state
    422 Unprocessable    → Pydantic validation error
    500 Server Error     → Unhandled exception

Job Errors:
    error_message field  → Stored in database for failed jobs
    Logged to console    → Check terminal for details
```

## Performance Characteristics

| Metric | Value | Notes |
|--------|-------|-------|
| Request latency | <100ms | Mostly DB I/O |
| State check frequency | 1/sec | Configurable |
| Concurrent jobs | Unlimited* | Limited by DB |
| Memory per job | ~1MB | Minimal (metadata only) |
| Max FASTA size | 100KB | Configurable in schema |

*Practical limit depends on database and file system.

## Security Considerations

**Current Implementation (MVP):**
- ⚠️ No authentication/authorization
- ⚠️ CORS allows all origins
- ⚠️ Suitable for hackathon/internal use

**Production Hardening:**
- ✅ Add API key authentication
- ✅ Restrict CORS to frontend domain
- ✅ Use HTTPS/TLS
- ✅ Add rate limiting
- ✅ Implement input sanitization
- ✅ Add audit logging

---

## Deployment Path

### Local Development
```bash
python -m uvicorn app.main:app --reload --port 8000
```

### Production
```bash
# Using Gunicorn + Uvicorn
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app

# Or Docker
docker build -t cesga-api .
docker run -p 8000:8000 cesga-api
```

---

**Document version**: 1.0
**Last updated**: 2024-03-17
**Platform**: FastAPI + SQLAlchemy + SQLite
