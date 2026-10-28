# Istruzioni per Claude Code

## Parte specifica di Claude Code

- Le skill locali condivise sono visibili in `.claude/skills/`.
- La loro collocazione fisica canonica è `.claude/skills/`.
- Anche le nuove skill destinate a entrambi gli ambienti vanno create soltanto
  in `.claude/skills/`.
- Dopo l'aggiunta, la rinomina, la rimozione o la modifica di `name` o
  `description` di una skill, esegui
  `python3 .agents/skills/genera-entrypoint-codex/scripts/genera_entrypoint.py`.
- Gli entrypoint Codex generati sotto `.agents/skills/` non devono essere
  modificati a mano.
- Se viene attivato il modulo di scrittura, i plugin sono visibili in
  `.claude/scrittura-plugins/`.
- Nei file condivisi usa i percorsi canonici `.claude/...`.

## Parte comune

Prima di operare, leggi per intero `PROJECT_GUIDE.md` nella radice del
progetto e applicane le istruzioni.
