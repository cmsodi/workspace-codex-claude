# italiano

Metodo in tre ruoli per ottenere un testo italiano corretto nei fatti e gradevole da leggere. È un plugin di Claude Code, e le sue istruzioni sono Markdown semplice, quindi le può seguire qualunque altro LLM (vedi `AGENTS.md`).

## I tre ruoli

| Skill | Ruolo | Che cosa fa | Può cambiare i fatti? | Obbligatoria |
|---|---|---|---|---|
| `/italiano:scrittore` | lo scrittore | Scrive di getto un testo completo da appunti, materiale o un argomento, poi lo leviga: corretto, chiaro, senza ripetizioni, pleonasmi, frasi contorte, doppie negazioni, frasi fatte. Nessuna pretesa di stile | Sì | Sì |
| `/italiano:verificatore` | il verificatore | Controlla che i dati siano corretti con la ricerca in rete, registra le fonti, assegna un esito a ogni affermazione, corregge e aggiunge con parsimonia | Sì | No |
| `/italiano:stilista` | lo stilista | Porta il testo a un italiano buono, piacevole, armonioso e scorrevole: riduce l'ampolloso, il barocco, il ridondante, spezza i periodi che affaticano senza cadere nello staccato, lega le frasi con i nessi (asciutto non vuol dire telegrafico) e mette le conclusioni dopo le ragioni | No, e non toglie informazione | Sì |

La sequenza è scrittore, poi verificatore se serve, poi stilista. Chi si occupa dei fatti non si occupa dello stile, e chi si occupa dello stile non può toccare i fatti né togliere informazione. *Asciutto* vuol dire senza fronzoli, mai riassunto.

Si entra dove serve: con del materiale si parte dallo scrittore; con un testo già scritto e corretto si può andare direttamente allo stilista.

## Uso in Claude Code

Il plugin sta nel marketplace locale `scrittura-local` (cartella `scrittura-plugins`, insieme al gemello `inglese`). Installazione, una volta:

```
claude plugin marketplace add /percorso/di/scrittura-plugins
claude plugin install italiano@scrittura-local
```

Poi:

```
/italiano:scrittore appunti.md
/italiano:verificatore input/miotesto/miotesto-1-stesura.md
/italiano:stilista testo.md riscrittura cerniere
```

Per i testi lunghi lo stilista lavora a pezzi con l'agente `italiano:stilista`, con approvazione a ogni passo; per le ricerche ampie il verificatore usa l'agente `italiano:verificatore`.

## Contenuto

- `skills/`: le tre skill.
- `agents/`: `verificatore` (ricerca in rete, contesto isolato) e `stilista` (lavoro a pezzi sui documenti lunghi).
- `riferimenti/contratto.md`: file di scambio, registro delle affermazioni, regole sui fatti, note e fonti.
- `riferimenti/diagnosi.md`: modello di buona prosa, ritmo, intoppi di lettura, tic degli LLM e degli autori umani, calchi dall'inglese, preferenze di stile dell'utente.
- `riferimenti/grammatica-italiana.md`: guida di grammatica normativa (materiale di terzi, vedi `riferimenti/NOTE-LEGALI.md`).
- `strumenti/controlla.py`: controlli di integrità (con ricerca di omissioni), struttura, ritmo, tic e scorrevolezza. Solo libreria standard di Python. Ha due profili di lingua (`--lingua it|en`); senza l'opzione vale `it`, e le skill di questo plugin lo usano così. È la stessa identica copia del plugin `inglese`.
- `strumenti/verifica_integrita.py`: controllo riga per riga dei pezzi (dal plugin `revisione`).

## Rapporto con `revisione`

Questo plugin raccoglie e sostituisce `revisione` (skill `rivedi` e `rivedi-bilingue`, agente `doc-reviewer`) per la parte italiana: ne riprende il flusso a pezzi con approvazione, il controllo d'integrità e i criteri contro i calchi. La parte in inglese americano e il confronto fra le due versioni di un documento sono nel plugin gemello `inglese` (`/inglese:stilista`, `/inglese:confronto`).

---

## Note

- Versione 0.1.0, bozza. Costruita su due prove (un articolo di divulgazione scientifica e l'Introduzione di un libro dell'utente) e verificata su un solo modello. Le soglie di ritmo sono ordini di grandezza ricavati da pochi testi.
- Licenza MIT, autore cms.
