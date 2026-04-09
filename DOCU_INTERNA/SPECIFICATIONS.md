# CESGA API Simulator - Specification & Conformance Document

## 📋 Conformance with Requirements

Based on the specifications from:
- `/docs/Local, novice-friendly web interface for protein structure prediction on a CESGA-backed HPC cluster.docx`
- `/docs/Propuesta de cambios_API_RETO_CAMELIA.pdf`

### ✅ SECTION A: Gestión de Trabajos (Mock de Slurm)

#### A1. `POST /jobs/submit` ✅
**Requirement**: Recibe la secuencia FASTA y los parámetros de hardware (GPUs, memoria, tiempo). Valida el formato del input pero, en lugar de invocar a sbatch, registra el trabajo en una BD local con estado PENDING.

**Implementation**:
- ✅ Accepts FASTA sequence with format validation
- ✅ Accepts hardware parameters: GPUs, CPUs, memory (GB), max_runtime_seconds
- ✅ Validates FASTA format (must start with '>')
- ✅ Validates resource limits:
  - GPUs: 0-4 max (configurable MAX_GPUS_PER_JOB)
  - Memory: 0-256 GB (configurable MAX_MEMORY_GB)
  - CPUs: 1-64 (configurable MAX_CPUS_PER_JOB)
  - Runtime: 60-86400 seconds
- ✅ Creates entry in local SQLite/PostgreSQL database
- ✅ Sets initial state to PENDING
- ✅ Returns job_id in format "job_<hex>"
- ✅ Records creation timestamp

**Test**: 
```bash
curl -X POST http://localhost:8000/jobs/submit \
  -H "Content-Type: application/json" \
  -d '{
    "fasta_sequence": ">protein\nMKFSMVQVS...",
    "fasta_filename": "protein.fasta",
    "gpus": 1,
    "cpus": 8,
    "memory_gb": 32.0,
    "max_runtime_seconds": 3600
  }'
```

#### A2. `GET /jobs/{id}/status` ✅
**Requirement**: Emula los comandos squeue y sacct. Devuelve estados realistas: PENDING (en cola), RUNNING (simulando ejecución) o COMPLETED.

**Implementation**:
- ✅ Returns job status information
- ✅ Status values: PENDING, RUNNING, COMPLETED (also supports FAILED, CANCELLED)
- ✅ Returns metadata:
  - job_id
  - current status
  - created_at (timestamp)
  - started_at (when moved to RUNNING, null if still PENDING)
  - completed_at (when finished, null if not completed)
  - resource metadata (gpus, cpus, memory, max_runtime)
  - fasta_filename
  - error_message (if applicable)
- ✅ Similar to Unix `squeue` (current status) and `sacct` (accounting info)

**Test**:
```bash
curl http://localhost:8000/jobs/{job_id}/status
```

#### A3. Programador de Eventos Interno (Internal Event Scheduler) ✅
**Requirement**: Un hilo secundario (worker) actualiza los estados basándose en reglas de negocio (ej. un trabajo pasa de cola a ejecución tras $N$ segundos) para simular la carga del cluster.

**Implementation**:
- ✅ Implemented as async background task in `app/background_tasks/job_scheduler.py`
- ✅ Runs as separate asyncio coroutine (not blocking HTTP requests)
- ✅ Configurable transition delays:
  - `PENDING_TO_RUNNING_DELAY` (default: 5 seconds)
  - `RUNNING_TO_COMPLETED_DELAY` (default: 10 seconds)
- ✅ Checks job states every 1 second
- ✅ Automatically transitions jobs through states based on time elapsed
- ✅ Respects system resource limits
- ✅ Generates output files when job completes

**Configuration** (in `.env`):
```ini
PENDING_TO_RUNNING_DELAY=5
RUNNING_TO_COMPLETED_DELAY=10
```

---

### ✅ SECTION B: Módulo de Datos y Resultados (Mock de Almacenamiento)

#### B1. Repo de Datos Precomputados ✅
**Requirement**: El servidor lo dispondríamos de una carpeta con resultados reales de AlphaFold2 (PDB, mmCIF, JSON de confianza) previamente generados.

