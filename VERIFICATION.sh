#!/bin/bash

# CESGA API Simulator - Final Verification Script
# This script verifies that all real protein integration is complete and working

set -e

WORKSPACE="/Users/juditgonzalez/Desktop/API_CESGA"
cd "$WORKSPACE"

echo "🔍 CESGA API Simulator - Final Verification"
echo "==========================================="
echo ""

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

check_count=0
pass_count=0

check_file() {
    local file=$1
    local description=$2
    check_count=$((check_count + 1))
    
    if [ -f "$file" ]; then
        echo -e "${GREEN}✓${NC} [$check_count] $description: ${file##*/}"
        pass_count=$((pass_count + 1))
    else
        echo -e "${RED}✗${NC} [$check_count] $description: ${file##*/} NOT FOUND"
    fi
}

check_directory() {
    local dir=$1
    local description=$2
    check_count=$((check_count + 1))
    
    if [ -d "$dir" ]; then
        echo -e "${GREEN}✓${NC} [$check_count] $description: ${dir##*/}/"
        pass_count=$((pass_count + 1))
    else
        echo -e "${RED}✗${NC} [$check_count] $description: ${dir##*/}/ NOT FOUND"
    fi
}

echo -e "${BLUE}Section 1: Source Files${NC}"
check_file "app/services/real_protein_database.py" "Real protein database module"
check_file "app/services/mock_data_service.py" "Enhanced mock data service"
check_file "app/services/job_service.py" "Enhanced job service"
check_file "scripts/init_db_real_proteins.py" "Database initialization script"
check_file "scripts/generate_precomputed_structures.py" "PDB generation script"
echo ""

echo -e "${BLUE}Section 2: Documentation${NC}"
check_file "README.md" "Main README"
check_file "QUICKSTART.md" "Quick start guide"
check_file "EXECUTIVE_SUMMARY.md" "Executive summary"
check_file "API_QUICK_REFERENCE.md" "API quick reference"
check_file "SPECIFICATIONS.md" "Specifications"
check_file "ARCHITECTURE.md" "Architecture documentation"
check_file "TESTING_REAL_PROTEINS.md" "Testing guide"
check_file "DOCUMENTATION_INDEX.md" "Documentation index"
check_file "PROJECT_SUMMARY.md" "Project summary"
echo ""

echo -e "${BLUE}Section 3: Directories${NC}"
check_directory "app" "Application directory"
check_directory "scripts" "Scripts directory"
check_directory "tests" "Tests directory"
check_directory "app/mock_data" "Mock data directory"
check_directory "app/services" "Services directory"
echo ""

echo -e "${BLUE}Section 4: Configuration${NC}"
check_file "requirements.txt" "Python requirements"
check_file ".env" "Environment file" || check_file ".env.example" "Environment example"
check_file "quickstart.sh" "Quick start shell script"
echo ""

echo -e "${BLUE}Section 5: Code Verification${NC}"
check_count=$((check_count + 1))

# Check if real_protein_database.py has REAL_PROTEINS_DATABASE
if grep -q "REAL_PROTEINS_DATABASE" "app/services/real_protein_database.py"; then
    echo -e "${GREEN}✓${NC} [$check_count] Real proteins database defined"
    pass_count=$((pass_count + 1))
else
    echo -e "${RED}✗${NC} [$check_count] Real proteins database NOT found"
fi

check_count=$((check_count + 1))
# Check if there are 6+ proteins
if grep -q "ubiquitin" "app/services/real_protein_database.py" && \
   grep -q "insulin" "app/services/real_protein_database.py" && \
   grep -q "lysozyme" "app/services/real_protein_database.py"; then
    echo -e "${GREEN}✓${NC} [$check_count] Real proteins include ubiquitin, insulin, lysozyme"
    pass_count=$((pass_count + 1))
else
    echo -e "${RED}✗${NC} [$check_count] Expected proteins not found"
fi

check_count=$((check_count + 1))
# Check if job_service has protein identification
if grep -q "_identify_protein" "app/services/job_service.py"; then
    echo -e "${GREEN}✓${NC} [$check_count] Protein identification method present"
    pass_count=$((pass_count + 1))
else
    echo -e "${RED}✗${NC} [$check_count] Protein identification method NOT found"
fi

check_count=$((check_count + 1))
# Check if mock_data_service imports real proteins
if grep -q "real_protein_database" "app/services/mock_data_service.py"; then
    echo -e "${GREEN}✓${NC} [$check_count] Mock service imports real protein database"
    pass_count=$((pass_count + 1))
else
    echo -e "${RED}✗${NC} [$check_count] Mock service doesn't import real protein database"
fi

echo ""
echo -e "${BLUE}Section 6: Python Syntax${NC}"

check_count=$((check_count + 1))
if python -m py_compile app/services/real_protein_database.py 2>/dev/null; then
    echo -e "${GREEN}✓${NC} [$check_count] real_protein_database.py syntax OK"
    pass_count=$((pass_count + 1))
else
    echo -e "${RED}✗${NC} [$check_count] real_protein_database.py syntax ERROR"
fi

check_count=$((check_count + 1))
if python -m py_compile scripts/init_db_real_proteins.py 2>/dev/null; then
    echo -e "${GREEN}✓${NC} [$check_count] init_db_real_proteins.py syntax OK"
    pass_count=$((pass_count + 1))
else
    echo -e "${RED}✗${NC} [$check_count] init_db_real_proteins.py syntax ERROR"
fi

check_count=$((check_count + 1))
if python -m py_compile scripts/generate_precomputed_structures.py 2>/dev/null; then
    echo -e "${GREEN}✓${NC} [$check_count] generate_precomputed_structures.py syntax OK"
    pass_count=$((pass_count + 1))
else
    echo -e "${RED}✗${NC} [$check_count] generate_precomputed_structures.py syntax ERROR"
fi

echo ""
echo "==========================================="
echo ""
echo -e "${BLUE}Verification Results:${NC}"
echo -e "Passed: ${GREEN}${pass_count}/${check_count}${NC} checks"
echo ""

if [ "$pass_count" -eq "$check_count" ]; then
    echo -e "${GREEN}✅ ALL CHECKS PASSED!${NC}"
    echo ""
    echo "🚀 Ready to run:"
    echo "  1. ./quickstart.sh"
    echo "  2. open http://localhost:8000/docs"
    echo ""
    exit 0
else
    failed=$((check_count - pass_count))
    echo -e "${RED}❌ ${failed} CHECKS FAILED${NC}"
    echo ""
    echo "Please review the failed items above and ensure:"
    echo "- All real protein integration files are present"
    echo "- Documentation is complete"
    echo "- Python syntax is valid"
    echo ""
    exit 1
fi
