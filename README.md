# CESGA Supercomputer Simulator API

Simulador REST de la API del supercomputador CESGA Finis Terrae III. Imita el sistema de colas Slurm y el pipeline de predicción de estructuras proteicas con AlphaFold2 — sin necesitar acceso real al clúster ni GPUs.

Pensado para desarrollo de frontends, hackathons y pruebas de integración.

---

## Estructura del proyecto

```
API_CESGA/
│
├── app/                        # Código fuente principal
│   ├── main.py                 # Arranque FastAPI, CORS, lifespan
│   ├── config.py               # Configuración vía variables de entorno
│   ├── database.py             # SQLAlchemy (SQLite por defecto)
│   ├── models/
│   │   ├── db_models.py        # Modelo ORM de Job
│   │   └── schemas.py          # Schemas Pydantic (request/response)
│   ├── routers/
│   │   ├── jobs.py             # POST /jobs/submit, GET /jobs/{id}/...
│   │   └── proteins.py         # GET /proteins/ y /proteins/{id}
│   ├── services/
│   │   ├── job_service.py      # Lógica de negocio de jobs
│   │   ├── mock_data_service.py # Generación de PDB, pLDDT, PAE, logs
│   │   └── real_protein_database.py  # 22 proteínas curadas (UniProt)
│   ├── background_tasks/
│   │   └── job_scheduler.py    # Máquina de estados PENDING→RUNNING→COMPLETED
│   └── mock_data/
│       ├── precomputed/        # PDBs precomputados para proteínas conocidas
│       └── sample_results/     # Resultados generados en tiempo de ejecución
│
├── docs/
│   └── USER_GUIDE.md           # Guía de usuario completa (conceptos + endpoints)
│
├── scripts/                    # Utilidades de inicialización y generación de datos
│
├── Dockerfile                  # Imagen Docker para despliegue
├── docker-compose.yml          # Orquestación para desarrollo y producción
├── requirements.txt            # Dependencias Python
├── .env.example                # Plantilla de variables de entorno
└── start_api.sh                # Script de arranque local con venv
```

---

## Arranque local (desarrollo)

### Requisitos previos
- Python 3.9 o superior
- pip

### Pasos

```bash
# 1. Clonar o descargar el proyecto
cd API_CESGA

# 2. Crear entorno virtual e instalar dependencias
python3 -m venv venv
source venv/bin/activate          # En Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. Configurar variables de entorno
cp .env.example .env              # Edita .env si necesitas cambiar algún valor

# 4. Arrancar el servidor
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

O con el script incluido:

```bash
chmod +x start_api.sh
./start_api.sh
```

**URLs disponibles:**

| URL | Descripción |
|---|---|
| `http://localhost:8000` | Raíz de la API |
| `http://localhost:8000/docs` | Swagger UI (interfaz interactiva) |
| `http://localhost:8000/redoc` | ReDoc (documentación alternativa) |
| `http://localhost:8000/health` | Health check |

---

## Despliegue externo (acceso desde internet)

> **TL;DR — Recomendación directa:** usa **Railway Hobby ($5/mes)** o **Fly.io (~$4/mes)**. Son las únicas opciones que resuelven correctamente los tres requisitos críticos de este proyecto: SQLite persistente, sin hibernación, y RAM suficiente para numpy.
>
> Lee la sección de cada opción para entender por qué las demás no funcionan bien para esta app en concreto.

---

### Por qué importan estos tres requisitos

| Requisito | Por qué es crítico en esta API |
|---|---|
| **SQLite persistente** | La base de datos guarda todos los jobs. Si el contenedor se reinicia y no hay volumen persistente, se pierde todo el historial. |
| **Sin hibernación** | Si el servicio se "duerme" por inactividad, la primera petición tarda 15–60 segundos en responder. Eso rompe cualquier frontend que haga polling de estado. |
| **RAM ≥ 512 MB** | numpy (usado para generar matrices PAE y scores pLDDT) ocupa ~100–150 MB solo al importarse. Con FastAPI + SQLAlchemy, el proceso fácilmente supera 250 MB. |

---

### Opción A — ngrok (solo para demo en vivo, no para hosting)

