---
name: verifica-workspace
description: Verifica la configurazione del workspace condiviso fra Codex e Claude Code, inclusi file di avvio, cartelle di base, fonte canonica delle skill, allineamento degli entrypoint Codex e stato dell'eventuale modulo di scrittura. Usala quando l'utente chiede di controllare, validare o diagnosticare il workspace dopo una copia o un clone, oppure segnala che i due ambienti vedono configurazioni diverse. Non usarla automaticamente nelle attività ordinarie.
---

# Verifica il workspace condiviso

1. Dalla radice del progetto esegui:

   ```sh
   python3 .claude/skills/verifica-workspace/scripts/verifica_workspace.py
   ```

2. Comunica separatamente lo stato del nucleo, degli entrypoint Codex e
   dell'eventuale modulo di scrittura.
3. Se il controllo fallisce, esamina soltanto i percorsi segnalati e spiega la
   causa concreta. La verifica è in sola lettura: non generare o modificare
   entrypoint senza una richiesta di riparazione.
4. Se Python non è disponibile, esegui manualmente gli stessi controlli
   descritti dallo script senza chiedere all'utente di usare il terminale.
