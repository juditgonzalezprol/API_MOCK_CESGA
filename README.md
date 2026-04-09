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

Hay varias opciones según el contexto. Se explican de menos a más infraestructura.

---

### Opción A — ngrok (la más rápida, sin servidor)

Ideal para demos, hackathons o compartir la API temporalmente desde tu propio ordenador.

```bash
# 1. Instalar ngrok: https://ngrok.com/download
# En Mac con Homebrew:
brew install ngrok

# 2. Arrancar la API en local
uvicorn app.main:app --host 0.0.0.0 --port 8000

# 3. En otra terminal, exponer el puerto
ngrok http 8000
```

ngrok te dará una URL pública tipo `https://abc123.ngrok-free.app`. Esa URL funciona desde cualquier dispositivo con internet. El Swagger estará en `https://abc123.ngrok-free.app/docs`.

> **Limitación:** la URL cambia cada vez que reinicias ngrok (en el plan gratuito). Para URL fija, necesitas cuenta ngrok de pago o una de las opciones siguientes.

---

### Opción B — Railway (cloud, despliegue con git push)

Railway detecta automáticamente aplicaciones Python/FastAPI y las despliega sin configuración manual.

```bash
# 1. Instalar CLI de Railway
npm install -g @railway/cli    # o descarga desde https://railway.app

# 2. Login
railway login

# 3. Desde la carpeta del proyecto
railway init
railway up
```

Railway leerá el `Dockerfile` si existe (lo detecta automáticamente). La API quedará disponible en una URL tipo `https://tu-proyecto.railway.app`.

**Variables de entorno en Railway:** ve a Settings → Variables y añade las del `.env.example`. Como mínimo:

```
DEBUG=False
LOG_LEVEL=WARNING
PENDING_TO_RUNNING_DELAY=5
RUNNING_TO_COMPLETED_DELAY=5
```

> **Tier gratuito:** 500 horas/mes. Más que suficiente para desarrollo o hackathon.

---

### Opción C — Render (cloud, free tier)

```bash
# 1. Crea una cuenta en https://render.com

# 2. New → Web Service → conecta tu repositorio GitHub/GitLab

# 3. Configuración del servicio:
#    - Environment: Python 3
#    - Build command: pip install -r requirements.txt
#    - Start command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Render asignará un dominio tipo `https://tu-api.onrender.com`.

> **Importante en Render:** el servicio gratuito se "duerme" tras 15 min de inactividad. La primera petición tarda ~30 s en despertar. Para uso continuo usa el plan Starter ($7/mes) o activa un ping periódico con [UptimeRobot](https://uptimerobot.com/).

---

### Opción D — Fly.io

```bash
# 1. Instalar flyctl: https://fly.io/docs/hands-on/install-flyctl/

# 2. Login
fly auth login

# 3. Desde la carpeta del proyecto (usará el Dockerfile)
fly launch
# Acepta los valores por defecto o ajusta la región

# 4. Desplegar
fly deploy
```

La API quedará en `https://tu-app.fly.dev`. Fly.io tiene un tier gratuito generoso (3 VMs pequeñas, siempre activas).

---

### Opción E — VPS propio con Docker

Para despliegue en cualquier servidor Linux (DigitalOcean, Hetzner, OVH, AWS EC2, etc.).

#### 1. Instalar Docker en el servidor

```bash
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
```

#### 2. Copiar el proyecto al servidor

```bash
# Desde tu máquina local
scp -r API_CESGA/ usuario@IP_SERVIDOR:~/
# O con git:
ssh usuario@IP_SERVIDOR
git clone https://github.com/tu-usuario/API_CESGA.git
cd API_CESGA
```

#### 3. Configurar variables de entorno

```bash
cp .env.example .env
nano .env   # Edita según necesites
```

Para producción, modifica estas variables en `.env`:

```bash
DEBUG=False
LOG_LEVEL=WARNING
CORS_ORIGINS=["https://tu-frontend.com"]   # Restringe el CORS en producción
```

#### 4. Levantar con Docker Compose

```bash
docker compose up -d
```

La API escuchará en `http://IP_SERVIDOR:8000`.

#### 5. (Recomendado) Poner nginx delante con HTTPS

Instala certbot + nginx para tener HTTPS con certificado gratuito de Let's Encrypt:

```bash
sudo apt install nginx certbot python3-certbot-nginx
sudo certbot --nginx -d tu-dominio.com
```

Configuración nginx (`/etc/nginx/sites-available/cesga-api`):

```nginx
server {
    server_name tu-dominio.com;

    location / {
        proxy_pass         http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header   Host $host;
        proxy_set_header   X-Real-IP $remote_addr;
        proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header   X-Forwarded-Proto $scheme;
    }

    listen 443 ssl;
    # certbot rellenará los certificados aquí automáticamente
}

server {
    listen 80;
    server_name tu-dominio.com;
    return 301 https://$host$request_uri;
}
```

```bash
sudo ln -s /etc/nginx/sites-available/cesga-api /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
```

La API quedará en `https://tu-dominio.com` con HTTPS automático.

#### 6. Gestión de contenedores

```bash
# Ver logs en tiempo real
docker compose logs -f

# Parar
docker compose down

# Actualizar tras cambios en el código
docker compose build && docker compose up -d

# Ver estado
docker compose ps
```

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