**Implementation**:
- ✅ Dedicated folder: `app/mock_data/precomputed/` for precomputed structures
- ✅ Dedicated folder: `app/mock_data/sample_results/{job_id}/` for per-job outputs
- ✅ Real protein database in `app/services/real_protein_database.py` includes:
  - 6 real proteins from UniProt/PDB:
    - Ubiquitin (P0CG47, PDB: 1UBQ)
    - Insulin (P01308, PDB: 4MIF)
    - Hemoglobin alpha (P69905, PDB: 1A3N)
    - Lysozyme (P61626, PDB: 1LYZ)
    - Amylase (P04746, PDB: 1BVN)
    - Myoglobin (P02144, PDB: 1MBN)
  - Includes real properties from literature:
    - Molecular weight, pI, extinction coefficients
    - Known PDB structures with resolutions
    - UniProt identifiers and links

#### B2. `GET /jobs/{id}/outputs` ✅
**Requirement**: Cuando un trabajo simulado llega al estado COMPLETED, este endpoint sirve los archivos correspondientes a la secuencia enviada, permitiendo que el frontend que realicen los participantes los visualice con Mol*.

**Implementation**:
- ✅ Only available when job status == COMPLETED (returns 400 if not)
- ✅ Returns structure files:
  - **pdb_file**: Full PDB format (X-ray coordinates compatible with Mol*)
  - **cif_file**: mmCIF format (alternative 3D structure format)
  - **confidence**: 
    - plddt_per_residue (array, one score per residue, 0-100)
    - plddt_mean (average confidence)
    - plddt_histogram (distribution: very_high, high, medium, low)
    - pae_matrix (predicted aligned error, NxN matrix)
    - mean_pae (average PAE error)
- ✅ Data can be visualized in Mol* viewer
- ✅ Returns full output bundle in JSON format

**Response Example**:
```json
{
  "job_id": "job_abc123",
  "status": "COMPLETED",
  "structural_data": {
    "pdb_file": "HEADER...",
    "cif_file": "data_simulated...",
    "confidence": {
      "plddt_per_residue": [75.2, 80.1, 82.3, ...],
      "plddt_mean": 75.8,
      "pae_matrix": [[0.5, 1.2, ...], ...],
      "mean_pae": 3.2
    }
  },
  "biological_data": { ... },
  "logs": "..."
}
```

#### B3. Simulación de Logs ✅
**Requirement**: Genera archivos de texto que imitan la salida estándar de un contenedor Apptainer, incluyendo warnings de GPU y progreso de la búsqueda MSA.

**Implementation**:
- ✅ `slurm_output.log` file generated per job
- ✅ Realistic Apptainer container output simulation:
  - Timestamps (ISO format)
  - Model weight loading messages
  - MSA (Multiple Sequence Alignment) generation progress (0%, 25%, 50%, 75%, 100%)
  - GPU memory utilization warnings (e.g., "GPU memory utilization: 89%")
  - AlphaFold2 model evaluation messages
  - pLDDT distribution statistics
  - Final completion message
- ✅ Example log output:
  ```
  [2024-03-17 10:30:05] Job started in Apptainer container
  [INFO] Loading AlphaFold2 model weights...
  [INFO] Model weights loaded successfully
  [INFO] Generating multiple sequence alignment (MSA)...
  [INFO] MSA generation at 25%...
  [INFO] MSA generation at 75%...
  [INFO] MSA generation at 100%
  [WARNING] GPU memory utilization: 89%
  [INFO] Prediction confidence (pLDDT) distribution: mean=75.3, std=12.1
  [2024-03-17 10:30:35] Job completed successfully
  ```

---

### ✅ SECTION C: Telemetría y Contabilidad (Mock de Accounting)

#### C1. `GET /jobs/{id}/accounting` ✅
**Requirement**: Al finalizar, calcula un consumo ficticio de "CPU-horas" y eficiencia de memoria para que el portal presente informes de uso realistas.

**Implementation**:
- ✅ Only available when job has resource data (after completion recommended)
- ✅ Returns realistic resource consumption metrics:
  - **cpu_hours**: Total CPU-hours consumed (calculated as cpus × wall_time × utilization%)
  - **gpu_hours**: Total GPU-hours (if GPUs were requested)
  - **memory_gb_hours**: Memory-hours consumed
  - **total_wall_time_seconds**: Total elapsed time
  - **cpu_efficiency_percent**: CPU utilization percentage (40-70%)
  - **memory_efficiency_percent**: Memory utilization percentage (60-85%)
  - **gpu_efficiency_percent**: GPU utilization (if applicable, 75-95%)
- ✅ Realistic values based on job configuration

**Response Example**:
```json
{
  "job_id": "job_abc123",
  "status": "COMPLETED",
  "accounting": {
    "cpu_hours": 6.8,
    "gpu_hours": 2.3,
    "memory_gb_hours": 128.0,
    "total_wall_time_seconds": 1500,
    "cpu_efficiency_percent": 85.5,
    "memory_efficiency_percent": 92.1
  }
}
```

