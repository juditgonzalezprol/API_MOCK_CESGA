# 📥 CESGA API - Datos Externos a Descargar

## ✅ Estado de la API

```
✅ API FUNCIONANDO CORRECTAMENTE
   - Imports: OK
   - Endpoints: OK (5 rutas disponibles)
   - Database: Inicializado (SQLite)
   - Versión: 1.0.0
   - Puerto: 8000
```

---

## 📋 Resumen: Qué Descargar

La API tiene **dos niveles de funcionamiento**:

### 1️⃣ **NIVEL BÁSICO** (Ya funciona - Sin descargas)
- ✅ API completa operativa
- ✅ 6 proteínas precargadas (UniProt)
- ✅ Resultados simulados realistas
- ✅ Información biológica sintética
- ✅ Scripts de CESGA listos

**Uso**: Pruebas, hackathons, desarrollo frontend
**Descarga requerida**: NINGUNA

### 2️⃣ **NIVEL AVANZADO** (Mejor precisión - Requiere descargas)
- 📥 Estructuras 3D reales del PDB
- 📥 Predicciones AlphaFold2 reales
- 📥 Bases de datos BLAST/HMMER
- 📥 Análisis biológico mejorado

**Uso**: Investigación real, análisis preciso
**Descarga requerida**: ~50 GB (opcional)

---

## 🔍 Bases de Datos Necesarias (Por Tipo)

### **GRUPO A: Alto Impacto** (Recomendado - 25GB)

#### 1. **AlphaFold2 Database** 
**Para**: Predicciones de estructura 3D ⭐⭐⭐⭐⭐

```
Nombre: AlphaFold2 Database (Proteins)
Tamaño: ~15-20 GB (proteomas completos)
Actualización: Anual
Fuente: https://alphafold.ebi.ac.uk/download
```

**Qué contiene**:
- Predicciones de estructura para 200M+ proteínas
- Información de confianza (pLDDT)
- Matrices PAE (Predicted Aligned Error)

**Cómo descargar**:
```bash
# Opción 1: Acceso por web
# https://alphafold.ebi.ac.uk/download

# Opción 2: Via FTP (más rápido)
wget ftp://ftp.ebi.ac.uk/pub/databases/alphafold/latest/proteomes/

# Opción 3: Descarga selectiva (menor tamaño)
# Descargar solo el archivo que necesites (organismo específico)
```

**Dónde colocarlo en el API**:
```
API_CESGA/data/alphafold_db/
  ├── structure_predictions/
  ├── confidence_scores/
  └── metadata/
```

---

#### 2. **PDB (Protein Data Bank)**
**Para**: Estructuras experimentales ⭐⭐⭐⭐

```
Nombre: PDB Complete Download
Tamaño: ~30 GB (todos los archivos)
         ~5 GB (subset importante)
Actualización: Semanal
Fuente: https://www.rcsb.org/docs/programmatic-access/file-download-services
```

**Qué contiene**:
- 190,000+ estructuras 3D
- Archivos en formato PDB/CIF/mmCIF
- Metadatos (resolución, método experimental)

**Cuál descargar**:
```bash
# Opción 1: Todos (COMPLETO - 30 GB)
rsync -rlpt -v --delete --port=33444 \
  rsync.rcsb.org::ftp_data/structures/divided/pdb/ \
  ./pdb/

# Opción 2: Solo lo importante (5 GB)
# - Estructuras con resolución < 2.0 Å
# - Únicamente estructuras humanas

# Opción 3: Por proteína individual
# https://www.rcsb.org/
# Buscar: 1UBQ, 4MIF, 1HBA (ya listadas en API)
```

**Dónde colocarlo**:
```
API_CESGA/data/pdb/
  ├── structures/
  │   ├── 1ubq.pdb
  │   ├── 4mif.pdb
  │   └── ...
  └── metadata/
```

---

#### 3. **UniProt Database**
**Para**: Información de proteínas ⭐⭐⭐⭐

