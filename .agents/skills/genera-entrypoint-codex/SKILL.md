---
name: genera-entrypoint-codex
description: Genera o aggiorna gli entrypoint locali che permettono a Codex di scoprire le skill canoniche conservate in .claude/skills. Usala durante la prima configurazione Codex e dopo l'aggiunta, la rinomina, la rimozione o la modifica dei metadati di una skill canonica. Non usarla per modificare il contenuto delle skill.
---

# Genera Entrypoint Codex

1. Dalla radice del progetto esegui:

   ```sh
   python3 .agents/skills/genera-entrypoint-codex/scripts/genera_entrypoint.py
   ```

2. Comunica quanti entrypoint sono stati creati, aggiornati o rimossi e segnala
   eventuali conflitti. Non modificare a mano gli entrypoint generati.
3. Ricorda all'utente di aprire una nuova sessione Codex quando l'insieme o i
   metadati delle skill sono cambiati, perché la scoperta avviene all'avvio
   della sessione.

Le skill complete appartengono sempre a `.claude/skills/`, anche quando sono
create o aggiornate da Codex. Questa skill è l'unica skill canonica conservata
in `.agents/skills/`; gli altri `SKILL.md` presenti lì sono entrypoint locali
generati e ignorati da Git.

Per un controllo in sola lettura usa:

```sh
python3 .agents/skills/genera-entrypoint-codex/scripts/genera_entrypoint.py --check
```