---

## 📊 Flujo de Entrada/Salida (Input/Output Flow)

### Paso 1: Entrada (Submission Phase) ✅

1. **Input**: Usuario proporciona secuencia en formato FASTA
   ```fasta
   >protein_name
   MKVLSPADKTNVKA...
   ```

2. **Validación**: API verifica
   - ✅ Formato FASTA válido (comienza con '>')
   - ✅ Secuencia de amino ácidos válida
   - ✅ Límites de recursos (max 4 GPUs, 256 GB RAM, 64 CPUs)
   - ✅ Máximo tiempo de ejecución (24 horas)

3. **Registro**: 
   - ✅ Se crea entrada en BD con job_id único
   - ✅ Estado inicial: PENDING
   - ✅ Se registra timestamp de creación
   - ✅ Se inicia temporizador de "cola de espera"

### Paso 2: Procesamiento (Simulation Phase) ✅

1. **En Cola** (PENDING state):
   - ✅ Durante X segundos (configurable, default 5s)
   - ✅ GET /status devuelve: status=PENDING, started_at=null, completed_at=null
   - ✅ Logs no están disponibles aún

2. **Ejecución** (RUNNING state):
   - ✅ Después de X segundos, estado cambia a RUNNING
   - ✅ started_at timestamp registrado
   - ✅ GetStatus devuelve: status=RUNNING, started_at=<timestamp>
   - ✅ Logs simulados disponibles (se generan gradualmente)
   - ✅ Portal puede mostrar logs en tiempo real (simulados)

3. **Transición a Completado** (COMPLETED state):
   - ✅ Después de Y segundos más (configurable, default 10s)
   - ✅ Estado cambia a COMPLETED
   - ✅ completed_at timestamp registrado
   - ✅ Todos los archivos generados y almacenados

### Paso 3: Salida (Delivery Phase) ✅

1. **Finalización** (COMPLETED):
   ```
   /jobs/{id}/status → status=COMPLETED
   ```

2. **Entrega de Assets** - `GET /jobs/{id}/outputs`:
   - ✅ Estructura 3D: `.pdb` (PDB format)
   - ✅ Estructura alternativa: `.cif` (mmCIF format)
   - ✅ Confianza:
     - pLDDT por residuo (para colorear proteína por confianza)
     - Matriz PAE (para heatmap de error de alineamiento)
   - ✅ Logs (salida estándar simulada)
   - ✅ Datos biológicos adicionales

---

## 🧬 Datos Biológicos Adicionales (Extra Data)

### ✅ Implementado: Propiedades Bioinformáticas

Según los requisitos, se proporcionan datos adicionales que añaden variabilidad:

1. **Solubility Score** ✅
   - Rango: 0-100 (100 = máxima solubilidad)
   - Método: Análisis composición amino ácidos hydrofóbicos vs hidrofílicos
   - Predicción: "soluble", "poorly soluble", "moderately soluble"

2. **Instability Index** ✅
   - Rango: 0-100
   - Classification: "stable" (< 40) or "unstable" (> 40)
   - Método: Basado en escala Kyte-Doolittle de hidrofobicidad dipéptidos

3. **Toxicity Alerts** ✅
   - Detección de motivos potencialmente tóxicos:
     - Signal peptide consensus sequences
     - Protease cleavage sites (motivos dibasic RR, KK)
     - Disulfide bonds (múltiples cisteínas)
   - Ejemplo: "6 cysteine residues detected - may form disulfide bonds"

4. **Allergenicity Alerts** ✅
   - Detección de epítopos potenciales:
     - Tamaño de proteína (típicamente > 100 aa son alergénicos)
     - Alta densidad de carga (potencial epítopo IgE)
     - Clusters de carga repetitivos
   - Ejemplo: "High positive charge content (potential allergen epitope)"

5. **Secondary Structure Prediction** ✅
   - Predicción de estructura secundaria:
     - Porcentaje alphaliase (α-helix)
     - Porcentaje beta-strand (β-sheet)
     - Porcentaje coil (random coil)
   - Método: Cabat-Labhardt rules

6. **Sequence Properties** ✅
   - Longitud de secuencia
   - Peso molecular aproximado
   - Número de cargas positivas/negativas
   - Residuos aromáticos
   - Residuos cisteína

---

## 🗄️ Real Protein Database

