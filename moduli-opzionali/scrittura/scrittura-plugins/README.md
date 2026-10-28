# scrittura-plugins

Marketplace locale di Claude Code `scrittura-local`. Contiene due plugin gemelli per il metodo in tre ruoli (scrittore, verificatore, stilista):

- `italiano/`: testi italiani. Skill `/italiano:scrittore`, `/italiano:verificatore`, `/italiano:stilista`.
- `inglese/`: testi in inglese americano, istruzioni e rapporti in italiano. Skill `/inglese:scrittore`, `/inglese:verificatore`, `/inglese:stilista` e `/inglese:confronto` (confronto fra la versione italiana e quella inglese di un documento).

Il dettaglio di ciascun plugin è nel suo `README.md`.

## Installazione

Dalla radice di questo progetto:

```bash
claude plugin marketplace add .agents/scrittura-plugins
```

```bash
claude plugin install italiano@scrittura-local --scope user
```

```bash
claude plugin install inglese@scrittura-local --scope user
```

I plugin si caricano all'avvio di una sessione: dopo l'installazione, o dopo una modifica ai file, serve una nuova sessione. Essendo un marketplace di tipo cartella, Claude Code legge i plugin direttamente da queste cartelle (`claude plugin list` mostra «Read from»), quindi una modifica ai sorgenti vale dalla sessione successiva senza reinstallare. Nella cache di Claude (`~/.claude/plugins/cache/scrittura-local/`) resta una copia dell'installazione che la sessione non usa. Se un giorno il marketplace passasse su git, `claude plugin marketplace update scrittura-local` e `claude plugin update italiano@scrittura-local` porterebbero le modifiche nella copia installata.

## Struttura

```
.claude-plugin/marketplace.json     definizione del marketplace
italiano/                           plugin italiano
inglese/                            plugin inglese
prove/                              prove automatiche (non fanno parte dei plugin)
LICENSE                             MIT
```

`strumenti/controlla.py` è lo stesso file, identico byte per byte, in `italiano/` e in `inglese/` (ha due profili di lingua, `--lingua it|en`). Un plugin distribuito (da git o dalla cache) è copiato da solo e non può leggere file fuori dalla sua cartella, perciò la copia è inevitabile: la prova `CopieIdentiche` verifica che restino uguali. Se si modifica uno, si copia nell'altro e si rilancia la prova.

## Prove

```bash
python3 -I prove/test_controlla.py
```

Solo libreria standard. I testi in `prove/fixtures/` sono scritti da Claude per collaudare gli strumenti (non sono campioni di autori reali); in `prove/golden/` ci sono gli output di riferimento dell'italiano, per verificare che la generalizzazione a due lingue non lo abbia cambiato.

## Stato

Versione 0.1.0 di entrambi i plugin. Il ritmo inglese è calibrato provvisoriamente, in attesa di campioni di autori reali (vedi `inglese/riferimenti/diagnosi.md`, sezione 3).

## Licenza

MIT, autore cms.
