# 🖥️ CESGA API - Interfaces Gráficas Disponibles

## ✅ Sí TIENE interfaz gráfica - FastAPI incluye 3 interfaces automáticas

---

## 🚀 CÓMO INICIAR LA API

### Opción 1: Usar script (RECOMENDADO)
```bash
cd /Users/juditgonzalez/Desktop/API_CESGA
chmod +x start_api.sh
./start_api.sh
```

### Opción 2: Manual
```bash
cd /Users/juditgonzalez/Desktop/API_CESGA
source venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

---

## 📊 LAS 3 INTERFACES GRÁFICAS

### 1️⃣ **Swagger UI** ⭐⭐⭐⭐⭐ (LA MEJOR)

**URL**: `http://localhost:8000/docs`

**Qué es**: Interfaz interactiva para probar la API

**Características**:
- ✅ Ver todos los endpoints
- ✅ Documentación integrada
- ✅ Probar endpoints directamente desde el navegador
- ✅ Ver parámetros requeridos
- ✅ Ver ejemplos de respuesta
- ✅ Ejecutar curl automáticamente

**Pantalla se ve así**:
```
┌─────────────────────────────────────────────────────────┐
│ CESGA Supercomputer Simulator                      [v1.0]│
├─────────────────────────────────────────────────────────┤
│                                                         │
│ POST /jobs/submit                                       │
│   Description: Submit a new job                         │
│   [Try it out]                                          │
│                                                         │
│   Request body:                                         │
│   {                                                     │
│     "fasta_sequence": "MKVLSPAD...",                   │
│     "gpus": 4,                                          │
│     "cpus": 8                                           │
│   }                                                     │
│                                                         │
│   Responses:                                            │
│   201 - Job submitted successfully                      │
│   {                                                     │
│     "job_id": "job_123...",                            │
│     "status": "PENDING"                                │
│   }                                                     │
│                                                         │
│ GET /jobs/{job_id}/status                              │
│   Description: Get job status                           │
│   ...más endpoints                                      │
└─────────────────────────────────────────────────────────┘
```

---

### 2️⃣ **ReDoc** ⭐⭐⭐⭐ (DOCUMENTACIÓN)

**URL**: `http://localhost:8000/redoc`

**Qué es**: Documentación clara y profesional

**Características**:
- ✅ Documentación organizada
- ✅ Fácil de leer
- ✅ Esquemas claros
- ✅ Ideal para compartir con el equipo
- ✅ NO permite probar (solo lectura)

**Para**: Compartir documentación, revisar specs

---

### 3️⃣ **OpenAPI JSON** ⭐⭐⭐ (MÁQUINA)

**URL**: `http://localhost:8000/openapi.json`

**Qué es**: Especificación técnica en formato JSON/YAML

**Características**:
- ✅ Formato estándar OpenAPI 3.0
- ✅ Para herramientas automáticas
- ✅ Importar en Postman
- ✅ Generar clientes automáticos

**Para**: Integración con otras herramientas

---

## 🎯 CUÁL USAR PARA QUÉ

| Necesidad | Usa |
|-----------|-----|
| Probar API interactivamente | **Swagger UI** (`/docs`) |
| Ver documentación clara | **ReDoc** (`/redoc`) |
| Compartir con equipo | **ReDoc** (`/redoc`) |
| Importar en Postman | **OpenAPI JSON** (`/openapi.json`) |
| Generar cliente Python/JS | **OpenAPI JSON** |
| Debugging rápido | **Swagger UI** |

---

## 📝 EJEMPLO: USAR SWAGGER UI

### Paso 1: Iniciar API
```bash
./start_api.sh
# Salida:
# ✅ Iniciando servidor...
# INFO:     Uvicorn running on http://127.0.0.1:8000
```

### Paso 2: Abrir navegador
```
Ir a: http://localhost:8000/docs
```

### Paso 3: Probar endpoint

```
1. Click en "POST /jobs/submit"
2. Click en "Try it out"
3. Rellenar datos:
   {
     "fasta_sequence": ">protein\nMKVLSPADKTNVK",
     "fasta_filename": "test.fasta",
     "gpus": 1,
     "cpus": 4,
     "memory_gb": 8,
     "max_runtime_seconds": 3600
   }
4. Click "Execute"
5. Ver respuesta:
   {
     "job_id": "job_1234567890",
     "status": "PENDING",
     "message": "Job submitted successfully"
   }
```

---

## 🔗 TODOS LOS ENDPOINTS

### Disponibles en ambas interfaces:

```
1. POST   /jobs/submit
   Enviar un trabajo

2. GET    /jobs/
   Listar todos los trabajos

3. GET    /jobs/{job_id}/status
   Ver estado de un trabajo

4. GET    /jobs/{job_id}/outputs
   Descargar resultados

5. GET    /jobs/{job_id}/accounting
   Ver uso de recursos
```

---

## 💾 IMPORTAR EN POSTMAN

Si prefieres usar Postman en lugar de Swagger:

### Método 1: URL directa
```
1. Abrir Postman
2. Click: Import
3. Paste link: http://localhost:8000/openapi.json
4. Click: Continue
5. Listo - Todos los endpoints importados
```

### Método 2: Descargar JSON
```bash
curl http://localhost:8000/openapi.json > cesga_api.json
# Abrir en Postman: Import > cesga_api.json
```

---

## 🐍 PYTHON CLIENTS EJEMPLO

