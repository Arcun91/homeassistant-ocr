#!/usr/bin/env python3
"""
OCR Web Tool - Home Assistant Add-on
Backend Flask per l'estrazione OCR di testo da immagini e documenti PDF,
ottimizzato per Raspberry Pi (ARM) e architetture x86_64.
"""

import io
import json
import logging
import os
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from flask import Flask, jsonify, render_template, request
from PIL import Image, ImageEnhance, ImageOps
import pytesseract
from werkzeug.utils import secure_filename

# Supporto opzionale per documenti PDF
try:
    import pypdf
except ImportError:
    pypdf = None

try:
    import pdf2image
except ImportError:
    pdf2image = None

# Configurazione logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("ocr_web_tool")

# Inizializzazione Flask
app = Flask(__name__)

# Estensioni consentite
ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "webp", "bmp", "tiff", "tif"}
ALLOWED_DOCUMENT_EXTENSIONS = {"pdf"}
ALLOWED_EXTENSIONS = ALLOWED_IMAGE_EXTENSIONS | ALLOWED_DOCUMENT_EXTENSIONS

# Percorso file di opzioni di Home Assistant
OPTIONS_PATH = Path("/data/options.json")


def load_addon_config() -> dict:
    """Carica le opzioni dell'add-on da /data/options.json o dall'ambiente."""
    config = {
        "default_language": os.environ.get("DEFAULT_LANGUAGE", "ita"),
        "tesseract_psm": int(os.environ.get("TESSERACT_PSM", 3)),
        "tesseract_oem": int(os.environ.get("TESSERACT_OEM", 3)),
        "max_upload_size_mb": int(os.environ.get("MAX_UPLOAD_SIZE_MB", 20)),
        "max_image_dimension": int(os.environ.get("MAX_IMAGE_DIMENSION", 1200)),
        "omp_thread_limit": int(os.environ.get("OMP_THREAD_LIMIT", 2)),
    }

    if OPTIONS_PATH.is_file():
        try:
            with open(OPTIONS_PATH, "r", encoding="utf-8") as f:
                options = json.load(f)
                config.update(options)
                logger.info(f"Caricate opzioni da {OPTIONS_PATH}: {config}")
        except Exception as e:
            logger.warning(f"Impossibile leggere {OPTIONS_PATH}: {e}. Uso configurazione predefinita.")

    return config


APP_CONFIG = load_addon_config()

# Limite dimensione payload upload in byte
app.config["MAX_CONTENT_LENGTH"] = APP_CONFIG["max_upload_size_mb"] * 1024 * 1024


