# Compatibilità tra Claude Code e Codex

La cartella `.claude/scrittura-plugins/` conserva la struttura canonica del marketplace Claude Code. Le skill condivise risiedono in `.claude/skills/`; la skill `genera-entrypoint-codex` crea sotto `.agents/skills/` i piccoli entrypoint locali necessari alla loro scoperta da parte di Codex.

Quando una skill canonica viene caricata attraverso un entrypoint condiviso, applica queste equivalenze:

- `$ARGUMENTS` indica la richiesta corrente dell'utente.
- `${CLAUDE_SKILL_DIR}` indica la cartella che contiene il `SKILL.md` canonico aperto sotto `.claude/scrittura-plugins/`.
- Le convenzioni comuni del progetto sono in `PROJECT_GUIDE.md`; le sole istruzioni specifiche dell'ambiente sono in `AGENTS.md` per Codex e in `CLAUDE.md` per Claude Code.
- `Read`, `Write`, `Glob`, `Grep` e `Bash` indicano gli strumenti locali equivalenti disponibili nell'ambiente. Per le ricerche testuali, quando disponibile, preferisci `rg`.
- `WebSearch` e `WebFetch` indicano gli strumenti web disponibili. Apri sempre la pagina sorgente: un risultato di ricerca non equivale a una fonte consultata.
- Un agente nominato nelle istruzioni canoniche può essere sostituito da un agente o subagente equivalente quando l'ambiente lo permette e il compito lo giustifica. In caso contrario, esegui lo stesso flusso nel contesto principale.
- Le invocazioni Claude `/italiano:ruolo` e `/inglese:ruolo` corrispondono agli entrypoint condivisi `italiano-ruolo` e `inglese-ruolo`.

I percorsi operativi degli entrypoint partono sempre dalla radice del progetto e usano la forma canonica `.claude/...`. Gli entrypoint generati sotto `.agents/skills/` non devono contenere copie del metodo né essere modificati a mano.
