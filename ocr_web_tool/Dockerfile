# Dockerfile per Add-on Home Assistant OS: OCR Web Tool
# Ottimizzato per architetture ARM (Raspberry Pi 3/4/5) e x86_64 (amd64)

FROM python:3.11-slim-bookworm

# Evita prompt interattivi e disabilita buffering stdout per log in tempo reale
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=5000 \
    OMP_THREAD_LIMIT=2

# Configura apt per forzare IPv4, aumentare i retry e il timeout DNS/HTTP.
# Risolve l'errore "Temporary failure resolving 'deb.debian.org'" su Docker e Home Assistant OS.
RUN echo 'Acquire::ForceIPv4 "true";' > /etc/apt/apt.conf.d/99force-ipv4 && \
    echo 'Acquire::Retries "5";' > /etc/apt/apt.conf.d/99retries && \
    echo 'Acquire::http::Timeout "30";' > /etc/apt/apt.conf.d/99timeout

# Installazione dei pacchetti di sistema necessari:
# - tesseract-ocr con modelli per italiano (ita) e inglese (eng)
# - poppler-utils per la conversione/estrazione da PDF
# - python3-pillow precompilato nativamente da Debian (risolve il build su armv7 a 32-bit)
# - jq per il parsing di options.json di Home Assistant
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    tesseract-ocr-ita \
    tesseract-ocr-eng \
    poppler-utils \
    python3-pillow \
    jq \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \
    && rm -rf /usr/share/doc/* /usr/share/man/* /usr/share/locale/*

# Directory di lavoro dell'applicazione
WORKDIR /app

# Copia e installazione delle dipendenze Python con ruote binarie precompilate
COPY requirements.txt /app/
RUN pip install --no-cache-dir --no-compile -r requirements.txt

# Copia dell'applicazione
COPY app.py /app/
COPY templates /app/templates/
COPY static /app/static/
COPY run.sh /run.sh

# Permessi di esecuzione per lo script di avvio
RUN chmod +x /run.sh

# Porta esposta predefinita
EXPOSE 5000

# Etichette di metadati per Home Assistant
LABEL io.hass.version="1.0.2" \
      io.hass.type="addon" \
      io.hass.arch="aarch64|amd64" \
      io.hass.name="OCR Web Tool" \
      io.hass.description="Applicazione web OCR leggera con Tesseract per immagini e PDF"

# Entrypoint tramite lo script di bootstrap dell'add-on
CMD ["/run.sh"]
