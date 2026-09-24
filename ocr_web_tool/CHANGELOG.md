# Changelog

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
