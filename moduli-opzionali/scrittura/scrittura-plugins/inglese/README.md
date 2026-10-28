# inglese

Metodo in tre ruoli per ottenere un testo in **inglese americano** corretto nei fatti e gradevole da leggere. Istruzioni, note e rapporti sono in italiano; i testi trattati sono in inglese. È il gemello del plugin `italiano` (stessi ruoli, stesse regole sui fatti), con la diagnosi, le convenzioni e gli strumenti adattati all'inglese. È un plugin di Claude Code, e le sue istruzioni sono Markdown semplice, quindi le può seguire qualunque altro LLM (vedi `AGENTS.md`).

## I tre ruoli

| Skill | Ruolo | Che cosa fa | Può cambiare i fatti? | Obbligatoria |
|---|---|---|---|---|
| `/inglese:scrittore` | lo scrittore | Scrive di getto un testo inglese completo da appunti, materiale (anche italiano) o un argomento, poi lo leviga: corretto, chiaro, senza ripetizioni, frasi contorte, doppie negazioni, frasi fatte, calchi dall'italiano. Nessuna pretesa di stile | Sì | Sì |
| `/inglese:verificatore` | il verificatore | Controlla che i dati siano corretti con la ricerca in rete, registra le fonti, assegna un esito a ogni affermazione, corregge e aggiunge con parsimonia | Sì | No |
| `/inglese:stilista` | lo stilista | Porta il testo a un inglese buono, piacevole e scorrevole: voce attiva con giudizio, verbi al posto delle nominalizzazioni, niente tic da LLM, niente corporate-speak, niente calchi; spezza i periodi che affaticano senza cadere nello staccato | No, e non toglie informazione | Sì |

A questi si aggiunge una quarta skill, `/inglese:confronto`, che non fa parte della sequenza: confronta le due versioni (italiana e inglese) dello stesso documento e segnala le divergenze, senza riscrivere (vedi più sotto).

La sequenza è scrittore, poi verificatore se serve, poi stilista. Chi si occupa dei fatti non si occupa dello stile, e chi si occupa dello stile non può toccare i fatti né togliere informazione. *Asciutto* (*lean*) vuol dire senza fronzoli, mai riassunto. Le cautele (*according to*, *is thought to*, *could*) non si rafforzano né si indeboliscono.

Si entra dove serve: con del materiale si parte dallo scrittore; con un testo già scritto e corretto si può andare direttamente allo stilista.

## Confronto fra due versioni

```
/inglese:confronto cartella-con-i-due-file originale: it
```

La cartella contiene la versione italiana e quella inglese dello stesso documento, una traduzione dell'altra, con la stessa struttura. La skill controlla prima l'allineamento (stessa sequenza di titoli e stessi elementi non prosa; se non coincidono si ferma), poi mette a fronte le due versioni (`controlla.py confronta`, più la lettura frase per frase) e scrive un solo rapporto in italiano con le divergenze numerate, i termini resi in modo diverso e i calchi. Non riscrive niente: per correggere si usano scrittore e stilista della lingua interessata, poi si ripete il confronto. Riprende la funzione di `rivedi-bilingue` del plugin `revisione`, senza la revisione di stile a pezzi, che ora spetta agli stilisti.

## Differenze dal plugin italiano

- **Passivi.** In italiano il *si* passivante e l'impersonale sono naturali e restano. In inglese si preferisce la voce attiva, ma non si inventa mai l'agente e si conservano i passivi che portano una cautela di attribuzione.
- **Ortografia e tipografia americane** (Chicago Manual of Style): `riferimenti/convenzioni-us.md`. L'em dash è ammesso senza spazi e con parsimonia, ma un progetto che vieta i trattini lunghi prevale.
- **Calchi dall'italiano** (falsi amici, reggenze, articoli, plurali): `riferimenti/diagnosi.md`, sezione 5.
- **Ritmo: soglie provvisorie.** Nessun testo inglese di autore reale è stato ancora misurato. Le soglie di `controlla.py --lingua en` sono quelle italiane scalate di circa 0,85, e ogni rapporto le dichiara provvisorie. Vedi `diagnosi.md`, sezione 3.