ngrok **no es una plataforma de hosting**. Es un túnel que expone tu ordenador local a internet. La API sigue corriendo en tu máquina.

```bash
# 1. Instalar ngrok (Mac)
brew install ngrok

# 2. Arrancar la API en local
uvicorn app.main:app --host 0.0.0.0 --port 8000

# 3. En otra terminal, abrir el túnel
ngrok http 8000
# → Te da una URL pública: https://abc123.ngrok-free.app
```

**Cuándo usarlo:** presentación en un hackathon donde tú estás delante del ordenador y la demo dura 1–2 horas.

**Por qué NO sirve para hosting permanente:**

- ⚠️ El plan gratuito muestra una **página de advertencia interstitial** a quien visite la URL — esto rompe las llamadas directas de API desde un frontend JavaScript.
- La URL cambia cada vez que reinicias ngrok (plan gratuito). No hay URL fija.
- Si tu ordenador se apaga, se cierra el portátil o se va a dormir, la API desaparece.
- El plan gratuito tiene límite de 20.000 peticiones/mes.

---

### Opción B — Railway Hobby ($5/mes) ⭐ Recomendada

**La opción más sencilla** con los tres requisitos cubiertos. Railway detecta automáticamente proyectos Python/FastAPI y usa el `Dockerfile` incluido.

> **Nota sobre el tier gratuito de Railway:** el plan gratuito obliga a modo serverless (el app se duerme tras 10 min de inactividad). Además, el crédito gratuito es solo $1/mes tras el periodo de prueba inicial. Para uso real, el plan Hobby a $5/mes es necesario — y los $5 de crédito incluido cubren el coste de este app.

#### Pasos de despliegue

```bash
# 1. Instalar CLI
npm install -g @railway/cli

# 2. Login y conexión al proyecto
railway login
railway init      # la primera vez
# o railway link  # si ya tienes el proyecto creado en la web

# 3. Desplegar
railway up
```

Railway usará el `Dockerfile` automáticamente. En 2–3 minutos tendrás la API en `https://tu-proyecto.railway.app`.

#### Crear el volumen para SQLite (imprescindible)

En el dashboard de Railway: **tu servicio → Volumes → Add Volume**

- Mount path: `/app/data`
- Size: 1 GB (más que suficiente)

Luego actualiza la variable de entorno en Railway para apuntar la base de datos al volumen:

```
DATABASE_URL=sqlite:////app/data/cesga_simulator.db
```

#### Variables de entorno en Railway

Ve a **Settings → Variables** y añade:

```
DEBUG=False
LOG_LEVEL=WARNING
DATABASE_URL=sqlite:////app/data/cesga_simulator.db
PENDING_TO_RUNNING_DELAY=5
RUNNING_TO_COMPLETED_DELAY=5
CORS_ORIGINS=["*"]
```

#### Desactivar el modo serverless (importante)

En el dashboard: **tu servicio → Settings → Serverless → desactivar**. Así el app no se duerme nunca.

**Resumen Railway Hobby:**

| | |
|---|---|
| Precio | $5/mes (crédito de $5 incluido, app pequeña = ~$0 extra) |
| SQLite persistente | ✅ Con volumen montado |
| Hibernación | ❌ Desactivable con plan Hobby |
| RAM | 512 MB–8 GB (pay-per-use, ~$1.50/mes por 512 MB) |
| Complejidad de setup | Baja — CLI + dashboard web |

---

### Opción C — Fly.io (~$3.50–5.50/mes)

Fly.io es técnicamente excelente para este caso de uso: sin hibernación por defecto, volúmenes persistentes, y documentación oficial específica para SQLite. Algo más complejo de configurar que Railway.

> **Nota sobre el tier gratuito de Fly.io:** el tier gratuito fue **eliminado en octubre de 2024** para nuevos usuarios. Requiere tarjeta de crédito y es de pago desde el primer recurso creado.

#### Pasos de despliegue

```bash
# 1. Instalar flyctl
# Mac:
brew install flyctl
# Linux:
curl -L https://fly.io/install.sh | sh

# 2. Login
fly auth login

# 3. Desde la carpeta del proyecto (detecta el Dockerfile automáticamente)
fly launch
# Nombre: cesga-api (o el que quieras)
# Región: ams (Amsterdam) o mad (Madrid) para latencia mínima desde España
# No crear base de datos Postgres (usamos SQLite)

# 4. Crear volumen persistente para SQLite
fly volumes create cesga_data --size 1 --region ams

# 5. Editar fly.toml para montar el volumen
```

