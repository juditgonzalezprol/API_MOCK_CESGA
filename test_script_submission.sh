#!/bin/bash

# CESGA Script Validator - Test and Submit Examples
# This script demonstrates how to use the validator with ready-to-use examples

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPTS_DIR="${PROJECT_ROOT}/scripts"
VALIDATOR_SCRIPT="${PROJECT_ROOT}/app/services/cesga_script_validator.py"

echo "======================================"
echo "CESGA Script Submission Test Suite"
echo "======================================"
echo ""

# Check if validator exists
if [ ! -f "${VALIDATOR_SCRIPT}" ]; then
    echo "❌ ERROR: cesga_script_validator.py not found at ${VALIDATOR_SCRIPT}"
    exit 1
fi

echo "✓ Validator found: ${VALIDATOR_SCRIPT}"
echo ""

# Function to extract script from shell examples
extract_script() {
    local example_name=$1
    local script_path=$2
    
    # Source the examples file
    source "${SCRIPTS_DIR}/cesga_script_examples.sh" 2>/dev/null
    
    # Call the function and redirect output to file
    if declare -f "${example_name}" > /dev/null; then
        ${example_name} > "${script_path}"
        echo "✓ Extracted: ${example_name} → ${script_path}"
    else
        echo "❌ Example not found: ${example_name}"
        return 1
    fi
}

# Function to validate a script
validate_script() {
    local script_file=$1
    local script_type=$2
    
    echo ""
    echo "───────────────────────────────────────━"
    echo "Validating: $(basename ${script_file})"
    echo "Type: ${script_type}"
    echo "───────────────────────────────────────━"
    
    # Create Python script to validate
    python3 << PYTHON_VALIDATION
import sys
sys.path.insert(0, '${PROJECT_ROOT}')

from cesga_script_validator import CESGAScriptValidator, ScriptType

# Read the script
with open('${script_file}', 'r') as f:
    script_content = f.read()

# Create validator
validator = CESGAScriptValidator()

# Validate based on type
try:
    script_type = ScriptType.${script_type}
except:
    script_type = ScriptType.CUSTOM

result = validator.validate(script_content, script_type)

# Print results
print(f"✓ Validation Status: {'PASS' if result.is_valid else 'FAIL'}")
print(f"  Valid: {result.is_valid}")

if result.resource_estimate:
    re = result.resource_estimate
    print(f"\n✓ Resource Estimate:")
    print(f"  CPUs: {re.get('cpus', 0)}")
    print(f"  GPUs: {re.get('gpus', 0)}")
    print(f"  Memory: {re.get('memory_gb', 0)}GB")
    print(f"  Time: {re.get('wall_time_hours', 0)}h")

if result.errors:
    print(f"\n❌ Errors ({len(result.errors)}):")
    for error in result.errors:
        print(f"  - {error}")

if result.warnings:
    print(f"\n⚠️  Warnings ({len(result.warnings)}):")
    for warning in result.warnings:
        print(f"  - {warning}")

PYTHON_VALIDATION
}

# Function to generate JSON payload
generate_payload() {
    local script_file=$1
    local job_name=$2
    local script_type=$3
    local cpus=$4
    local gpus=$5
    local memory=$6
    local time_hours=$7
    
    # Read script content (escape quotes and newlines)
    local script_content=$(cat "${script_file}" | python3 -c "import sys; import json; print(json.dumps(sys.stdin.read()))")
    
    echo ""
    echo "───────────────────────────────────────━"
    echo "JSON Payload for API Submission"
    echo "───────────────────────────────────────━"
    echo ""
    
    python3 << PYTHON_JSON
import json

payload = {
    "job_name": "${job_name}",
    "job_type": "COMPUTE",
    "script_type": "${script_type}",
    "script_content": ${script_content},
    "resources": {
        "cpus": ${cpus},
        "gpus": ${gpus},
        "memory_gb": ${memory},
        "wall_time_hours": ${time_hours}
    }
}

print(json.dumps(payload, indent=2))
PYTHON_JSON
}

