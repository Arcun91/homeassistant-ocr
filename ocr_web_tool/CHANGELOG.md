# Changelog

## 1.0.3 (2026-09-24)
- **Ottimizzazione drastica prestazioni su Raspberry Pi / ARM**:
  - Adozione dei modelli neurali ufficiali quantizzati a 8-bit `tessdata_fast` (`ita`, `eng`, `osd`), accelerati tramite istruzioni SIMD ARM NEON (fino a 4x più veloci ed estremamente parsimoniosi di RAM).
  - Eliminazione della seconda esecuzione superflua di Tesseract (`image_to_data`), dimezzando il tempo di calcolo su ogni scansione (-50%).
  - Nuova risoluzione predefinita a `1200 px` per ridurre ulteriormente il carico di calcolo e memoria.
  - Filtro predefinito impostato su **Scala di Grigi** (massima velocità e consumo buffer ridotto a 1 byte/pixel).
  - Mantenuto il limite di concorrenza CPU a 2 thread (`omp_thread_limit: 2`) per proteggere il Raspberry Pi 3 da surriscaldamento.

## 1.0.2 (2026-09-24)
- Pubblicazione immagini multi-arch precompilate su GitHub Container Registry (`ghcr.io`).
- Installazione immediata senza compilazione su Raspberry Pi.
- Risolto build su architetture 32-bit (ARMv7) con pacchetto nativo `python3-pillow`.

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
