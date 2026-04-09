#!/bin/bash

# Demo: Probar API sin interfaz gráfica (útil si no tienes navegador)

set -e

PROJECT_ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
cd "$PROJECT_ROOT"

# Colors
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  CESGA API - Demo (Sin interfaz gráfica)                 ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Activate venv
source venv/bin/activate

# Check if API is running
echo -e "${YELLOW}[1] Verificando que API está corriendo...${NC}"
if ! curl -s http://localhost:8000/health > /dev/null; then
    echo -e "${RED}✗ API no está corriendo${NC}"
    echo ""
    echo -e "${YELLOW}Inicia la API primero:${NC}"
    echo "  ./start_api.sh"
    echo ""
    exit 1
fi
echo -e "${GREEN}✓ API corriendo en localhost:8000${NC}"
echo ""

# Test health endpoint
echo -e "${YELLOW}[2] Health Check...${NC}"
curl -s http://localhost:8000/health | python -m json.tool
echo ""

# Submit a job
echo -e "${YELLOW}[3] Enviando trabajo de prueba...${NC}"
JOB_RESPONSE=$(curl -s -X POST http://localhost:8000/jobs/submit \
  -H "Content-Type: application/json" \
  -d '{
    "fasta_sequence": ">ubiquitin_test\nMQIFVKTLTGKTITLEVESPDTIENVALVENAKAKTLVKILSQDPEAGSFSQRNETAVKQ",
    "fasta_filename": "ubiquitin.fasta",
    "gpus": 1,
    "cpus": 8,
    "memory_gb": 32,
    "max_runtime_seconds": 7200
  }')

echo "$JOB_RESPONSE" | python -m json.tool
JOB_ID=$(echo "$JOB_RESPONSE" | python -c "import sys, json; print(json.load(sys.stdin)['job_id'])")
echo ""
echo -e "${GREEN}✓ Trabajo enviado con ID: $JOB_ID${NC}"
echo ""

# Wait a moment for job to start
sleep 2

# Check job status
echo -e "${YELLOW}[4] Verificando estado del trabajo...${NC}"
curl -s http://localhost:8000/jobs/$JOB_ID/status | python -m json.tool
echo ""

# List all jobs
echo -e "${YELLOW}[5] Listando todos los trabajos...${NC}"
JOBS=$(curl -s http://localhost:8000/jobs/)
echo "$JOBS" | python -m json.tool | head -50
echo ""

# Try to get outputs (might not be ready yet)
echo -e "${YELLOW}[6] Intentando obtener outputs...${NC}"
curl -s http://localhost:8000/jobs/$JOB_ID/outputs | python -m json.tool | head -30
echo ""

# Get accounting
echo -e "${YELLOW}[7] Información de accounting...${NC}"
curl -s http://localhost:8000/jobs/$JOB_ID/accounting | python -m json.tool
echo ""

echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  ✅ DEMO COMPLETADO - API FUNCIONA PERFECTAMENTE        ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}📊 ACCESO A INTERFACES GRÁFICAS:${NC}"
echo -e "   Swagger: ${YELLOW}http://localhost:8000/docs${NC}"
echo -e "   ReDoc:   ${YELLOW}http://localhost:8000/redoc${NC}"
echo ""
