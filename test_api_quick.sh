#!/bin/bash

# Test rápido de la API CESGA
# Verifica que todo funcione correctamente sin descargar datos

set -e

PROJECT_ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
cd "$PROJECT_ROOT"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}CESGA API - Test Rápido${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check Python
echo -e "${YELLOW}[1/5] Verificando Python...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ Python3 no encontrado${NC}"
    exit 1
fi
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo -e "${GREEN}✓ Python ${PYTHON_VERSION}${NC}"
echo ""

# Check venv
echo -e "${YELLOW}[2/5] Verificando virtualenv...${NC}"
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}⚠ Creando virtualenv...${NC}"
    python3 -m venv venv
fi
source venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activado${NC}"
echo ""

# Check dependencies
echo -e "${YELLOW}[3/5] Verificando dependencias...${NC}"
python -c "
import sys
try:
    import fastapi
    import uvicorn
    import sqlalchemy
    import pydantic
    import numpy
    print('✓ Todas las dependencias instaladas')
except ImportError as e:
    print(f'✗ Falta: {e}')
    sys.exit(1)
" || {
    echo -e "${YELLOW}⚠ Instalando dependencias...${NC}"
    pip install -q fastapi uvicorn sqlalchemy pydantic pydantic-settings python-dotenv aiosqlite numpy
}
echo ""

# Test API imports
echo -e "${YELLOW}[4/5] Verificando API...${NC}"
python3 << 'EOF'
import sys
try:
    from app.main import app
    print(f"✓ API importada correctamente")
    print(f"  - Título: {app.title}")
    print(f"  - Versión: {app.version}")
    print(f"  - Rutas: {len([r for r in app.routes if r.path.startswith('/jobs')])}")
except Exception as e:
    print(f"✗ Error: {e}")
    sys.exit(1)
EOF
echo ""

# Test database
echo -e "${YELLOW}[5/5] Verificando base de datos...${NC}"
python3 << 'EOF'
import sqlite3
import os
from pathlib import Path
from app.database import engine

try:
    # Check if database can be created
    connection = engine.connect()
    connection.close()
    
    # Check if tables exist
    import sqlalchemy as sa
    inspector = sa.inspect(engine)
    tables = inspector.get_table_names()
    
    if 'jobs' in tables:
        print(f"✓ Base de datos OK")
        print(f"  - Tabla 'jobs' existe")
    else:
        print(f"⚠ Tabla 'jobs' no existe (se creará al iniciar)")
except Exception as e:
    print(f"✗ Error en DB: {e}")
EOF
echo ""

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}✅ API LISTA PARA USAR${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# Show quick start info
echo -e "${BLUE}Para iniciar la API:${NC}"
echo ""
echo -e "  source venv/bin/activate"
echo -e "  uvicorn app.main:app --reload --port 8000"
echo ""
echo -e "${BLUE}Luego acceder a:${NC}"
echo -e "  ${YELLOW}http://localhost:8000/docs${NC}  (Interactive API docs)"
echo -e "  ${YELLOW}http://localhost:8000/health${NC}  (Health check)"
echo ""

echo -e "${BLUE}Datos necesarios a descargar:${NC}"
echo -e "  Ver: ${YELLOW}DATOS_A_DESCARGAR.md${NC}"
echo ""

source venv/bin/activate
