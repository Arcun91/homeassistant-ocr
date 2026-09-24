# Documentazione OCR Web Tool

## Introduzione
**OCR Web Tool** è un add-on leggero per Home Assistant OS che fornisce una comoda interfaccia web per l'estrazione ottica del testo (OCR) da immagini e documenti PDF.
È ottimizzato per l'architettura ARM (Raspberry Pi 3, 4, 5) e x86_64, con un consumo di memoria estremamente contenuto e supporto nativo sia per Home Assistant Ingress (accesso integrato nella barra laterale) sia per connessioni dirette HTTP (porta 5000) tramite LAN o reti VPN mesh come NetBird.

---

## Funzionalità Principali
- **Supporto multi-formato:** JPEG, PNG, WebP, BMP, TIFF e documenti **PDF** (digitali o scansionati).
- **Riconoscimento lingue:** Italiano (`ita`), Inglese (`eng`), o bilingue (`ita+eng`).
- **Mobile-friendly:** Interfaccia responsive con pulsante dedicato per **scattare una foto** direttamente dalla fotocamera dello smartphone.
- **Incolla da Appunti:** Supporto a `Ctrl+V` / `Cmd+V` per analizzare screenshot al volo.
- **Filtri di pre-elaborazione per Raspberry Pi:**
  - Correzione automatica orientamento EXIF (foto smartphone ruotate).
  - Ridimensionamento dinamico per limitare il carico CPU/RAM su ARM.
  - Auto-contrasto, nitidezza, scala di grigi e binarizzazione B/N per scontrini e fatture.
- **Risultati completi:** Testo estratto, stima della confidenza %, statistiche caratteri/parole, pulsante rapido **Copia negli appunti** e download come file `.txt`.

---

## Configurazione dell'Add-on

Nella scheda **Configurazione** dell'add-on su Home Assistant sono disponibili i seguenti parametri:

| Opzione | Predefinito | Descrizione |
|---|---|---|
| `default_language` | `ita` | Lingua OCR predefinita (`ita`, `eng`, `ita+eng`) |
| `tesseract_psm` | `3` | Page Segmentation Mode di Tesseract (3 = Completamente automatico) |
| `tesseract_oem` | `3` | OCR Engine Mode (3 = Predefinito basato su reti neurali LSTM) |
| `max_upload_size_mb` | `20` | Dimensione massima file in upload (MB) |
| `max_image_dimension` | `1200` | Dimensione massima (px) per ridimensionamento automatico |
| `omp_thread_limit` | `2` | Limite thread CPU Tesseract per evitare surriscaldamenti su Raspberry Pi |

---

## Modalità di Accesso

### 1. Tramite Home Assistant (Ingress)
Attiva l'opzione **"Mostra nella barra laterale"** nella pagina principale dell'add-on. Potrai accedere direttamente all'applicazione dalla barra laterale di Home Assistant senza dover autenticarti separatamente o aprire porte.

### 2. Tramite Rete Locale (LAN) o VPN Mesh (NetBird)
L'add-on espone la porta `5000` (configurabile nella scheda Rete):
- **Accesso LAN:** `http://homeassistant.local:5000` o `http://<IP_RASPBERRY>:5000`
- **Accesso NetBird VPN:** `http://<IP_NETBIRD_HA>:5000`
