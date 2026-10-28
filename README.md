# Workspace condiviso per Codex e Claude Code

Questo modello prepara una cartella di progetto utilizzabile sia da Codex sia
da Claude Code. Le istruzioni comuni vivono in `PROJECT_GUIDE.md`; i due file
di avvio contengono soltanto le indicazioni specifiche dell'ambiente.

La directory fisica delle skill è `.agents/`. Il percorso `.claude` è un
collegamento simbolico a `.agents`, così i due ambienti vedono gli stessi
strumenti senza mantenere copie divergenti.

## Struttura

```text
.
├── AGENTS.md
├── CLAUDE.md
├── PROJECT_GUIDE.md
├── .agents/
│   └── skills/
│       └── chiudi-fase/
├── .claude -> .agents
├── input/
├── lavorazione/
├── output/
├── legacy/
├── test/
├── strumenti/
└── moduli-opzionali/
    └── scrittura/
```

- `input/`: materiali ricevuti o messi a disposizione del progetto;
- `lavorazione/`: bozze, trasformazioni e risultati intermedi;
- `output/`: prodotti generati o destinati alla consegna;
- `legacy/`: materiali superati conservati per recupero e confronto;
- `test/`: prove, fixture e risultati temporanei di verifica.

Le cinque cartelle sono mantenute in Git mediante un file nascosto
`.gitkeep`. Il loro contenuto operativo è inizialmente vuoto.

## Avvio di un nuovo progetto

1. Copia l'intera cartella preservando il collegamento simbolico.
2. Rinomina la cartella con il nome del progetto.
3. Compila le sezioni tra parentesi quadre in `PROJECT_GUIDE.md`.
4. Aggiungi soltanto le skill locali realmente necessarie in
   `.agents/skills/`.
5. Esegui `python3 strumenti/verifica_struttura.py`.
6. Inizializza il repository Git quando opportuno.

## Modulo di scrittura opzionale

Il modulo in `moduli-opzionali/scrittura/` è inattivo finché non viene
copiato nella directory condivisa. Dalla radice del nuovo progetto:

```sh
cp -R moduli-opzionali/scrittura/scrittura-plugins .agents/
cp -R moduli-opzionali/scrittura/skills/. .agents/skills/
python3 -I .agents/scrittura-plugins/prove/test_controlla.py
```

Il modulo aggiunge scrittura, verifica delle fonti e revisione stilistica in
italiano e inglese americano, oltre al confronto bilingue. Le convenzioni
specifiche registrate in `PROJECT_GUIDE.md` prevalgono sui suoi valori
predefiniti.