Una vez la API está corriendo:

### Con httpx (sincrónico)
```python
import httpx

client = httpx.Client()
response = client.post(
    "http://localhost:8000/jobs/submit",
    json={
        "fasta_sequence": ">protein\nMKVLSPAD...",
        "fasta_filename": "test.fasta",
        "gpus": 1,
        "cpus": 4,
        "memory_gb": 8,
        "max_runtime_seconds": 3600
    }
)
print(response.json())
# {"job_id": "job_123...", "status": "PENDING"}
```

### Con requests (común)
```python
import requests

response = requests.post(
    "http://localhost:8000/jobs/submit",
    json={
        "fasta_sequence": ">protein\nMKVLSPAD...",
        "gpus": 1,
        "cpus": 4
    }
)
job_id = response.json()["job_id"]

# Consultar estado
status = requests.get(
    f"http://localhost:8000/jobs/{job_id}/status"
).json()
print(status)
```

### Con curl (quick test)
```bash
# Enviar trabajo
curl -X POST http://localhost:8000/jobs/submit \
  -H "Content-Type: application/json" \
  -d '{
    "fasta_sequence": ">protein\nMKVLSPAD",
    "gpus": 1,
    "cpus": 4,
    "memory_gb": 8,
    "max_runtime_seconds": 3600
  }'

# Respuesta:
# {"job_id":"job_1234567890","status":"PENDING","message":"Job submitted successfully."}

# Consultar estado
curl http://localhost:8000/jobs/job_1234567890/status
```

---

## 🎁 HERRAMIENTAS RECOMENDADAS

| Herramienta | Para Qué | Interfaz | Gratis |
|-------------|----------|----------|--------|
| **Swagger UI** | Probar API | Gráfica | ✅ Incluida |
| **Postman** | Testing avanzado | Gráfica | ✅ Gratis |
| **VS Code REST Client** | Pruebas rápidas | Texto | ✅ Gratis |
| **curl** | Command line | Terminal | ✅ Incluido |
| **Python httpx** | Scripts | Código | ✅ Gratis |

---

## 📊 EJEMPLOS DE USO CON SWAGGER

### Ejemplo 1: Enviar una proteína
```
1. Abrir: http://localhost:8000/docs
2. Expandir: "POST /jobs/submit"
3. "Try it out"
4. En "fasta_sequence" pegar:
   >ubiquitin
   MQIFVKTLTGKTITLEVESPDTIENVALVENAKAKTLVKILSQDPEAGSFSQRNETAVK
5. Dejar otros valores por defecto
6. "Execute"
7. Ver resultado: Job ID + status
```

### Ejemplo 2: Ver estado del trabajo
```
1. Abrir: http://localhost:8000/docs
2. Expandir: "GET /jobs/{job_id}/status"
3. "Try it out"
4. En "job_id" pegar el ID del paso anterior
5. "Execute"
6. Ver: status, created_at, started_at, etc.
```

### Ejemplo 3: Descargar resultados
```
1. Abrir: http://localhost:8000/docs
2. Expandir: "GET /jobs/{job_id}/outputs"
3. "Try it out"
4. En "job_id" pegar el ID
5. "Execute"
6. Ver: PDB file, confidence scores, biological data
```

### Ejemplo 4: Ver accounting
```
1. Abrir: http://localhost:8000/docs
2. Expandir: "GET /jobs/{job_id}/accounting"
3. "Try it out"
4. "Execute"
5. Ver: CPU-hours, GPU-hours, memory usage, cost
```

---

## ⌨️ ATAJOS ÚTILES EN SWAGGER

| Acción | Shortcut |
|--------|----------|
| Expandir/Cerrar todos | Click en "Expand all" |
| Buscar endpoint | Ctrl+F |
| Copiar curl | Click botón "Copy" |
| Probar directamente | Click "Try it out" |
| Limpiar datos | Click "Clear" |

---

## 🔍 TROUBLESHOOTING

### API no responde
```bash
# Verificar que está corriendo
curl http://localhost:8000/health

# Si falla, reiniciar:
# 1. Ctrl+C en terminal donde corre la API
# 2. ./start_api.sh
```

### "Cannot connect to localhost:8000"
```bash
# Verificar que puerto 8000 está libre
lsof -i :8000

# Si algo ocupa el puerto:
# Opción 1: Matar proceso
kill -9 <PID>

# Opción 2: Usar otro puerto
uvicorn app.main:app --port 8001
```

### Interfaz no carga
```bash
# Limpiar cache navegador
# Ctrl+Shift+Delete (Chrome/Firefox)
# Cmd+Shift+Delete (Mac Chrome)

# O abrir en modo incógnito
# Ctrl+Shift+N (Windows)
# Cmd+Shift+N (Mac)
```

---

## 📚 RECURSOS

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Swagger UI Docs](https://swagger.io/tools/swagger-ui/)
- [OpenAPI Spec](https://spec.openapis.org/)
- [ReDoc Docs](https://redoc.ly/)

---

## 🎯 RESUMEN RÁPIDO

```
API URL:      http://localhost:8000
Docs:         http://localhost:8000/docs (Swagger) ⭐
ReDoc:        http://localhost:8000/redoc
Health:       http://localhost:8000/health
Iniciar:      ./start_api.sh
```

**LA API TIENE INTERFAZ GRÁFICA LISTA PARA USAR. ¡ABRE SWAGGER Y PRUEBA!** 🚀
