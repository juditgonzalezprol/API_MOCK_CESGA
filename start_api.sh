#!/bin/bash

# Script para iniciar la API CESGA con interfaz gráfica
# Accede a http://localhost:8000/docs para ver la interfaz interactiva

set -e

PROJECT_ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
cd "$PROJECT_ROOT"

# Colors
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║    CESGA API - Iniciando Servidor con Interfaz Gráfica   ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Activate venv
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}⚠ Creando virtual environment...${NC}"
    python3 -m venv venv
fi

source venv/bin/activate

# Check if dependencies are installed
python -c "import fastapi" 2>/dev/null || {
    echo -e "${YELLOW}⚠ Instalando dependencias...${NC}"
    pip install -q fastapi uvicorn sqlalchemy pydantic pydantic-settings python-dotenv aiosqlite numpy
}

echo ""
echo -e "${GREEN}✅ Todo listo${NC}"
echo ""
echo -e "${BLUE}─────────────────────────────────────────────────────────────${NC}"
echo -e "${BLUE}INTERFAZ GRÁFICA DISPONIBLE IN:${NC}"
echo ""
echo -e "  📊 ${YELLOW}http://localhost:8000/docs${NC}"
echo -e "     (Swagger UI - Interfaz interactiva + testing)"
echo ""
echo -e "  📖 ${YELLOW}http://localhost:8000/redoc${NC}"
echo -e "     (ReDoc - Documentación clara)"
echo ""
echo -e "  🏥 ${YELLOW}http://localhost:8000/health${NC}"
echo -e "     (Health Check)"
echo ""
echo -e "${BLUE}─────────────────────────────────────────────────────────────${NC}"
echo ""
echo -e "${GREEN}Iniciando servidor...${NC}"
echo ""

# Start the API
uvicorn app.main:app --reload --port 8000 --host 127.0.0.1
