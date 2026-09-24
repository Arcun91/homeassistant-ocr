# Home Assistant Add-on: OCR Web Tool 📄🔍

Un Add-on personalizzato, moderno e leggero per **Home Assistant OS** che fornisce un'applicazione web completa di **OCR (Optical Character Recognition)** per l'estrazione di testo da immagini e documenti PDF.

Ottimizzato specificamente per girare in modo fluido su **Raspberry Pi (ARM)** e su macchine x86_64, con un'interfaccia responsive progettata per essere utilizzata comodamente anche da smartphone.

---

## 🌟 Caratteristiche Principali

- 🧠 **Motore OCR Avanzato:** Basato su **Tesseract 5** con modelli di reti neurali LSTM per lingua **Italiana (`ita`)** e **Inglese (`eng`)**.
- 📱 **Mobile-First & Scatto Diretto:** Pulsante dedicato per scattare foto direttamente dalla fotocamera dello smartphone (`capture="environment"`).
- 📋 **Supporto Appunti & Drag-and-Drop:** Trascina i file o incolla direttamente qualsiasi screenshot catturato con `Ctrl + V` / `Cmd + V`.
- 📑 **Supporto Documenti PDF:** Estrazione digitale istantanea per PDF nativi e rasterizzazione automatica per scansioni cartacee.
- ⚡ **Ottimizzato per Raspberry Pi (ARM):**
  - **Auto-orientamento EXIF:** raddrizza le foto scattate con smartphone prima dell'analisi.
  - **Filtri di pre-elaborazione intelligenti:** alto contrasto, binarizzazione netta B/N o scala di grigi.
  - **Downscaling adattivo:** limita l'impatto sulla RAM e sulla CPU ridimensionando immagini ad altissima risoluzione senza perdita di accuratezza.
  - **Limitazione thread CPU:** previene il surriscaldamento del processore sul Raspberry Pi.
- 🚀 **Integrazione Home Assistant Completa:**
  - **Ingress Nativo:** accessibile direttamente dalla barra laterale di Home Assistant con autenticazione integrata.
  - **Porta HTTP 5000 opzionale:** per accesso diretto in LAN o tramite VPN mesh (es. **NetBird**).
  - Statistiche immediate: tempo di elaborazione, percentuale di confidenza, conteggio caratteri e parole.
  - Tasto rapido **"Copia negli appunti"** con notifica visiva e download in formato `.txt`.

---

## 📁 Struttura della Repository GitHub

Affinché Home Assistant riconosca il progetto come un catalogo add-on valido, la repository deve rispettare questa struttura gerarchica:

```text
homeassistant-ocr/
├── repository.yaml             # Manifest del catalogo per l'Add-on Store di HA
├── README.md                   # Documentazione principale del progetto
├── docker-compose.yml          # Per test e sviluppo locale opzionale (senza HA)
├── .gitignore
└── ocr_web_tool/               # Cartella dell'add-on vero e proprio
    ├── config.yaml             # Configurazione add-on (porte, permessi, schema opzioni)
    ├── Dockerfile              # Immagine Docker multi-arch (Debian Slim + Tesseract)
    ├── run.sh                  # Script bash di avvio e lettura configurazione
    ├── requirements.txt        # Dipendenze Python (Flask, Pillow, pytesseract, pdf2image)
    ├── DOCS.md                 # Documentazione visibile all'interno di Home Assistant
    ├── CHANGELOG.md            # Registro delle versioni
    ├── icon.png                # Icona dell'add-on per l'interfaccia di HA
    ├── logo.png                # Logo ad alta risoluzione
    ├── app.py                  # Backend Flask e pipeline di pre-elaborazione OCR
    ├── templates/
    │   └── index.html          # Interfaccia grafica responsive
    └── static/
        ├── css/
        │   └── style.css       # Stili moderni (tema scuro/chiaro compatibile con HA)
        └── js/
            └── app.js          # Gestione interazioni, fotocamera, API e clipboard
```

