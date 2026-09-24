#!/usr/bin/env bash
set -e

echo "=========================================================="
echo " Starting OCR Web Tool Add-on for Home Assistant OS       "
echo "=========================================================="

OPTIONS_FILE="/data/options.json"

if [ -f "$OPTIONS_FILE" ]; then
    echo "[INFO] Reading configuration from ${OPTIONS_FILE}..."
    export DEFAULT_LANGUAGE=$(jq -r '.default_language // "ita"' "$OPTIONS_FILE")
    export TESSERACT_PSM=$(jq -r '.tesseract_psm // 3' "$OPTIONS_FILE")
    export TESSERACT_OEM=$(jq -r '.tesseract_oem // 3' "$OPTIONS_FILE")
    export MAX_UPLOAD_SIZE_MB=$(jq -r '.max_upload_size_mb // 20' "$OPTIONS_FILE")
    export MAX_IMAGE_DIMENSION=$(jq -r '.max_image_dimension // 1200' "$OPTIONS_FILE")
    export OMP_THREAD_LIMIT=$(jq -r '.omp_thread_limit // 2' "$OPTIONS_FILE")
else
    echo "[INFO] No ${OPTIONS_FILE} found. Using fallback environment variables / defaults."
    export DEFAULT_LANGUAGE="${DEFAULT_LANGUAGE:-ita}"
    export TESSERACT_PSM="${TESSERACT_PSM:-3}"
    export TESSERACT_OEM="${TESSERACT_OEM:-3}"
    export MAX_UPLOAD_SIZE_MB="${MAX_UPLOAD_SIZE_MB:-20}"
    export MAX_IMAGE_DIMENSION="${MAX_IMAGE_DIMENSION:-1200}"
    export OMP_THREAD_LIMIT="${OMP_THREAD_LIMIT:-2}"
fi

# Limita i thread OpenMP di Tesseract per evitare surriscaldamenti su Raspberry Pi
export OMP_THREAD_LIMIT="${OMP_THREAD_LIMIT}"

echo "[INFO] Configurazione attiva:"
echo "       - Lingua predefinita:     ${DEFAULT_LANGUAGE}"
echo "       - Tesseract PSM:          ${TESSERACT_PSM}"
echo "       - Tesseract OEM:          ${TESSERACT_OEM}"
echo "       - Limite upload:          ${MAX_UPLOAD_SIZE_MB} MB"
echo "       - Risoluzione max:        ${MAX_IMAGE_DIMENSION} px"
echo "       - Thread CPU limite:      ${OMP_THREAD_LIMIT}"

PORT="${PORT:-5000}"
echo "[INFO] Avvio server web Gunicorn sulla porta ${PORT} (0.0.0.0)..."

exec gunicorn \
    --bind "0.0.0.0:${PORT}" \
    --workers 1 \
    --threads 2 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    app:app