## Uso in Claude Code

Il plugin sta nel marketplace locale `scrittura-local` (cartella `scrittura-plugins`). Installazione, una volta:

```
claude plugin marketplace add /percorso/di/scrittura-plugins
claude plugin install inglese@scrittura-local
```

Poi:

```
/inglese:scrittore appunti.md
/inglese:verificatore input/mytext/mytext-1-stesura.md
/inglese:stilista testo.md riscrittura cerniere
```

Per i testi lunghi lo stilista lavora a pezzi con l'agente `inglese:stilista`, con approvazione a ogni passo; per le ricerche ampie il verificatore usa l'agente `inglese:verificatore`.

## Contenuto

- `skills/`: le tre skill del metodo e `confronto`.
- `agents/`: `verificatore` (ricerca in rete, contesto isolato) e `stilista` (lavoro a pezzi sui documenti lunghi).
- `riferimenti/contratto.md`: file di scambio, registro delle affermazioni, regole sui fatti, note e fonti, traduzione dall'italiano.
- `riferimenti/convenzioni-us.md`: ortografia, punteggiatura, numeri, date e titoli in americano.
- `riferimenti/diagnosi.md`: modello di buona prosa, ritmo (provvisorio), tic degli LLM e degli autori umani (con le famiglie del repertorio dei segni di scrittura automatica), calchi dall'italiano, passivi, intoppi di lettura e, alla sezione 11, ciò che non è un segno.
- `riferimenti/NOTE-LEGALI.md`: origine dei materiali e licenze.
- `riferimenti/manutenzione.md`: data dei lessici di tic, quando rivederli e come aggiungerne o toglierne uno.
- `strumenti/controlla.py`: controlli di integrità (con ricerca di omissioni), struttura, ritmo, tic e scorrevolezza. Solo libreria standard di Python. Si usa sempre con `--lingua en`. È la stessa identica copia del plugin `italiano` (un'unica fonte con due profili di lingua).
- `strumenti/verifica_integrita.py`: controllo riga per riga dei pezzi (dal plugin `revisione`).
- `strumenti/verifica_allineamento.py`: controllo che due file (italiano e inglese) abbiano la stessa struttura (dal plugin `revisione`).

## Rapporto con `revisione`

Questo plugin e `italiano` raccolgono e sostituiscono `revisione` (skill `rivedi`, `rivedi-bilingue`, agente `doc-reviewer`): la revisione dello stile di testi inglesi, il controllo degli italianismi e il flusso a pezzi con approvazione sono nello stilista; il confronto di due versioni è in `/inglese:confronto`.

---

## Limiti d'uso

Il plugin migliora uno stile e controlla i fatti: non è un rilevatore di testi generati da IA e non dimostra chi ha scritto un testo. Gli indizi di `controlla.py` sono segnali di stile con soglie in parte provvisorie. Molti (frasi ovvie, triadi, connettivi, pile di nomi, calchi dalla prima lingua) compaiono anche nella prosa di autori umani, in particolare di chi scrive in una seconda lingua o in registri burocratici e accademici. Non vanno usati per attribuire un testo a una macchina né per giudicare una persona: servono a chi scrive per rivedere il proprio testo. Il plugin non cerca di eludere i rilevatori.

## Note

- Versione 0.1.0, bozza. Costruita copiando il metodo del plugin `italiano` e adattando diagnosi, convenzioni e strumenti all'inglese. Provata solo su testi di prova scritti da Claude (vedi `prove/` nel marketplace), non su testi di autori reali.
- Da fare: ricalibrare il ritmo su 3-5 brani di autori reali anteriori al 2023 e 2-3 testi noiosi o artefatti; provare con altri LLM.
- Licenza MIT, autore cms.
