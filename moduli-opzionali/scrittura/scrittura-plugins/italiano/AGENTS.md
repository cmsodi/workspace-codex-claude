# Istruzioni per qualunque LLM

Questa cartella contiene un metodo in tre ruoli per testi italiani. Se sei un LLM diverso da Claude Code, o lavori senza il supporto dei plugin, usa i file come istruzioni:

1. Leggi `README.md` per capire i tre ruoli e la loro sequenza.
2. Per ogni ruolo apri `skills/<ruolo>/SKILL.md` e segui le istruzioni come se fossero le tue. Ruoli: `scrittore`, `verificatore` (facoltativo, richiede una ricerca in rete), `stilista`.
3. Leggi `riferimenti/contratto.md` (file di scambio, regole sui fatti), `riferimenti/diagnosi.md` (modello di buona prosa, tic, calchi) e, quando serve, `riferimenti/grammatica-italiana.md`.
4. Ignora le variabili `${CLAUDE_SKILL_DIR}` e `$ARGUMENTS`: i percorsi sono relativi al file della skill (`../../riferimenti/`, `../../strumenti/`) e la richiesta è quella dell'utente.
5. Se puoi eseguire programmi, usa `strumenti/controlla.py` (`python3 -I controlla.py integrita|struttura|ritmo|tic|scorrevolezza ...`). Se non puoi, fai a mano i controlli che le skill descrivono.
6. Se non hai una ricerca in rete, il ruolo `verificatore` non si esegue: dillo, e lascia le affermazioni «non verificate».

Tre regole valgono sempre:

- Non inventare fatti, numeri, citazioni, aneddoti. Ciò che manca si segnala.
- Lo stilista non tocca i fatti e non toglie informazione. *Asciutto* vuol dire senza fronzoli, mai riassunto.
- Conserva le cautele («secondo», «si crede», «ipotizzano») senza rafforzarle né indebolirle.

Frase pronta da incollare in un altro LLM:

> Leggi `AGENTS.md` nella cartella del plugin `italiano`, poi applica il ruolo **stilista** al file `NOME.md` con livello `riscrittura` e registro `regolare`. Segui le istruzioni di `skills/stilista/SKILL.md` e produci testo e rapporto come indicato.
