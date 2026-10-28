# Istruzioni per Codex

## Parte specifica di Codex

- Le skill complete e canoniche sono in `.claude/skills/`, anche quando le
  crea o le modifica Codex.
- `.agents/skills/genera-entrypoint-codex/` è l'unica skill canonica
  specifica di Codex. Gli altri entrypoint sotto `.agents/skills/` sono
  generati localmente e non devono essere modificati a mano.
- Dopo l'aggiunta, la rinomina, la rimozione o la modifica di `name` o
  `description` di una skill in `.claude/skills/`, usa
  `$genera-entrypoint-codex` e segnala che occorre aprire una nuova sessione
  Codex.
- Alla prima sessione Codex in un clone nuovo, genera gli entrypoint prima del
  lavoro ordinario se sotto `.agents/skills/` è presente soltanto
  `genera-entrypoint-codex`.
- Per il lavoro ordinario usa la skill più specifica disponibile e risolvi i
  percorsi operativi rispetto alla skill canonica sotto `.claude/skills/`.

## Parte comune

Prima di operare, leggi per intero `PROJECT_GUIDE.md` nella radice del
progetto e applicane le istruzioni.