def allowed_file(filename: str) -> bool:
    """Verifica se l'estensione del file è tra quelle supportate."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def get_available_languages() -> List[str]:
    """Recupera le lingue disponibili installate in Tesseract."""
    try:
        langs = pytesseract.get_languages()
        # Filtra 'osd' se non rilevante
        return [l for l in langs if l != "osd"]
    except Exception as e:
        logger.warning(f"Errore lettura lingue Tesseract: {e}")
        return ["ita", "eng"]


def preprocess_image(
    img: Image.Image,
    mode: str = "grayscale",
    auto_rotate: bool = True,
    max_dim: int = 1200
) -> Image.Image:
    """
    Ottimizza e pre-processa l'immagine per massimizzare la precisione OCR
    e ridurre il consumo di memoria/CPU su Raspberry Pi.
    """
    # 1. Correzione orientamento tramite metadati EXIF (foto smartphone)
    if auto_rotate:
        try:
            img = ImageOps.exif_transpose(img)
        except Exception as e:
            logger.debug(f"Nessun orientamento EXIF o errore correzione: {e}")

    # 2. Ridimensionamento conservativo se l'immagine supera max_dim
    w, h = img.size
    if max(w, h) > max_dim:
        logger.info(f"Ridimensionamento immagine da {w}x{h} per ottimizzazione ARM (max {max_dim}px)")
        img.thumbnail((max_dim, max_dim), Image.Resampling.LANCZOS)

    # 3. Applicazione del filtro selezionato
    if mode == "none":
        return img

    # Conversione in scala di grigi
    gray = img.convert("L")

    if mode == "grayscale":
        return gray

    elif mode == "contrast":
        # Migliora contrasto dinamico e nitidezza dei caratteri
        contrasted = ImageOps.autocontrast(gray, cutoff=2)
        enhancer = ImageEnhance.Sharpness(contrasted)
        return enhancer.enhance(1.6)

    elif mode == "binarize":
        # Binarizzazione bianco/nero (Otsu-like via punto soglia con auto-contrasto)
        contrasted = ImageOps.autocontrast(gray, cutoff=2)
        # Soglia a 140
        return contrasted.point(lambda p: 255 if p > 140 else 0, mode="1")

    return gray


def extract_ocr_from_pil(
    pil_image: Image.Image,
    language: str,
    psm: int,
    oem: int
) -> Tuple[str, Optional[float]]:
    """
    Esegue OCR su una singola istanza PIL Image in modalità rapida (singolo passaggio).
    Dimezza il tempo di elaborazione evitando la seconda esecuzione superflua di Tesseract.
    """
    custom_config = f"--psm {psm} --oem {oem}"
    
    # Estrazione testo rapida e diretta
    text = pytesseract.image_to_string(pil_image, lang=language, config=custom_config)

    return text.strip(), None


def process_pdf_document(
    file_bytes: bytes,
    language: str,
    psm: int,
    oem: int,
    preprocess_mode: str = "grayscale",
    max_pages: int = 15
) -> Tuple[str, Optional[float], int]:
    """
    Estrae testo da documento PDF:
    - Tenta prima l'estrazione digitale diretta con pypdf (velocissima, 0 CPU).
    - In caso di PDF scansionato, rasterizza le pagine ed esegue OCR Tesseract.
    """
    total_pages = 0
    extracted_text_parts = []
    
    # Tentativo 1: Estrazione testo digitale vettoriale (PDF non scansionati)
    if pypdf:
        try:
            reader = pypdf.PdfReader(io.BytesIO(file_bytes))
            total_pages = len(reader.pages)
            pages_to_read = min(total_pages, max_pages)
            
            digital_texts = []
            for i in range(pages_to_read):
                page_text = reader.pages[i].extract_text() or ""
                if page_text.strip():
                    digital_texts.append(f"--- Pagina {i+1} ---\n{page_text.strip()}")
            
            # Se la maggior parte delle pagine ha testo digitale, lo usiamo direttamente
            if len(digital_texts) >= (pages_to_read // 2) and "".join(digital_texts).strip():
                logger.info(f"PDF con testo digitale estratto con successo ({len(digital_texts)} pagine)")
                full_text = "\n\n".join(digital_texts)
                return full_text, None, pages_to_read
        except Exception as e:
            logger.warning(f"Estrazione digitale PDF fallita, passo a OCR raster: {e}")

    # Tentativo 2: Rasterizzazione con pdf2image ed esecuzione OCR pagina per pagina
    if not pdf2image:
        raise RuntimeError("Modulo pdf2image non disponibile per rasterizzare PDF scansionati.")

    logger.info("Conversione pagine PDF in immagini per OCR...")
    # dpi=200 offre ottimo bilanciamento tra memoria ARM e risoluzione OCR
    images = pdf2image.convert_from_bytes(
        file_bytes,
        dpi=200,
        first_page=1,
        last_page=max_pages
    )
    total_pages = len(images)
    
    for idx, page_img in enumerate(images, start=1):
        processed_img = preprocess_image(page_img, mode=preprocess_mode)
        page_text, _ = extract_ocr_from_pil(processed_img, language, psm, oem)
        if page_text:
            extracted_text_parts.append(f"--- Pagina {idx} ---\n{page_text}")

    full_text = "\n\n".join(extracted_text_parts)
    return full_text, None, total_pages


@app.context_processor
def inject_template_globals():
    """Inietta variabili globali per Home Assistant Ingress e configurazione."""
    raw_ingress = request.headers.get("X-Ingress-Path", "").rstrip("/")
    return {
        "ingress_path": raw_ingress,
        "default_language": APP_CONFIG["default_language"],
        "max_size_mb": APP_CONFIG["max_upload_size_mb"],
        "version": "1.0.3"
    }


@app.route("/", methods=["GET"])
def index():
    """Pagina principale dell'applicazione web."""
    available_langs = get_available_languages()
    return render_template(
        "index.html",
        available_languages=available_langs,
        default_language=APP_CONFIG["default_language"]
    )


