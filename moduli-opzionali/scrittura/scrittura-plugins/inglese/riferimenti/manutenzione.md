# Manutenzione dei lessici di tic

Ultimo aggiornamento dei lessici (`TIC_IT`, `TIC_EN`, `GRAPPOLO_IT`, `GRAPPOLO_EN` in `strumenti/controlla.py`): **2026-10-28** (costante `LESSICI_DATA`, stampata da `controlla.py tic-confronto`).

## Perché invecchiano

Le liste di tic fotografano le abitudini dei modelli e dei generi di scrittura che conosciamo. Ogni generazione di modelli ha le sue parole e le sue cadenze: alcune cadono, altre arrivano. Un lessico non datato dà una sicurezza che non ha. Le liste del plugin nascono da conoscenza generale dei testi da LLM, della prosa aziendale, accademica e giornalistica, e dal repertorio dei segni di scrittura automatica citato in `NOTE-LEGALI.md`. **Non sono state tarate su campioni di autori reali** e i fixture di `prove/` sono scritti da Claude: i test controllano che gli strumenti facciano ciò che dicono, non che le liste siano giuste.

## Quando rivederle

- quando si cambia il modello con cui si scrive o si rivede;
- circa ogni sei mesi;
- quando un testo nuovo mostra un tic non coperto, oppure uno strumento segnala a vuoto lo stesso passaggio in più testi puliti.

## Come aggiungere un tic

1. **Prova.** Almeno due occorrenze in testi reali, o nell'output di un modello, con data e modello annotati nel messaggio di commit.
2. **Famiglia.** Si sceglie una famiglia esistente o se ne crea una. Se la parola ha usi legittimi, l'etichetta dice «da valutare».
3. **Espressione.** Si scrive in `TIC_IT` o `TIC_EN` con `\b` e senza distinguere le maiuscole; nell'inglese l'ortografia è americana. Se è un indizio forte si aggiunge la famiglia a `GRAPPOLO_*`.
4. **Prove.** Un esempio nel fixture del catalogo (`en-segni-catalogo.md`, `it-segni-catalogo.md`), la prova che i testi puliti non lo attivano (`en-buono.md`, `en-non-segni.md`, `it-non-segni.md`, `en-riscritto.md`, `it-riscritto.md`) e un test in `prove/test_controlla.py`. Se un testo pulito supera il massimo di `Valutazione.PULITI`, o il massimo si alza, o l'espressione si restringe.
5. **Due copie.** `controlla.py` è lo stesso file nei plugin `italiano` e `inglese`: si copia dall'uno all'altro (un test controlla che coincidano).
6. **Data.** Si aggiorna `LESSICI_DATA` e, se serve, la nota in `diagnosi.md`.
7. **Controllo.** `python3 -I prove/test_controlla.py` passa per intero. L'output italiano dei golden non cambia, salvo una scelta dichiarata.

## Come ridurre o togliere un tic

Un falso positivo che si ripete su testi puliti si risolve restringendo l'espressione o passando l'etichetta a «da valutare». Un tic non si toglie solo perché i modelli recenti lo evitano: resta utile sui testi più vecchi e sulla prosa umana che lo usa. Se lo si toglie, il motivo va nel messaggio di commit.

## Soglie provvisorie

Non sono mai state calibrate su campioni di autori reali: ritmo in inglese (`PROFILI["en"]["ritmo"]`), densità di punteggiatura (`punteggiatura_di_pausa`), quota di capoversi senza ancoraggi (`concretezza`), chiusure a battuta, aperture ripetute, aperture secche, capoversi di lunghezza quasi costante e grassetto sparso. Vanno lette come «guarda meglio qui». Quando arriveranno i campioni, si misurano e si scrive qui il risultato.

## Che cosa non è

Il plugin non è un rilevatore di testi generati da IA e non cerca di eludere i rilevatori (vedi «Limiti d'uso» nel README).
