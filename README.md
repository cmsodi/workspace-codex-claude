# Workspace condiviso per Codex e Claude Code

Questo modello prepara una cartella di progetto utilizzabile sia da Codex sia
da Claude Code. Le istruzioni comuni vivono in `PROJECT_GUIDE.md`; i due file
di avvio contengono soltanto le indicazioni specifiche dell'ambiente.

La directory fisica e canonica di tutte le skill condivise è
`.claude/skills/`, indipendentemente dal sistema operativo e dall'ambiente
che le crea. Codex scopre le stesse skill attraverso piccoli entrypoint locali
generati sotto `.agents/skills/`. La struttura non usa collegamenti simbolici
e non richiede configurazioni speciali su Windows.

## Struttura

```text
.
├── AGENTS.md
├── CLAUDE.md
├── PROJECT_GUIDE.md
├── .claude/
│   └── skills/
│       ├── chiudi-fase/
│       └── verifica-workspace/
├── .agents/
│   └── skills/
│       └── genera-entrypoint-codex/
├── input/
├── lavorazione/
├── output/
├── legacy/
├── test/
└── moduli-opzionali/
    └── scrittura/
```

- `input/`: materiali ricevuti o messi a disposizione del progetto;
- `lavorazione/`: bozze, trasformazioni e risultati intermedi;
- `output/`: prodotti generati o destinati alla consegna;
- `legacy/`: materiali superati conservati per recupero e confronto;
- `test/`: prove, fixture e risultati temporanei di verifica.

Ognuna delle cinque cartelle contiene un breve `README.md` che ne definisce
funzione e confini. Il resto del contenuto operativo è inizialmente vuoto.

## Avvio di un nuovo progetto

1. Crea un repository dal modello e clonalo normalmente su macOS, Linux o
   Windows.
2. Rinomina la cartella con il nome del progetto.
3. Compila le sezioni tra parentesi quadre in `PROJECT_GUIDE.md`.
4. Aggiungi soltanto le skill locali realmente necessarie in
   `.claude/skills/`.
5. Se usi Codex, chiedi: «Genera gli entrypoint Codex», quindi apri una nuova
   sessione Codex.
6. Chiedi a Codex o Claude Code: «Verifica il workspace condiviso».
7. Inizializza il repository Git quando opportuno.

La richiesta di verifica attiva la skill `verifica-workspace`, che esegue
internamente i controlli senza richiedere all'utente di lanciare Python. La
skill non viene eseguita durante le normali attività del progetto.

## Regola unica per le skill

Ogni skill completa va creata, aggiornata, rinominata o rimossa esclusivamente
sotto `.claude/skills/`. Questa regola vale anche quando il lavoro viene
svolto da Codex: `.claude/` è una normale directory del repository e Codex
può modificarla come qualunque altra cartella autorizzata.

Dopo ogni aggiunta, rinomina o rimozione di una skill, e dopo ogni modifica ai
campi `name` o `description` del suo `SKILL.md`, occorre rigenerare gli
entrypoint Codex. In Codex si può invocare:

```text
$genera-entrypoint-codex
```

Da qualunque ambiente si può eseguire lo stesso aggiornamento con:

```sh
python3 .agents/skills/genera-entrypoint-codex/scripts/genera_entrypoint.py
```

Gli entrypoint generati sotto `.agents/skills/` contengono soltanto i
metadati necessari alla scoperta e il rinvio alla skill canonica. Sono ignorati
da Git e non devono essere modificati a mano. La sola skill permanente e
versionata in `.agents/skills/` è `genera-entrypoint-codex`.

Quando cambia l'insieme delle skill o uno dei relativi metadati, dopo la
generazione apri una nuova sessione Codex: la scoperta delle skill avviene
all'avvio della sessione.

## Modulo di scrittura opzionale

Il modulo in `moduli-opzionali/scrittura/` è inattivo finché non viene
copiato nella directory condivisa. Dalla radice del nuovo progetto, su
macOS, Linux o Git Bash:

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

Il modulo aggiunge scrittura, verifica delle fonti e revisione stilistica in
italiano e inglese americano, oltre al confronto bilingue. Le convenzioni
specifiche registrate in `PROJECT_GUIDE.md` prevalgono sui suoi valori
predefiniti. Se il progetto viene usato con Codex, dopo l'attivazione apri una
nuova sessione.