@app.route("/health", methods=["GET"])
def health():
    """Health check per monitoraggio contenitore."""
    return jsonify({"status": "ok", "app": "OCR Web Tool", "version": "1.0.3"})


@app.route("/api/status", methods=["GET"])
def api_status():
    """Restituisce informazioni su stato di Tesseract e configurazione attiva."""
    try:
        tess_version = str(pytesseract.get_tesseract_version())
    except Exception as e:
        tess_version = f"Non disponibile ({e})"

    return jsonify({
        "status": "ready",
        "tesseract_version": tess_version,
        "available_languages": get_available_languages(),
        "config": APP_CONFIG
    })


@app.route("/api/ocr", methods=["POST"])
def api_ocr():
    """Endpoint principale per l'upload e il riconoscimento OCR."""
    start_time = time.perf_counter()

    if "file" not in request.files:
        return jsonify({"success": False, "error": "Nessun file inviato nella richiesta."}), 400

    uploaded_file = request.files["file"]
    if uploaded_file.filename == "":
        return jsonify({"success": False, "error": "Nome file non valido o vuoto."}), 400

    filename = secure_filename(uploaded_file.filename)
    if not allowed_file(filename):
        ext = filename.rsplit(".", 1)[1] if "." in filename else ""
        return jsonify({
            "success": False,
            "error": f"Formato file '.{ext}' non supportato. Formati validi: {', '.join(sorted(ALLOWED_EXTENSIONS))}"
        }), 400

    # Parametri richiesta (con fallback a configurazione add-on)
    req_lang = request.form.get("language", APP_CONFIG["default_language"]).strip()
    req_psm = int(request.form.get("psm", APP_CONFIG["tesseract_psm"]))
    req_oem = int(request.form.get("oem", APP_CONFIG["tesseract_oem"]))
    preprocess_mode = request.form.get("preprocessing", "grayscale").strip()
    auto_rotate = request.form.get("auto_rotate", "true").lower() in ("true", "1", "yes")

    # Mappa lingua per Tesseract
    lang_map = {
        "ita": "ita",
        "eng": "eng",
        "ita+eng": "ita+eng",
        "eng+ita": "eng+ita"
    }
    tess_language = lang_map.get(req_lang, req_lang)

    try:
        file_bytes = uploaded_file.read()
        file_ext = filename.rsplit(".", 1)[1].lower() if "." in filename else ""

        if file_ext == "pdf":
            # Elaborazione documento PDF
            text, confidence, page_count = process_pdf_document(
                file_bytes=file_bytes,
                language=tess_language,
                psm=req_psm,
                oem=req_oem,
                preprocess_mode=preprocess_mode
            )
        else:
            # Elaborazione immagine standard (JPEG, PNG, WebP, ecc.)
            pil_img = Image.open(io.BytesIO(file_bytes))
            processed_img = preprocess_image(
                img=pil_img,
                mode=preprocess_mode,
                auto_rotate=auto_rotate,
                max_dim=APP_CONFIG["max_image_dimension"]
            )
            text, confidence = extract_ocr_from_pil(
                pil_image=processed_img,
                language=tess_language,
                psm=req_psm,
                oem=req_oem
            )
            page_count = 1

        duration = round(time.perf_counter() - start_time, 2)
        char_count = len(text)
        word_count = len(text.split())

        return jsonify({
            "success": True,
            "text": text,
            "confidence": confidence,
            "processing_time": duration,
            "char_count": char_count,
            "word_count": word_count,
            "page_count": page_count,
            "filename": filename,
            "language": req_lang,
            "preprocessing": preprocess_mode
        })

    except Exception as e:
        logger.error(f"Errore durante l'elaborazione OCR di '{filename}': {e}", exc_info=True)
        return jsonify({
            "success": False,
            "error": f"Errore durante l'elaborazione del file: {str(e)}"
        }), 500


@app.errorhandler(413)
def request_entity_too_large(error):
    """Gestione errore superamento limite dimensione file."""
    max_mb = APP_CONFIG["max_upload_size_mb"]
    return jsonify({
        "success": False,
        "error": f"Il file inviato supera il limite massimo consentito di {max_mb} MB."
    }), 413


if __name__ == "__main__":
    # Modalità standalone per test locali
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
