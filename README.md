# OCR Web Tool - Home Assistant Add-on

[![Home Assistant Add-on](https://img.shields.io/badge/Home%20Assistant-Add--on-blue.svg)](https://www.home-assistant.io/)
[![Architectures](https://img.shields.io/badge/arch-aarch64%20%7C%20amd64%20%7C%20armv7%20%7C%20armhf-brightgreen.svg)]()
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.0.0-orange.svg)]()

Un Add-on leggero e reattivo per **Home Assistant OS** che fornisce un'applicazione web completa per il riconoscimento ottico dei caratteri (**OCR**), consentendo l'estrazione rapida e accurata di testo da immagini, scontrini, fatture e documenti PDF.

Progettato specificamente per girare in modo efficiente su **Raspberry Pi (architetture ARM)** e sistemi x86_64, con un'interfaccia minimale ottimizzata per l'uso sia da desktop che da smartphone.

---

## Caratteristiche

- **Motore OCR Neurale:** Basato su **Tesseract 5** con modelli LSTM per lingua **Italiana (`ita`)** e **Inglese (`eng`)**, combinabili (`ita+eng`).
- **Mobile-First & Scatto Diretto:** Pulsante dedicato per scattare una foto direttamente dalla fotocamera dello smartphone (`capture="environment"`).
- **Incolla da Appunti & Drag-and-Drop:** Trascina immagini nel riquadro o incolla direttamente qualsiasi screenshot catturato con `Ctrl + V` / `Cmd + V`.
- **Supporto Documenti PDF:** Estrazione diretta istantanea del testo vettoriale per PDF digitali e rasterizzazione pagina per pagina per scansioni cartacee.
- **Ottimizzazioni per Raspberry Pi (ARM):**
  - **Auto-orientamento EXIF:** Corregge automaticamente l'orientamento delle foto scattate con smartphone prima dell'analisi.
  - **Filtri di Pre-elaborazione:** Auto-contrasto dinamico, aumento della nitidezza, scala di grigi e binarizzazione B/N per scontrini o testo a basso contrasto.
  - **Downscaling Adattivo:** Ridimensiona immagini con risoluzioni eccessive (oltre 2400px) per prevenire picchi di RAM e velocizzare l'elaborazione su ARM.
  - **Controllo Termico CPU:** Limita i thread OpenMP di Tesseract per evitare surriscaldamenti del processore su sistemi privi di raffreddamento attivo.
- **Integrazione Home Assistant:**
  - Supporto nativo **Ingress** con accesso diretto dalla barra laterale di Home Assistant senza dover aprire porte sul router.
  - Porta `5000/tcp` opzionale per connessioni dirette in rete locale (LAN) o tramite reti mesh VPN (es. **NetBird**).
  - Tasto rapido **"Copia"** con notifica visiva e download del testo estratto in formato `.txt`.

---

## Installazione

1. In Home Assistant, recarsi su **Impostazioni** > **Add-on** > **Raccolta di Add-on**.
2. Cliccare sui **tre puntini in alto a destra (⋮)** e selezionare **Repository**.
3. Aggiungere l'URL del repository:
   ```text
   https://github.com/Arcun91/homeassistant-ocr
   ```
4. Cercare **OCR Web Tool** all'interno dello store e cliccare su **Installa**.
5. Al termine dell'installazione:
   - Attivare l'opzione **Mostra nella barra laterale** per un accesso rapido.
   - Cliccare su **Avvia**.

---

## Modalità di Accesso

### 1. Barra Laterale di Home Assistant (Ingress)
Accedendo tramite la voce **OCR Tool** nella barra laterale di Home Assistant:
- Il traffico viene instradato e autenticato internamente dal Supervisor.
- Non è richiesta alcuna apertura di porte verso l'esterno.

### 2. Accesso Diretto (Porta 5000) via LAN o VPN NetBird
Se si desidera aprire l'interfaccia web direttamente nel browser senza passare dalla dashboard di Home Assistant:
- Verificare che nella scheda **Configurazione** (sezione **Rete**) dell'add-on la porta host `5000` sia assegnata.
- **In rete locale:** `http://<IP_HOME_ASSISTANT>:5000`
- **Tramite VPN Mesh (NetBird):** `http://<IP_NETBIRD_DI_HA>:5000`  
  *(Consente l'accesso sicuro e crittografato end-to-end WireGuard da qualsiasi luogo, senza dover esporre alcuna porta sul router)*.

---

## Configurazione

Le seguenti opzioni possono essere personalizzate nella scheda **Configurazione** dell'add-on:

| Parametro | Tipo | Predefinito | Descrizione |
|---|---|---|---|
| `default_language` | `list` | `ita` | Lingua OCR predefinita (`ita`, `eng`, `ita+eng`). |
| `tesseract_psm` | `int` | `3` | Page Segmentation Mode (3 = completamente automatico). |
| `tesseract_oem` | `int` | `3` | OCR Engine Mode (3 = motore predefinito basato su reti neurali LSTM). |
| `max_upload_size_mb` | `int` | `20` | Dimensione massima ammessa per i file caricati (in megabyte). |
| `max_image_dimension` | `int` | `2400` | Dimensione massima in pixel per il ridimensionamento automatico delle immagini. |
| `omp_thread_limit` | `int` | `2` | Numero massimo di thread CPU assegnati a Tesseract per salvaguardare le temperature di Raspberry Pi. |

---

## Architettura e Tecnologie

- **Sistema Base:** Debian 12 (Bookworm Slim) multi-architettura.
- **Motore OCR:** Tesseract OCR 5 con pacchetti linguistici `tesseract-ocr-ita` e `tesseract-ocr-eng`.
- **Backend:** Python 3.11, Flask, Gunicorn (server WSGI multi-worker/multi-thread), Pillow (PIL), PyPDF e Poppler Utilities.
- **Frontend:** Vanilla HTML5, CSS3 responsive (tema dinamico chiaro/scuro in linea con lo stile di Home Assistant), Vanilla JavaScript (Web APIs per Clipboard, Drag & Drop e Camera Capture). Zero dipendenze da CDN esterne (funziona al 100% offline in LAN).

---

## Licenza

Distribuito sotto licenza **MIT**. Consultare il file `LICENSE` per ulteriori informazioni.