> [!IMPORTANT]
> Il file [repository.yaml](file:///home/bob/Code/homeassistant-ocr/repository.yaml) posizionato nella cartella radice è obbligatorio: senza di esso, Home Assistant restituirà l'errore *"Invalid repository"* durante l'aggiunta dello store esterno.

---

## 🚀 Pubblicazione della Repository su GitHub

Se non hai ancora caricato il codice su GitHub, esegui questi passaggi dal terminale del tuo computer:

```bash
cd /home/bob/Code/homeassistant-ocr

# Inizializza il repository git locale
git init
git add .
git commit -m "Initial commit: OCR Web Tool Add-on for Home Assistant"

# Collega la tua repository remota GitHub
git branch -M main
git remote add origin https://github.com/Arcun91/homeassistant-ocr.git
git push -u origin main
```

*(Ricorda di aggiornare l'URL nel file [repository.yaml](file:///home/bob/Code/homeassistant-ocr/repository.yaml) e in [ocr_web_tool/config.yaml](file:///home/bob/Code/homeassistant-ocr/ocr_web_tool/config.yaml) inserendo il tuo URL GitHub reale).*

---

## 📦 Installazione su Home Assistant OS

Puoi installare l'add-on in due modi:

### Metodo 1: Aggiunta come Repository Esterna (Consigliato)

1. Apri la tua istanza di **Home Assistant** nel browser.
2. Vai su **Impostazioni (Settings)** > **Add-on**.
3. Clicca sul pulsante blu **Raccolta di Add-on (Add-on Store)** in basso a destra.
4. Clicca sui **tre puntini verticali (⋮)** in alto a destra e seleziona **Repository**.
5. Incolla l'URL della tua repository GitHub:
   ```text
   https://github.com/Arcun91/homeassistant-ocr
   ```
6. Clicca su **Aggiungi** e poi su **Chiudi**.
7. La pagina dello store si aggiornerà: troverai la sezione **"Home Assistant OCR Add-ons"** con all'interno **OCR Web Tool**.
8. Clicca sulla scheda dell'add-on e premi **Installa** (l'operazione impiegherà 1-2 minuti al primo avvio su Raspberry Pi per compilare/scaricare l'immagine Docker).
9. Al termine, attiva le levette:
   - **Avvia all'avvio (Start on boot)**
   - **Mostra nella barra laterale (Show in sidebar)** per accedere subito tramite Ingress.
10. Clicca su **Avvia (Start)**.

---

### Metodo 2: Installazione Locale Diretta (Senza GitHub)

Se preferisci testare l'add-on localmente senza passare da GitHub:

1. Installa l'add-on ufficiale **Samba Share** o **Terminal & SSH** su Home Assistant.
2. Copia l'intera cartella [ocr_web_tool](file:///home/bob/Code/homeassistant-ocr/ocr_web_tool) direttamente dentro la cartella condivisa `/addons/` del tuo Home Assistant (risultato: `/addons/ocr_web_tool/config.yaml`).
3. Vai in **Impostazioni** > **Add-on** > **Raccolta di Add-on**.
4. Clicca sui tre puntini in alto a destra e seleziona **Ricarica (Check for updates)**.
5. In cima allo store comparirà la sezione **"Add-on locali"** con **OCR Web Tool**.
6. Clicca e premi **Installa**.

---

## ⚙️ Opzioni di Configurazione

Dalla scheda **Configurazione** dell'add-on è possibile personalizzare i parametri:

```yaml
default_language: ita
tesseract_psm: 3
tesseract_oem: 3
max_upload_size_mb: 20
max_image_dimension: 2400
omp_thread_limit: 2
```

- **`default_language`**: Lingua predefinita (`ita`, `eng`, `ita+eng`).
- **`max_upload_size_mb`**: Limite di dimensione file in MB.
- **`max_image_dimension`**: Risoluzione massima in pixel oltre la quale l'immagine viene downscalata per risparmiare risorse sul Raspberry Pi (default: 2400px, ottimale per testo e scontrini).
- **`omp_thread_limit`**: Numero massimo di core CPU usati in parallelo da Tesseract (impostato su 2 per evitare picchi termici su Raspberry Pi privi di ventola attiva).

---

## 🔒 Accesso Sicuro e Configurazione Rete (LAN & VPN NetBird)

L'add-on supporta due canali di accesso paralleli:

### 1. Accesso tramite Home Assistant Ingress (Zero porte aperte)
- Se abiliti la voce **"Mostra nella barra laterale"**, l'applicazione comparirà nel menu laterale sinistro di Home Assistant.
- Le chiamate sono proxate internamente dal Supervisor di Home Assistant. Non serve esporre alcuna porta sul router e tutte le comunicazioni sono protette dalle credenziali e dalla 2FA del tuo account Home Assistant.

---

### 2. Accesso Diretto (Porta 5000) tramite VPN Mesh NetBird
Se desideri accedere direttamente all'interfaccia web dell'OCR da qualsiasi dispositivo esterno (smartphone fuori casa, PC dell'ufficio) senza passare per la dashboard di Home Assistant o se vuoi creare scorciatoie web indipendenti:

#### Perché usare una VPN Mesh come NetBird?
- **Nessun Port Forwarding:** Non devi aprire la porta 5000 sul router di casa verso Internet, evitando esposizioni a scansioni bot o vulnerabilità pubbliche.
- **Crittografia End-to-End:** Il traffico tra il tuo smartphone e il Raspberry Pi viaggia all'interno di un tunnel cifrato WireGuard punto-a-punto.

#### Procedura di configurazione:
1. **Configura NetBird su Home Assistant:**
   - Installa il client NetBird su Home Assistant OS (ad es. tramite l'add-on NetBird o configurato come router di sottorete nel tuo pannello NetBird).
   - Verifica l'indirizzo IP virtuale NetBird assegnato a Home Assistant (es. `100.64.0.15`).
2. **Mappatura della Porta nell'Add-on OCR:**
   - Nella pagina dell'add-on **OCR Web Tool**, vai nella scheda **Configurazione** > sezione **Rete**.
   - Assicurati che alla voce `5000/tcp` sia indicato il valore `5000` (porta host).
   - Salva e riavvia l'add-on.
3. **Connessione da Smartphone o Laptop:**
   - Attiva l'applicazione NetBird sul tuo smartphone o PC.
   - Apri il browser e naviga all'indirizzo:
     ```text
     http://100.64.0.15:5000
     ```
     *(Sostituisci `100.64.0.15` con l'IP NetBird effettivo del tuo Home Assistant)*.
4. **Restrizione degli Accessi con NetBird ACL:**
   - Dal dashboard web di amministrazione di NetBird, puoi creare una regola di controllo accessi (ACL) che consente il traffico verso la porta `5000` **esclusivamente** ai dispositivi fidati del tuo gruppo personale.

---

## 💻 Test Locale con Docker (Senza Home Assistant)

Se vuoi avviare e testare l'applicazione direttamente sul tuo computer con Docker:

```bash
cd /home/bob/Code/homeassistant-ocr
docker compose up --build
```

Una volta avviato il container, apri il browser all'indirizzo:
```text
http://localhost:5000
```

---

## 🛠️ Tecnologie Utilizzate

- **Backend:** Python 3.11, Flask, Gunicorn (multi-threaded).
- **Motore OCR:** Tesseract-OCR 5, Pytesseract, Poppler (`pdftoppm`).
- **Elaborazione Immagini:** Pillow (PIL) con filtri di contrasto dinamico e correzione EXIF.
- **Estrazione PDF:** PyPDF (estrazione vettoriale nativa) e pdf2image.
- **Frontend:** Vanilla HTML5, CSS3 responsive (design conforme a Home Assistant), Vanilla JavaScript (Clipboard API, FileReader API, Drag & Drop API).

---

## 📄 Licenza

Rilasciato sotto licenza MIT. Libero da utilizzare, modificare e distribuire.