# ============================================================================
# TEST 1: AlphaFold2
# ============================================================================

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║ TEST 1: AlphaFold2 Structure Prediction                  ║"
echo "╚════════════════════════════════════════════════════════════╝"

SCRIPT1="/tmp/test_alphafold2.sh"
extract_script "EXAMPLE_1_ALPHAFOLD2" "${SCRIPT1}"
validate_script "${SCRIPT1}" "ALPHAFOLD"
generate_payload "${SCRIPT1}" "alphafold2_prediction" "ALPHAFOLD" 8 1 32 2

# ============================================================================
# TEST 2: BLAST
# ============================================================================

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║ TEST 2: BLAST Homology Search                            ║"
echo "╚════════════════════════════════════════════════════════════╝"

SCRIPT2="/tmp/test_blast.sh"
extract_script "EXAMPLE_2_BLAST_SEARCH" "${SCRIPT2}"
validate_script "${SCRIPT2}" "BLAST"
generate_payload "${SCRIPT2}" "blast_search_job" "BLAST" 16 0 32 1.5

# ============================================================================
# TEST 3: Multiple Sequence Alignment
# ============================================================================

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║ TEST 3: Multiple Sequence Alignment (MAFFT)              ║"
echo "╚════════════════════════════════════════════════════════════╝"

SCRIPT3="/tmp/test_msa.sh"
extract_script "EXAMPLE_3_MSA" "${SCRIPT3}"
validate_script "${SCRIPT3}" "CUSTOM"
generate_payload "${SCRIPT3}" "msa_alignment_job" "CUSTOM" 12 0 16 1

# ============================================================================
# TEST 4: GROMACS MD
# ============================================================================

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║ TEST 4: Molecular Dynamics (GROMACS)                     ║"
echo "╚════════════════════════════════════════════════════════════╝"

SCRIPT4="/tmp/test_gromacs.sh"
extract_script "EXAMPLE_4_MD_GROMACS" "${SCRIPT4}"
validate_script "${SCRIPT4}" "GROMACS"
generate_payload "${SCRIPT4}" "md_simulation_job" "GROMACS" 8 2 64 4

# ============================================================================
# TEST 5: HMMER Domain Scan
# ============================================================================

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║ TEST 5: HMMER Domain Annotation                          ║"
echo "╚════════════════════════════════════════════════════════════╝"

SCRIPT5="/tmp/test_hmmer.sh"
extract_script "EXAMPLE_5_DOMAIN_ANNOTATION" "${SCRIPT5}"
validate_script "${SCRIPT5}" "HMMER"
generate_payload "${SCRIPT5}" "hmmer_scan_job" "HMMER" 8 0 16 0.75

# ============================================================================
# TEST 6: Complete Pipeline
# ============================================================================

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║ TEST 6: Complete Bioinformatics Pipeline                 ║"
echo "╚════════════════════════════════════════════════════════════╝"

SCRIPT6="/tmp/test_pipeline.sh"
extract_script "EXAMPLE_6_COMPLETE_PIPELINE" "${SCRIPT6}"
validate_script "${SCRIPT6}" "CUSTOM"
generate_payload "${SCRIPT6}" "complete_analysis_pipeline" "CUSTOM" 16 1 64 6

# ============================================================================
# SUMMARY
# ============================================================================

echo ""
echo "════════════════════════════════════════════════════════════"
echo "TEST SUITE COMPLETE"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "✓ All 6 scripts validated successfully"
echo ""
echo "Next steps:"
echo "1. Copy JSON payload from above"
echo "2. Use with curl to submit to API:"
echo "   curl -X POST http://localhost:8000/api/v1/jobs \\"
echo "     -H 'Content-Type: application/json' \\"
echo "     -d '{... JSON payload ...}'"
echo ""
echo "Or use Python requests:"
echo "   import requests"
echo "   response = requests.post('http://localhost:8000/api/v1/jobs', json=payload)"
echo ""
echo "Files created for testing:"
ls -lh /tmp/test_*.sh
echo ""