Añade esto al `fly.toml` generado:

```toml
[mounts]
  source = "cesga_data"
  destination = "/app/data"
```

```bash
# 6. Desplegar
fly deploy
```

#### Variables de entorno en Fly.io

```bash
fly secrets set DEBUG=False
fly secrets set LOG_LEVEL=WARNING
fly secrets set DATABASE_URL="sqlite:////app/data/cesga_simulator.db"
fly secrets set CORS_ORIGINS='["*"]'
```

**Resumen Fly.io:**

| | |
|---|---|
| Precio | ~$3.50–5.50/mes (VM 512 MB + 1 GB volumen) |
| SQLite persistente | ✅ Con volumen montado |
| Hibernación | ❌ Sin hibernación por defecto |
| RAM | 256 MB–2 GB (la de 256 MB es insuficiente para numpy — usa 512 MB) |
| Complejidad de setup | Media — flyctl CLI + editar fly.toml |

---

### Opción D — VPS propio con Docker (máximo control, ~$4/mes)

Para quien quiera control total. El VPS más barato del mercado (Hetzner CX11: €3.29/mes, 1 vCPU, 2 GB RAM) es más que suficiente para esta API.

#### 1. Preparar el servidor

```bash
# Conectar al VPS
ssh root@IP_SERVIDOR

# Instalar Docker
curl -fsSL https://get.docker.com | sh
usermod -aG docker $USER
```

#### 2. Copiar el proyecto

```bash
# Desde tu máquina local
scp -r API_CESGA/ usuario@IP_SERVIDOR:~/
# O con git si tienes el repo:
git clone https://github.com/tu-usuario/API_CESGA.git
cd API_CESGA
```

#### 3. Configurar variables de entorno

```bash
cp .env.example .env
nano .env
```

Cambios mínimos para producción:

```bash
DEBUG=False
LOG_LEVEL=WARNING
CORS_ORIGINS=["https://tu-frontend.com"]
```

#### 4. Levantar con Docker Compose

```bash
docker compose up -d
# La API escucha en http://IP_SERVIDOR:8000
```

#### 5. HTTPS con nginx + Let's Encrypt (muy recomendado)

```bash
apt install nginx certbot python3-certbot-nginx
certbot --nginx -d tu-dominio.com
```

Configuración nginx (`/etc/nginx/sites-available/cesga-api`):

```nginx
server {
    server_name tu-dominio.com;

    location / {
        proxy_pass         http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header   Host              $host;
        proxy_set_header   X-Real-IP         $remote_addr;
        proxy_set_header   X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header   X-Forwarded-Proto $scheme;
    }

    listen 443 ssl;  # certbot rellena aquí los certificados
}

server {
    listen 80;
    server_name tu-dominio.com;
    return 301 https://$host$request_uri;
}
```

```bash
ln -s /etc/nginx/sites-available/cesga-api /etc/nginx/sites-enabled/
nginx -t && systemctl reload nginx
```

#### 6. Gestión del contenedor

```bash
docker compose logs -f              # logs en tiempo real
docker compose down                 # parar
docker compose build && docker compose up -d   # actualizar tras cambios
docker compose ps                   # estado
```

**Resumen VPS:**

| | |
|---|---|
| Precio | ~$4/mes (Hetzner CX11 más barato del mercado) |
| SQLite persistente | ✅ Fichero en el disco del servidor |
| Hibernación | ❌ Nunca (servidor siempre encendido) |
| RAM | 2 GB (muy holgado) |
| Complejidad de setup | Alta — requiere administrar Linux, nginx, certbot |

---

### Comparativa final

