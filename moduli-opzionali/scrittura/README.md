# Modulo opzionale di scrittura

Il modulo aggiunge ruoli condivisi per:

- scrittura, verifica delle fonti e revisione stilistica in italiano;
- scrittura, verifica delle fonti e revisione stilistica in inglese americano;
- confronto semantico fra versioni italiana e inglese.

Contiene i plugin canonici, i relativi strumenti e gli entrypoint locali per
Codex. Licenze e note legali restano nelle rispettive cartelle.

Il modulo è inattivo nella posizione corrente. Per attivarlo, dalla radice del
progetto:

```sh
cp -R moduli-opzionali/scrittura/scrittura-plugins .agents/
cp -R moduli-opzionali/scrittura/skills/. .agents/skills/
python3 -I .agents/scrittura-plugins/prove/test_controlla.py
```

Prima della copia controlla eventuali skill con lo stesso nome. Dopo
l'attivazione, le convenzioni del progetto registrate in `PROJECT_GUIDE.md`
prevalgono sui valori predefiniti del modulo.
