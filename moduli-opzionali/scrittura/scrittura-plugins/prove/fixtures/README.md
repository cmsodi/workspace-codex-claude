# Fixture di prova

Tutti i testi di questa cartella sono stati scritti da Claude per collaudare gli strumenti. Non sono campioni di autori reali e non servono a calibrare il ritmo.

- `it-origine.md`, `it-rivisto.md`: italiano, con tic di proposito. Gli output di riferimento in `../golden/` vengono dalla versione di `controlla.py` precedente alla generalizzazione.
- `en-buono.md`: inglese piano, senza tic voluti.
- `en-llm.md`: inglese con i tic tipici dei testi da LLM.
- `en-italianismi.md`: inglese con calchi dall'italiano, ortografia britannica e date non americane.
- `en-origine.md`, `en-rivisto-ok.md`, `en-rivisto-guasto.md`: coppia per il controllo di integrità (una riscrittura fedele e una che cambia numeri, nomi e cautele).