| | ngrok (gratis) | Railway Hobby ($5/mes) | Fly.io (~$4/mes) | Render gratis | VPS Hetzner (~$4/mes) |
|---|---|---|---|---|---|
| ¿Requiere tarjeta? | No | Sí | Sí | Sí ($1 de pre-autorización) | Sí |
| SQLite persistente | ✅ (local) | ✅ Con volumen | ✅ Con volumen | ❌ **Se borra al reiniciar** | ✅ Disco del servidor |
| Sin hibernación | ❌ (depende de tu PC) | ✅ Desactivable | ✅ Por defecto | ❌ Duerme a los 15 min | ✅ Siempre activo |
| Cold start | N/A | ❌ Solo si hibernación ON | ❌ | ✅ **~60 segundos** | ❌ |
| RAM para numpy | Tu RAM | 512 MB–8 GB | 512 MB (mín. recomendado) | 512 MB | 2 GB |
| Simplicidad setup | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ |
| ¿Sirve para esta API? | Solo demos en vivo | ✅ **Sí** | ✅ **Sí** | ❌ No (sin disco persistente) | ✅ **Sí** |

> **Render gratuito queda descartado** para esta API: sin disco persistente, la base de datos SQLite se borra en cada reinicio o ciclo de hibernación. No hay forma de mantener los jobs entre sesiones.

**Recomendación por caso de uso:**
- **Hackathon / demo rápida (horas):** ngrok desde tu ordenador
- **Desarrollo compartido / hackathon de días:** Railway Hobby ($5/mes), setup en 15 minutos
- **Producción ligera con mínimo coste:** Fly.io (~$4/mes) o Hetzner VPS (~$4/mes)

---

## Variables de entorno — referencia completa

Todas se configuran en el fichero `.env` (copia de `.env.example`):

| Variable | Default | Descripción |
|---|---|---|
| `DATABASE_URL` | `sqlite:///./cesga_simulator.db` | URL de base de datos. SQLite para dev, PostgreSQL para prod |
| `DEBUG` | `True` | `False` en producción (desactiva recarga automática) |
| `LOG_LEVEL` | `INFO` | Nivel de log: `DEBUG`, `INFO`, `WARNING`, `ERROR` |
| `API_TITLE` | `CESGA Supercomputer Simulator` | Título que aparece en Swagger |
| `API_VERSION` | `1.0.0` | Versión de la API |
| `PENDING_TO_RUNNING_DELAY` | `5` | Segundos hasta que un job pasa de PENDING a RUNNING |
| `RUNNING_TO_COMPLETED_DELAY` | `5` | Segundos hasta que un job pasa de RUNNING a COMPLETED |
| `MAX_GPUS_PER_JOB` | `4` | Máximo de GPUs por job |
| `MAX_MEMORY_GB` | `256` | Máximo de RAM por job en GB |
| `MAX_CPUS_PER_JOB` | `64` | Máximo de CPUs por job |
| `CORS_ORIGINS` | `["*"]` | Orígenes permitidos. Restringe en producción |

---

## Endpoints — resumen

```
GET  /                         →  Info de la API
GET  /health                   →  Health check
GET  /docs                     →  Swagger UI

POST /jobs/submit              →  Enviar nuevo job (acepta FASTA)
GET  /jobs/                    →  Listar todos los jobs
GET  /jobs/{id}/status         →  Estado: PENDING / RUNNING / COMPLETED / FAILED
GET  /jobs/{id}/outputs        →  Resultados: PDB, mmCIF, pLDDT, PAE, datos biológicos
GET  /jobs/{id}/accounting     →  Contabilidad HPC: CPU-hours, GPU-hours, eficiencia

GET  /proteins/                →  Catálogo de proteínas (con filtros)
GET  /proteins/stats           →  Estadísticas de la base de datos
GET  /proteins/samples         →  Secuencias FASTA de ejemplo listas para copiar
GET  /proteins/{protein_id}    →  Detalles + FASTA de una proteína concreta
```

Ver la documentación completa para usuarios en [`docs/USER_GUIDE.md`](docs/USER_GUIDE.md).

---

## Stack técnico

| Componente | Tecnología | Versión |
|---|---|---|
| Framework | FastAPI | 0.104 |
| Servidor ASGI | Uvicorn | 0.24 |
| ORM | SQLAlchemy | 2.0 |
| Base de datos | SQLite (dev) / PostgreSQL (prod) | — |
| Validación | Pydantic v2 | 2.5 |
| Contenedores | Docker + Compose | — |
