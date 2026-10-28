# Entrypoint locali per Codex

Le skill complete e canoniche risiedono sempre in `.claude/skills/`.
`.agents/skills/` contiene stabilmente soltanto la skill
`genera-entrypoint-codex`; gli altri entrypoint sono generati localmente,
ignorati da Git e non devono essere modificati a mano.

Dopo l'aggiunta, la rinomina, la rimozione o la modifica dei metadati di una
skill canonica, esegui:

```sh
python3 .agents/skills/genera-entrypoint-codex/scripts/genera_entrypoint.py
```

Apri poi una nuova sessione Codex per aggiornare la scoperta delle skill.
