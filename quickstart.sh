#!/bin/bash

################################################################################################
# CESGA API Simulator - Quick Start Script
# This script sets up and runs the complete API with real protein data integration
################################################################################################

set -e  # Exit on error

WORKSPACE="/Users/juditgonzalez/Desktop/API_CESGA"
cd "$WORKSPACE"

echo "🚀 CESGA API Simulator - Quick Start"
echo "===================================="
echo ""

# Color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Step 1: Environment Setup
echo -e "${BLUE}[1/6]${NC} Setting up Python environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✓${NC} Virtual environment created"
else
    echo -e "${GREEN}✓${NC} Virtual environment already exists"
fi

source venv/bin/activate

# Step 2: Install Dependencies
echo ""
echo -e "${BLUE}[2/6]${NC} Installing dependencies..."
pip install --quiet --upgrade pip > /dev/null 2>&1
pip install --quiet -r requirements.txt > /dev/null 2>&1
echo -e "${GREEN}✓${NC} Dependencies installed"

# Step 3: Initialize Database with Real Proteins
echo ""
echo -e "${BLUE}[3/6]${NC} Initializing database with real protein samples..."
rm -f cesga_simulator.db  # Start fresh
python scripts/init_db_real_proteins.py > /dev/null 2>&1

# Verify database was created
if [ -f "cesga_simulator.db" ]; then
    JOB_COUNT=$(sqlite3 cesga_simulator.db "SELECT COUNT(*) FROM jobs;")
    echo -e "${GREEN}✓${NC} Database initialized with $JOB_COUNT sample jobs"
else
    echo -e "❌ Database initialization failed"
    exit 1
fi

# Step 4: Generate Precomputed Structures
echo ""
echo -e "${BLUE}[4/6]${NC} Generating precomputed PDB structures..."
python scripts/generate_precomputed_structures.py > /dev/null 2>&1
PDB_COUNT=$(find app/mock_data/precomputed -name "*.pdb" 2>/dev/null | wc -l)
echo -e "${GREEN}✓${NC} Generated $PDB_COUNT precomputed PDB files"

# Step 5: Show API Info
echo ""
echo -e "${BLUE}[5/6]${NC} API Configuration:"
echo "    📍 URL: http://localhost:8000"
echo "    📚 Swagger UI: http://localhost:8000/docs"
echo "    📋 Real proteins: 6 (Ubiquitin, Insulin, Hemoglobin, Lysozyme, Amylase, Myoglobin)"
echo "    💾 Database: cesga_simulator.db"
echo ""

# Step 6: Start API Server
echo -e "${BLUE}[6/6]${NC} Starting API server..."
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📖 Documentation: http://localhost:8000/docs"
echo "🧬 Try these endpoints:"
echo ""
echo "   # Get sample ubiquitin job status"
echo "   curl http://localhost:8000/jobs/sample_ubiquitin/status"
echo ""
echo "   # Get outputs (wait for COMPLETED status first)"
echo "   curl http://localhost:8000/jobs/sample_ubiquitin/outputs | jq ."
echo ""
echo "   # Submit new job"
echo "   curl -X POST http://localhost:8000/jobs/submit \\"
echo "     -H 'Content-Type: application/json' \\"
echo "     -d '{\"fasta_sequence\": \">protein\\nMKVLS...\", ...}'"
echo ""
echo "  • Submit a job:  curl -X POST http://localhost:8000/jobs/submit \\"
echo "                         -H 'Content-Type: application/json' \\"
echo "                         -d '@example_job.json'"
echo "  • Check status:  curl http://localhost:8000/jobs/{job_id}/status"
echo "  • View all jobs: curl http://localhost:8000/jobs/"
echo