### ✅ Proteínas Incluidas

La API incluye base de datos de 6 proteías reales con propiedades verificadas:

1. **Ubiquitin** (P0CG47)
   - PDB: 1UBQ
   - MW: 8.5 kDa
   - Función: Signaling protein
   - Solubility: 78.5/100 (soluble)
   - Stability: Stable (II: 29.4)

2. **Insulin** (P01308)
   - PDB: 4MIF
   - MW: 5.8 kDa
   - Función: Hormone (metabolic)
   - Links: 3 disulfide bonds
   - Allergenicity: Class II allergen

3. **Hemoglobin Alpha** (P69905)
   - PDB: 1A3N
   - MW: 15.2 kDa
   - Cofactor: Heme
   - Función: Oxygen transport

4. **Lysozyme** (P61626)
   - PDB: 1LYZ
   - MW: 14.3 kDa
   - EC: 3.2.1.17 (Lysozyme)
   - Actividad: Bacteriolytic enzyme
   - Links: 4 disulfide bonds

5. **Alpha-Amylase** (P04746)
   - PDB: 1BVN
   - MW: 57.5 kDa
   - EC: 3.2.1.1 (Glycosidase)
   - Cofactores: Ca2+, Cl-

6. **Myoglobin** (P02144)
   - PDB: 1MBN
   - MW: 17.0 kDa
   - Cofactor: Heme
   - Función: Oxygen storage

---

## 🔧 Configuración Completamente Customizable

Todos los parámetros pueden ser ajustados en `.env`:

```ini
# State transitions (seconds)
PENDING_TO_RUNNING_DELAY=5
RUNNING_TO_COMPLETED_DELAY=10

# Resource limits
MAX_GPUS_PER_JOB=4
MAX_CPUS_PER_JOB=64
MAX_MEMORY_GB=256

# Database
DATABASE_URL=sqlite:///./cesga_simulator.db

# Logging
LOG_LEVEL=INFO
DEBUG=True
```

---

## 📂 Carpeta Estructura de Resultados

Para cada trabajo completado se genera:

```
app/mock_data/sample_results/{job_id}/
├── structure.pdb                    # 3D coordinates (PDB format)
├── structure.cif                    # 3D coordinates (mmCIF format)
├── confidence.json                  # pLDDT scores + PAE matrix
├── biological_properties.json       # Solubility, stability, toxicity, allergenicity
├── slurm_output.log                 # Simulated container logs
├── accounting.json                  # CPU-hours, GPU-hours, efficiency
└── protein_metadata.json           # Protein identification if known
```

---

## ✅ CHECKLIST: Conformidad Completa

- [✅] POST /jobs/submit - FASTA validation + resource checks
- [✅] GET /jobs/{id}/status - Real-time status (PENDING→RUNNING→COMPLETED)
- [✅] GET /jobs/{id}/outputs - Structure files + confidence data
- [✅] GET /jobs/{id}/accounting - Resource usage metrics
- [✅] Background scheduler - Async state machine
- [✅] PDB/CIF generation - 3D structure files
- [✅] pLDDT/PAE data - Confidence scores for visualization
- [✅] Simulated logs - Apptainer output with GPU warnings & MSA progress
- [✅] Solubility prediction - Based on amino acid composition
- [✅] Instability index - Based on dipeptide hydrophobicity
- [✅] Toxicity alerts - Protease sites, signal peptides
- [✅] Allergenicity alerts - Potential epitopes, charge clusters
- [✅] Real protein database - 6 proteins with real properties
- [✅] Mol* compatible output - PDB format for visualization
- [✅] CORS enabled - Frontend integration ready
- [✅] Full OpenAPI documentation - Auto-generated Swagger
- [✅] Customizable timing - Via environment variables
- [✅] PostgreSQL support - For production scaling

---

## 🚀 Quick Start

```bash
# 1. Setup
cd /Users/juditgonzalez/Desktop/API_CESGA
./quickstart.sh

# 2. Initialize with real protein samples
python scripts/init_db_real_proteins.py

# 3. Start server
python -m uvicorn app.main:app --reload

# 4. Try API
curl http://localhost:8000/docs                    # Swagger UI
curl http://localhost:8000/jobs/sample_ubiquitin/status
curl http://localhost:8000/jobs/sample_ubiquitin/outputs
```

---

**Document Version**: 2.0 (with Real Protein Database)
**Last Updated**: 2024-03-17
**Status**: ✅ FULLY COMPLIANT with all specifications