```
Nombre: UniProt/SwissProt
Tamaño: SwissProt: ~1.5 GB, TrEMBL: ~100+ GB
Actualización: Mensual
Fuente: https://www.uniprot.org/help/downloads
```

**Qué descargar**:
- **SwissProt** (curado): 570,000 proteínas ✅ RECOMENDADO
- **TrEMBL** (no curado): Millones (muy grande)

**Cómo**:
```bash
# SwissProt (RECOMENDADO)
wget https://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.fasta.gz

# O descarga estructurada:
wget https://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.dat.gz
```

**Dónde colocarlo**:
```
API_CESGA/data/uniprot/
  ├── uniprot_sprot.fasta
  ├── uniprot_sprot.dat
  └── index/
```

---

### **GRUPO B: Impacto Medio** (Opcional - 10 GB)

#### 4. **BLAST Databases**
**Para**: Búsqueda de homología ⭐⭐⭐

```
Nombre: NCBI BLAST Databases
Tamaño: ~10 GB (depende de bases)
Actualización: Mensual
Fuente: ftp://ftp.ncbi.nlm.nih.gov/blast/db/
```

**Bases más usadas**:
```
nr        - Non-redundant protein
nt        - Nucleotide non-redundant
swissprot - SwissProt subset
```

**Cómo descargar**:
```bash
# Método 1: Mediante update_blastdb.pl
update_blastdb.pl --decompress swissprot

# Método 2: Manual
wget ftp://ftp.ncbi.nlm.nih.gov/blast/db/swissprot.*.tar.gz

# Método 3: Para el proyecto (MINIMAL - solo SwissProt)
wget ftp://ftp.ncbi.nlm.nih.gov/blast/db/swissprot.00.tar.gz
wget ftp://ftp.ncbi.nlm.nih.gov/blast/db/swissprot.01.tar.gz
# Extractar: tar -xzf swissprot.*.tar.gz
```

**Dónde colocarlo**:
```
API_CESGA/data/blast_db/
  ├── swissprot/
  │   ├── swissprot.00.phr
  │   ├── swissprot.00.pin
  │   ├── swissprot.00.psq
  │   └── ...
  └── nr/
```

---

#### 5. **Pfam Database**
**Para**: Identificar dominios de proteína ⭐⭐⭐

```
Nombre: Pfam
Tamaño: ~2 GB (modelo HMM)
Actualización: Anual
Fuente: http://ftp.ebi.ac.uk/pub/databases/Pfam/
```

**Qué descargar**:
```bash
# Modelo HMM principal (RECOMENDADO)
wget ftp://ftp.ebi.ac.uk/pub/databases/Pfam/current_release/Pfam-A.hmm.gz

# Archivo presipitado (generado)
wget ftp://ftp.ebi.ac.uk/pub/databases/Pfam/current_release/Pfam-A.hmm.dat.gz

# Base de datos FASTA (opcional)
wget ftp://ftp.ebi.ac.uk/pub/databases/Pfam/current_release/Pfam-A.fasta.gz
```

**Dónde colocarlo**:
```
API_CESGA/data/pfam/
  ├── Pfam-A.hmm
  ├── Pfam-A.hmm.dat
  └── Pfam-A.fasta
```

---

### **GRUPO C: Bajo Impacto** (Opcional - 10 GB)

#### 6. **HMMER Database (Completitud)**
**Para**: Búsqueda más precisa de HMMs ⭐⭐

```
Nombre: HMMER Manual
Tamaño: ~500 MB
Fuente: https://www.ebi.ac.uk/Tools/hmmer/
```

**Comando de descarga**:
```bash
wget ftp://ftp.ebi.ac.uk/pub/software/hmmer/hmmer-3.3.2.tar.gz
tar -xzf hmmer-3.3.2.tar.gz
```

---

#### 7. **InterPro Database** (OPCIONAL)
**Para**: Análisis funcional mejorado ⭐

```
Nombre: InterPro
Tamaño: ~5 GB
Fuente: https://www.ebi.ac.uk/interpro/download/
```

