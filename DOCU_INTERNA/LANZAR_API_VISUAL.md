# 🚀 CÓMO LANZAR LA API CON INTERFAZ GRÁFICA

## Estado Actual
✅ API completamente funcional  
✅ 5 endpoints implementados  
✅ Base de datos creada  
✅ Interfaz gráfica lista  

---

## PASO 1: Abre una terminal

```bash
cd /Users/juditgonzalez/Desktop/API_CESGA
```

---

## PASO 2: Lanza la API

### Opción A (RECOMENDADA - Automática):
```bash
chmod +x start_api.sh
./start_api.sh
```

### Opción B (Manual):
```bash
source venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

---

## PASO 3: Verás esto en la terminal

```
INFO:     Uvicorn running on http://127.0.0.1:8000 [Ctrl+C to quit]
INFO:     Application startup complete
```

---

## PASO 4: En un navegador, entra en UNA de estas URLs

### 🏆 OPCIÓN 1: SWAGGER UI (LA MEJOR - Te recomiendo esta)
```
http://localhost:8000/docs
```

**La verás así:**

```
┌──────────────────────────────────────────────────────────┐
│  CESGA Supercomputer Simulator  v1.0  [Authorize] [X]   │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  POST /jobs/submit                              ▾       │
│  ├─ Request Body                               [Try it] │
│  │  {                                                   │
│  │    "fasta_sequence": "string",                     │
│  │    "fasta_filename": "string",                     │
│  │    "gpus": 0,                                      │
│  │    "cpus": 0,                                      │
│  │    "memory_gb": 0,                                 │
│  │    "max_runtime_seconds": 0                        │
│  │  }                                                  │
│  │                                                    │
│  │  [Ctrl+A] [Clear] [Execute]                       │
│  │                                                    │
│  ├─ Response 200                                       │
│  │  {                                                 │
│  │    "job_id": "string",                            │
│  │    "status": "PENDING",                           │
│  │    "created_at": "2024-01-15T10:30:00"           │
│  │  }                                                 │
│  │                                                    │
│  ├─ Response 422                                       │
│  │  {                                                 │
│  │    "detail": "string"                            │
│  │  }                                                 │
│  │                                                    │
│  GET /jobs/                                    ▾       │
│  GET /jobs/{job_id}/status                     ▾       │
│  GET /jobs/{job_id}/outputs                    ▾       │
│  GET /jobs/{job_id}/accounting                 ▾       │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

**Desde aquí puedes:**
- ✅ Ver todos los endpoints
- ✅ Leer la documentación
- ✅ **Probar directamente desde el navegador** (botón "Try it out")
- ✅ Ver ejemplos de requests y responses
- ✅ Copiar curl commands

---

### 📖 OPCIÓN 2: ReDoc (Documentación profesional)
```
http://localhost:8000/redoc
```

**Para:**
- Leer documentación detallada
- Compartir con el equipo
- Revisar especificaciones

---

### 🗂️ OPCIÓN 3: OpenAPI JSON (Para herramientas)
```
http://localhost:8000/openapi.json
```

**Para:**
- Importar en Postman
- Generar clientes automáticos
- Herramientas de testing

---

## EJEMPLO: Cómo probar un endpoint desde Swagger

### 1. Haz click en "POST /jobs/submit"
Se expande el formulario

### 2. Click en "Try it out"
El formulario se hace editable

### 3. En el cuadro de "Request Body", reemplaza el contenido con:

```json
{
  "fasta_sequence": ">ubiquitin\nMQIFVKTLTGKTITLEVESPDTIENVALVENAKAKTLVKILSQDPEAGSFSQRNETAVKQ",
  "fasta_filename": "ubiquitin.fasta",
  "gpus": 1,
  "cpus": 8,
  "memory_gb": 32,
  "max_runtime_seconds": 7200
}
```

### 4. Click en "Execute"
Verás la respuesta:

```json
{
  "job_id": "job_0c7f3d9e",
  "status": "PENDING",
  "created_at": "2024-01-15T10:30:00",
  "message": "Job submitted successfully"
}
```

### 5. Copia el `job_id`

### 6. Prueba GET /jobs/{job_id}/status
- Click en "GET /jobs/{job_id}/status"
- Click "Try it out"
- Pega el job_id en el parámetro
- Click "Execute"

Verás:
```json
{
  "job_id": "job_0c7f3d9e",
  "status": "RUNNING",
  "current_step": "Structure prediction in progress...",
  "progress": 45.5,
  "created_at": "2024-01-15T10:30:00"
}
```

---

## DATOS DISPONIBLES

Si quieres usar secuencias reales, tenemos en la BD:

1. **Ubiquitin** (76 aminoácidos)
```fasta
>ubiquitin
MQIFVKTLTGKTITLEVESD​PTIENDALLVDNAK​AKTLVKILSQDPEAGSFN
```

2. **Insulin** (51 aminoácidos)
```fasta
>insulin
GIVEQCCTSICSLYQLENYCN
```

3. **Hemoglobin** (146 aminoácidos α-chain)

Y muchas más en la base de datos...

**Para descargar más datos**, ver: [`DATOS_A_DESCARGAR.md`](DATOS_A_DESCARGAR.md)

---

## ATAJOS ÚTILES

| Tarea | URL |
|-------|-----|
| **Interfaz interactiva** | http://localhost:8000/docs |
| **Ver documentación** | http://localhost:8000/redoc |
| **Especificación técnica** | http://localhost:8000/openapi.json |
| **API base** | http://localhost:8000 |
| **Health check** | http://localhost:8000/health |

---

## PROBLEMAS COMUNES

### "¿Dónde está Swagger?"
→ Swagger *ES* la interfaz en `/docs`. No es una descarga, está automática en FastAPI.

### "La URL no abre"
1. ¿La terminal muestra "Application startup complete"? Si no, la API no está corriendo
2. ¿Escribiste `http://` y no `https://`? Debe ser http://
3. ¿Está en `localhost:8000` y no en otra IP? Por defecto es localhost

### "Veo error 404"
→ Probablemente escribiste mal la URL. Verifica:
- `http://localhost:8000/docs` ✅
- `http://localhost:8000/Docs` ❌
- `http://localhost:8000/docs/` ❌

---

## ALTERNATIVA: Demo sin navegador

Si no tienes navegador disponible:

```bash
chmod +x demo_api.sh
./demo_api.sh
```

Mostrará todos los endpoints probados via curl.

---

## SIGUIENTE

Una vez la API está corriendo:

1. **Juega con Swagger** - Prueba los endpoints
2. **Lee DATOS_A_DESCARGAR.md** - Entiende qué datos hay
3. **Mira CESGA_SCRIPTS.md** - Cómo enviar trabajos reales
4. **Intégra con tus scripts** - Usa los ejemplos de Python

---

## ¿NECESITAS AYUDA?

- API no arranca → Ver logs en la terminal
- Endpoint no funciona → Swagger muestra el error exacto
- ¿Cómo envío datos? → Swagger UI tiene ejemplos

**¡Todo está listo! 🚀**

Ahora solo necesitas:
```bash
./start_api.sh
```

Y luego ir a: http://localhost:8000/docs

