# 🔧 Logging Fix - SQLAlchemy Verbose Output SOLVED

## Problema Original ❌

**Síntomas**: Logs de SQLAlchemy inundando la terminal cada segundo:

```
2026-03-17 22:17:11,905 - sqlalchemy.engine.Engine - INFO - SELECT jobs.id...
2026-03-17 22:17:11,905 - sqlalchemy.engine.Engine - INFO - [cached since 500.7s ago] ('RUNNING',)
2026-03-17 22:17:11,905 - sqlalchemy.engine.Engine - INFO - SELECT jobs.id...
2026-03-17 22:17:11,905 - sqlalchemy.engine.Engine - INFO - [cached since 500.7s ago] ('PENDING',)
... (repitiendo 1000 veces)
```

**Causa**: Tres problemas combinados
1. SQLAlchemy loggers configurado con level INFO (mostraba todos los debug statements)
2. `echo=True` en los create_engine() calls (duplicaba los logs)
3. El logging suppression se hacía DESPUÉS de importar SQLAlchemy (muy tarde)

---

## Solución Implementada ✅

Se realizaron cambios en **3 archivos** de la API:

### 1. **`app/main.py`** - Suprimir logs al INICIO

**Cambio**: Moved suppression to VERY TOP before any imports

```python
import logging

# Suppress verbose SQLAlchemy logging BEFORE importing any SQLAlchemy modules
sqlalchemy_loggers = [
    "sqlalchemy.engine",
    "sqlalchemy.pool", 
    "sqlalchemy.dialects",
    "sqlalchemy.engine.Engine"
]
for _logger_name in sqlalchemy_loggers:
    logging.getLogger(_logger_name).setLevel(logging.WARNING)

# NOW import everything else (after suppression is in place)
import asyncio
from contextlib import asynccontextmanager
...
```

**Por qué funciona**: La suppression ocurre ANTES de que SQLAlchemy sea importado, así los loggers se crean con el nivel WARNING desde el inicio.

---

### 2. **`app/database.py`** - Desactivar echo=True

**Cambio globales**: Dos engines (sync y async)

```python
# Antes ❌
engine = create_engine(
    settings.database_url,
    echo=settings.debug,  # echo=True cuando debug=True
    ...
)

# Después ✅
engine = create_engine(
    settings.database_url,
    echo=False,  # Logging configuration controls verbosity
    ...
)
```

**Por qué**: `echo=True` hace que SQLAlchemy imprima cada query SQL. Con `echo=False`:
- Las queries NO se imprimen por echo
- Los loggers de SQLAlchemy controlan qué se muestra
- Configuración más limpia y estándar

---

### 3. **`app/background_tasks/job_scheduler.py`** - Same fix para el scheduler

```python
class JobScheduler:
    def __init__(self):
        # Antes ❌
        self.engine = create_engine(
            settings.database_url,
            echo=settings.debug,
            ...
        )
        
        # Después ✅
        self.engine = create_engine(
            settings.database_url,
            echo=False,  # Logging configuration controls verbosity
            ...
        )
```

**Por qué**: El scheduler tiene su PROPIO engine. Si no desactivamos echo aquí también, el scheduler seguiría mostrando SQL queries.

---

## Resultado Final ✅

### ANTES (Problema):
```
Terminal inundada con SQL queries cada segundo, imposible ver logs útiles
```

### DESPUÉS (Limpio):
```
INFO:     Uvicorn running on http://127.0.0.1:8000
2026-03-17 22:20:00 - app.main - INFO - Starting CESGA API Simulator...
2026-03-17 22:20:00 - app.main - INFO - Database: sqlite:///./cesga_simulator.db
2026-03-17 22:20:00 - app.main - INFO - Job state transitions:
2026-03-17 22:20:00 - app.main - INFO -   PENDING -> RUNNING: 5s
2026-03-17 22:20:00 - app.main - INFO -   RUNNING -> COMPLETED: 10s
2026-03-17 22:20:00 - app.background_tasks.job_scheduler - INFO - Starting job scheduler...
INFO:     Application startup complete.
```

**🎯 Solo logs útiles** - Sin ruido de SQLAlchemy

---

## Cómo Usar

La API sigue funcionando exactamente igual. Pero MUCHO más limpio:

```bash
cd /Users/juditgonzalez/Desktop/API_CESGA
source venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

O con el script automático:
```bash
./start_api.sh
```

---

## Niveles de Log (Para Referencia)

Si NECESITAS ver logs de SQLAlchemy (debugging):

1. **Para ver WARNING y ERROR** (Default):
   ```python
   logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
   ```

2. **Para ver INFO** (muchas queries):
   ```python
   logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
   ```

3. **Para ver TODO** (incluye DEBUG):
   ```python
   logging.getLogger("sqlalchemy.engine").setLevel(logging.DEBUG)
   ```

Edita `app/main.py` en la sección de SQLAlchemy suppression para cambiar este nivel.

---

## Resumen de Cambios

| Archivo | Cambio | Líneas |
|---------|--------|--------|
| `app/main.py` | Moved suppression to TOP, antes de imports | +11 lines, moved |
| `app/database.py` | `echo=True` → `echo=False` (2 engines) | 2 changes |
| `app/background_tasks/job_scheduler.py` | `echo=True` → `echo=False` (1 engine) | 1 change |

**Total: 3 archivos modificados, líneas mínimas, código más limpio** ✨

---

## Verificación

Para verificar que el fix funciona:

```bash
source venv/bin/activate
python3 -c "from app.main import app; print('✅ API imported successfully')"
```

Deberías ver el mensaje sin SQL queries.

---

## Notas Técnicas

- **Why supression at top?** Because logging.getLogger() creates loggers lazily, and if SQLAlchemy is already imported when we try to suppress, some handlers might already be attached.
  
- **Why echo=False?** The `echo` parameter in SQLAlchemy makes the engine ITSELF print SQL. We want the logging system to control verbosity, not SQLAlchemy's echo.

- **Why all three engines?** The app uses 3 SQLAlchemy engines:
  1. Sync engine in `database.py` - Main API
  2. Async engine in `database.py` - Alternative (not used currently)
  3. Sync engine in `job_scheduler.py` - Background tasks

All three needed fixing.