---

## 📊 Tabla Resumen

| Base | Tamaño | Crítico | Descarga | URL |
|------|--------|---------|----------|-----|
| AlphaFold2 DB | 15-20 GB | ⭐⭐⭐ | Selectiva | alphafold.ebi.ac.uk |
| PDB | 5-30 GB | ⭐⭐⭐⭐ | Selectiva | rcsb.org |
| UniProt/SwissProt | 1.5 GB | ⭐⭐⭐⭐ | Completa | uniprot.org |
| BLAST/Nr | 10 GB | ⭐⭐⭐ | Selectiva | ncbi.nlm.nih.gov |
| Pfam | 2 GB | ⭐⭐⭐ | Completa | ebi.ac.uk/pfam |
| HMMER | 0.5 GB | ⭐⭐ | Opcional | ebi.ac.uk/hmmer |
| InterPro | 5 GB | ⭐ | Opcional | ebi.ac.uk/interpro |

**TOTAL RECOMENDADO**: ~25-35 GB (depende de necesidades)

---

## 🎯 Descargas por Caso de Uso

### **Caso 1: Hackathon/Demo** (Mejor ratio tiempo-beneficio)
```
✅ Descarga NADA - API funciona sin descargas
   - Usa datos precargados (6 proteínas reales)
   - Resultados simulados realistas
   - Perfecto para frontend/testing
   
⏱️ Tiempo: 0 segundos
💾 Espacio: 0 GB
```

### **Caso 2: Ambiente Local** (Máquina de desarrollo)
```
Descargar:
  1. UniProt/SwissProt (1.5 GB) ⭐ RECOMENDADO
  2. PDB subset (5 GB) - estructuras importantes
  3. Pfam (2 GB) - para análisis de dominios

⏱️ Tiempo: ~2-3 horas
💾 Espacio: 8.5 GB + índices
```

### **Caso 3: CESGA Finis Terrae III** (Producción)
```
Descargar TODO:
  1. AlphaFold2 DB (20 GB)
  2. PDB completo (30 GB)
  3. UniProt (1.5 GB)
  4. BLAST/Nr (10 GB)
  5. Pfam (2 GB)
  6. InterPro (5 GB)

⏱️ Tiempo: ~24 horas (en conexión buena)
💾 Espacio: 68.5 GB + índices (~100 GB total)
```

---

## 🚀 Instrucciones de Descarga RÁPIDA

### **Descarga Mínima (8.5 GB - 2 horas)**

```bash
#!/bin/bash
cd /Users/juditgonzalez/Desktop/API_CESGA

# Crear estructura de carpetas
mkdir -p data/{uniprot,pdb,pfam,blast_db,alphafold_db}

# 1. UniProt SwissProt (1.5 GB)
cd data/uniprot
wget https://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.fasta.gz
gunzip uniprot_sprot.fasta.gz
cd ../..

# 2. Pfam (2 GB) 
cd data/pfam
wget ftp://ftp.ebi.ac.uk/pub/databases/Pfam/current_release/Pfam-A.hmm.gz
gunzip Pfam-A.hmm.gz
cd ../..

# 3. PDB Importante (5 GB - solo estructuras buenas)
cd data/pdb
# Descarga manual desde: https://www.rcsb.org/
# O descarga proteínas específicas:
for pdb_id in 1ubq 4mif 1hba 1lyz; do
  wget https://files.rcsb.org/download/${pdb_id}.pdb
done
cd ../..

echo "✅ Descargas completadas"
```

### **Descarga Completa (50+ GB - 1 día)**

```bash
#!/bin/bash
cd /Users/juditgonzalez/Desktop/API_CESGA
mkdir -p data/{uniprot,pdb,pfam,blast_db,alphafold_db}

# (Usar scripts arriba para cada DB)
# + descargar AlphaFold2 DB selectivamente
# + descargar BLAST Nr completo
```

---

## 🔗 URLs de Descarga Directa

