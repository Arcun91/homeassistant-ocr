# Changelog

## 1.0.1 (2026-09-24)
- Risolto errore DNS e IPv6 (`Temporary failure resolving 'deb.debian.org'`) forzando IPv4 e timeout su apt.
- Corretta la sintassi degli intervalli numerici in `config.yaml` (`int(min,max)` invece di `..`).
- Rimosso `webui` ridondante in favore della gestione nativa Ingress.
- Ottimizzato il consumo di RAM: ridotto Gunicorn a 1 singolo worker a riposo.
- Snellito il Dockerfile con rimozione documentazione/man pages e `--no-compile` per ridurre le scritture su MicroSD del Raspberry Pi.
- Aggiunto `repository.json` e file di traduzioni `translations/en.yaml`.

## 1.0.0 (2026-09-24)
- Versione iniziale di OCR Web Tool per Home Assistant OS.
- Motore Tesseract 5 con supporto modelli neurali per lingua italiana (`ita`) e inglese (`eng`).
- Interfaccia web responsive ottimizzata per browser desktop e mobile.
- Supporto cattura diretta da fotocamera smartphone (`capture="environment"`).
- Supporto incollamento rapido screenshot da tastiera (`Ctrl+V` / `Cmd+V`).
- Supporto documenti PDF (estrazione vettoriale rapida o rasterizzazione scansioni).
- Integrazione completa con Home Assistant Ingress e mappatura porta `5000/tcp`.
- Pulsante rapido copia negli appunti e download `.txt`.
- Ottimizzazioni per Raspberry Pi (limite thread OpenMP, ridimensionamento dinamico immagini grandi, pre-elaborazione a basso impatto).
