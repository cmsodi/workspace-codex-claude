# Modulo opzionale di scrittura

Il modulo aggiunge ruoli condivisi per:

- scrittura, verifica delle fonti e revisione stilistica in italiano;
- scrittura, verifica delle fonti e revisione stilistica in inglese americano;
- confronto semantico fra versioni italiana e inglese.

Contiene i plugin canonici, i relativi strumenti e gli entrypoint locali per
Codex. Licenze e note legali restano nelle rispettive cartelle.

Il modulo è inattivo nella posizione corrente. Per attivarlo, dalla radice del
progetto su macOS, Linux o Git Bash:

```sh
cp -R moduli-opzionali/scrittura/scrittura-plugins .claude/
cp -R moduli-opzionali/scrittura/skills/. .claude/skills/
python3 -I .claude/scrittura-plugins/prove/test_controlla.py
python3 .agents/skills/genera-entrypoint-codex/scripts/genera_entrypoint.py
```

In PowerShell:

```powershell
Copy-Item -Recurse moduli-opzionali/scrittura/scrittura-plugins .claude/
Copy-Item -Recurse moduli-opzionali/scrittura/skills/* .claude/skills/
py -3 .claude/scrittura-plugins/prove/test_controlla.py
py -3 .agents/skills/genera-entrypoint-codex/scripts/genera_entrypoint.py
```

Prima della copia controlla eventuali skill con lo stesso nome. Dopo
l'attivazione, le convenzioni del progetto registrate in `PROJECT_GUIDE.md`
prevalgono sui valori predefiniti del modulo. Se usi Codex, apri una nuova
sessione dopo la generazione degli entrypoint.
