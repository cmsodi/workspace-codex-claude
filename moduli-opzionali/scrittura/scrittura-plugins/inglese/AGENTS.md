# Istruzioni per qualunque LLM

Questa cartella contiene un metodo in tre ruoli per testi in inglese americano. Le istruzioni e i rapporti sono in italiano; i testi sono in inglese. Se sei un LLM diverso da Claude Code, o lavori senza il supporto dei plugin, usa i file come istruzioni:

1. Leggi `README.md` per capire i tre ruoli e la loro sequenza.
2. Per ogni ruolo apri `skills/<ruolo>/SKILL.md` e segui le istruzioni come se fossero le tue. Ruoli: `scrittore`, `verificatore` (facoltativo, richiede una ricerca in rete), `stilista`. Fuori dalla sequenza c'è `confronto` (due versioni, italiana e inglese, dello stesso documento).
3. Leggi `riferimenti/contratto.md` (file di scambio, regole sui fatti), `riferimenti/convenzioni-us.md` (ortografia e tipografia americane) e `riferimenti/diagnosi.md` (modello di buona prosa, tic, calchi dall'italiano, passivi).
4. Ignora le variabili `${CLAUDE_SKILL_DIR}` e `$ARGUMENTS`: i percorsi sono relativi al file della skill (`../../riferimenti/`, `../../strumenti/`) e la richiesta è quella dell'utente.
5. Se puoi eseguire programmi, usa `strumenti/controlla.py` **sempre con `--lingua en`** (`python3 -I controlla.py --lingua en integrita|struttura|ritmo|tic|scorrevolezza ...`); il comando `confronta` (due versioni) è l'unico che non vuole `--lingua`. Senza l'opzione il programma applica le regole dell'italiano. Se non puoi eseguirlo, fai a mano i controlli che le skill descrivono.
6. Se non hai una ricerca in rete, il ruolo `verificatore` non si esegue: dillo, e lascia le affermazioni «non verificate».

Quattro regole valgono sempre:

- Non inventare fatti, numeri, citazioni, aneddoti. Ciò che manca si segnala.
- Lo stilista non tocca i fatti e non toglie informazione. *Asciutto* (*lean*) vuol dire senza fronzoli, mai riassunto.
- Conserva le cautele (*according to*, *is thought to*, *could*, *about*) senza rafforzarle né indebolirle.
- In inglese preferisci la voce attiva, ma non inventare l'agente di un passivo e non attivare un passivo che porta una cautela di attribuzione.

Le soglie di ritmo per l'inglese sono provvisorie: leggile come ordini di grandezza e dillo nel rapporto.

Frase pronta da incollare in un altro LLM:

> Leggi `AGENTS.md` nella cartella del plugin `inglese`, poi applica il ruolo **stilista** al file `NOME.md` con livello `riscrittura` e registro `regolare`. Segui le istruzioni di `skills/stilista/SKILL.md` e produci testo (in inglese) e rapporto (in italiano) come indicato.