### **Para Copiar-Pegar**

```
UniProt SwissProt:
https://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.fasta.gz

Pfam-A HMM:
ftp://ftp.ebi.ac.uk/pub/databases/Pfam/current_release/Pfam-A.hmm.gz

BLAST NR (parte 1):
ftp://ftp.ncbi.nlm.nih.gov/blast/db/BLAST_statisticsswissprotSWISSPROT.tar.gz

PDB (RCSB):
https://www.rcsb.org/

AlphaFold2 DB:
https://alphafold.ebi.ac.uk/download
```

---

## 📁 Estructura Final Recomendada

```
API_CESGA/
├── data/
│   ├── uniprot/
│   │   ├── uniprot_sprot.fasta      (1.5 GB)
│   │   └── uniprot_sprot.dat
│   │
│   ├── pdb/
│   │   ├── structures/
│   │   │   ├── 1ubq.pdb
│   │   │   ├── 4mif.pdb
│   │   │   └── ... (más estructuras)
│   │   └── metadata/
│   │
│   ├── pfam/
│   │   ├── Pfam-A.hmm              (2 GB + índices)
│   │   ├── Pfam-A.hmm.dat
│   │   └── Pfam-A.fasta
│   │
│   ├── blast_db/
│   │   ├── swissprot/
│   │   │   ├── swissprot.*.phr
│   │   │   ├── swissprot.*.pin
│   │   │   └── swissprot.*.psq
│   │   └── nr/
│   │
│   └── alphafold_db/
│       ├── structures/
│       ├── confidence/
│       └── metadata/
│
├── app/
│   ├── services/
│   │   └── real_protein_database.py
│   └── ...
└── ...
```

---

## 💾 Integración con la API

Una vez descargadas, actualizar los rutas en el código:

### **En `app/config.py`:**
```python
DATA_ROOT = Path("/Users/juditgonzalez/Desktop/API_CESGA/data")
BLAST_DB_PATH = DATA_ROOT / "blast_db"
UNIPROT_PATH = DATA_ROOT / "uniprot"
PDB_PATH = DATA_ROOT / "pdb"
PFAM_PATH = DATA_ROOT / "pfam"
ALPHAFOLD_PATH = DATA_ROOT / "alphafold_db"
```

### **En `app/services/job_service.py`:**
```python
# Líneas ~45-50
precomputed_pdb = self.PRECOMPUTED_DIR / f"{protein_name}.pdb"
# Cambiar a:
precomputed_pdb = BLAST_DB_PATH.parent / f"{protein_name}.pdb"
```

---

## ⚙️ Actualizaciones Automáticas

Para mantener las bases de datos al día:

```bash
#!/bin/bash
# cron job: diario a las 2 AM
0 2 * * * /Users/juditgonzalez/Desktop/API_CESGA/scripts/update_databases.sh

# Contenido de update_databases.sh:
#!/bin/bash
cd /Users/juditgonzalez/Desktop/API_CESGA/data

# Actualizar UniProt
cd uniprot
wget -N https://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.fasta.gz
gunzip -N uniprot_sprot.fasta.gz
cd ..

# Actualizar Pfam
cd pfam
wget -N ftp://ftp.ebi.ac.uk/pub/databases/Pfam/current_release/Pfam-A.hmm.gz
gunzip -N Pfam-A.hmm.gz
cd ..

echo "$(date): Bases de datos actualizadas" >> update.log
```

---

## 🎓 Resumen Ejecutivo

| Necesidad | Acción |
|-----------|--------|
| **Solo probar API** | ✅ Nada - funciona ahora |
| **Desarrollo local** | 📥 Descargar UniProt + Pfam (3.5 GB) |
| **Mejor precisión** | 📥 Descargar todo GRUPO A (25 GB) |
| **Producción CESGA** | 📥 Descargar TODOS los grupos (68 GB) |

---

**La API está ✅ FUNCIONANDO. Las descargas de datos son OPCIONALES y mejoran precisión.** 🚀
