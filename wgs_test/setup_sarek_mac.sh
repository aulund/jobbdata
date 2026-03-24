#!/bin/bash
# =============================================================
# Sarek WGS Pipeline Setup Script for Mac
# =============================================================
# Run this script on your Mac after transferring the wgs_test folder
#
# Prerequisites:
#   1. Install Docker Desktop: https://www.docker.com/products/docker-desktop/
#   2. Start Docker Desktop and make sure it's running
#   3. Allocate at least 8GB RAM to Docker (Preferences > Resources)
#
# Usage:
#   cd /path/to/wgs_test
#   chmod +x setup_sarek_mac.sh
#   ./setup_sarek_mac.sh
# =============================================================

set -e

echo "============================================="
echo "  Sarek WGS Pipeline Setup"
echo "============================================="

# --- Step 1: Check Docker ---
echo ""
echo "[1/4] Checking Docker..."
if ! command -v docker &> /dev/null; then
    echo "ERROR: Docker not found."
    echo "Install Docker Desktop from: https://www.docker.com/products/docker-desktop/"
    exit 1
fi

if ! docker info &> /dev/null; then
    echo "ERROR: Docker is not running. Please start Docker Desktop."
    exit 1
fi
echo "  ✓ Docker is running"

# --- Step 2: Install Nextflow ---
echo ""
echo "[2/4] Installing Nextflow..."
if command -v nextflow &> /dev/null; then
    echo "  ✓ Nextflow already installed: $(nextflow -version 2>&1 | head -3 | tail -1)"
else
    echo "  Installing Nextflow..."
    curl -s https://get.nextflow.io | bash
    sudo mv nextflow /usr/local/bin/
    echo "  ✓ Nextflow installed"
fi

# --- Step 3: Update samplesheet with absolute paths ---
echo ""
echo "[3/4] Configuring samplesheet..."
WORK_DIR="$(cd "$(dirname "$0")" && pwd)"

cat > "${WORK_DIR}/samplesheet.csv" << EOF
patient,sample,lane,fastq_1,fastq_2
patient1,ngs_test_01,lane_1,${WORK_DIR}/ngs_test_01_R1.fastq.gz,${WORK_DIR}/ngs_test_01_R2.fastq.gz
EOF
echo "  ✓ Samplesheet created with absolute paths"

# --- Step 4: Create run script ---
echo ""
echo "[4/4] Creating run script..."

cat > "${WORK_DIR}/run_sarek.sh" << 'RUNSCRIPT'
#!/bin/bash
set -e

WORK_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "${WORK_DIR}"

echo "============================================="
echo "  Running nf-core/sarek v3.8.1"
echo "============================================="
echo "  Input:  ${WORK_DIR}/samplesheet.csv"
echo "  Output: ${WORK_DIR}/results"
echo ""

# Run Sarek - germline variant calling with annotation
nextflow run nf-core/sarek -r 3.8.1 \
    -profile docker \
    --input "${WORK_DIR}/samplesheet.csv" \
    --outdir "${WORK_DIR}/results" \
    --genome GATK.GRCh38 \
    --tools haplotyper,strelka,snpeff,vep \
    --wes false \
    -resume

echo ""
echo "============================================="
echo "  Pipeline complete!"
echo "  Results in: ${WORK_DIR}/results"
echo "============================================="
RUNSCRIPT

chmod +x "${WORK_DIR}/run_sarek.sh"
echo "  ✓ Run script created"

# --- Done ---
echo ""
echo "============================================="
echo "  Setup complete!"
echo "============================================="
echo ""
echo "  Files you need to transfer to Mac:"
echo "    - ngs_test_01_R1.fastq.gz"
echo "    - ngs_test_01_R2.fastq.gz"
echo "    - samplesheet.csv"
echo "    - setup_sarek_mac.sh (this script)"
echo "    - run_sarek.sh (created by this script)"
echo ""
echo "  To run the pipeline:"
echo "    ./run_sarek.sh"
echo ""
echo "  The pipeline will:"
echo "    1. Align reads (BWA-MEM)"
echo "    2. Mark duplicates (GATK)"
echo "    3. Base quality recalibration (GATK)"
echo "    4. Call variants (HaplotypeCaller + Strelka)"
echo "    5. Annotate variants (SnpEff + VEP)"
echo "    6. Generate QC report (MultiQC)"
echo ""
echo "  Estimated runtime: 12-24h for 30x WGS"
echo "  Estimated disk: ~100GB for work + results"
echo "============================================="
