# Guida comune del progetto

> Questo file appartiene a un modello. Prima del primo lavoro reale sostituisci
> le indicazioni fra parentesi quadre e rimuovi questa nota.

## Identità

- **Nome:** [NOME DEL PROGETTO]
- **Scopo:** [RISULTATO CHE IL PROGETTO DEVE PRODURRE]
- **Radice locale autorizzata:** [PERCORSO ASSOLUTO DELLA CARTELLA]
- **Stato corrente:** [STATO INIZIALE O COLLEGAMENTO AL FILE DI STATO]

Le istruzioni esplicite dell'utente prevalgono sulle regole del progetto. I
file persistenti e Git costituiscono la fonte dello stato corrente; la memoria
della conversazione non li sostituisce.

## Struttura

- `input/`: materiali ricevuti o messi a disposizione del progetto. Non
  modificarli salvo richiesta esplicita.
- `lavorazione/`: bozze, trasformazioni, piani e risultati intermedi.
- `output/`: prodotti generati o destinati alla consegna.
- `legacy/`: materiali superati conservati per memoria, recupero o confronto;
  non sono fonti operative correnti.
- `test/`: prove, fixture e risultati temporanei di verifica.
- `.agents/skills/`: skill locali condivise da Codex e Claude Code.
- `moduli-opzionali/`: componenti disponibili ma inattivi finché non vengono
  installati nella struttura operativa.

[AGGIUNGERE QUI LE CARTELLE SPECIFICHE DEL PROGETTO E LA LORO FUNZIONE]

## Perimetro del contesto

Apri inizialmente soltanto questa guida e i file strettamente necessari alla
richiesta. Non esplorare ricorsivamente `input/`, `output/`, `legacy/` o
`test/` senza una ragione concreta. Consulta:

- `input/` quando il compito richiede i materiali ricevuti;
- `lavorazione/` per riprendere un'attività o verificare un passaggio
  intermedio;
- `output/` per ispezionare, validare o consegnare un prodotto;
- `legacy/` soltanto per recuperare o confrontare materiale storico;
- `test/` soltanto per eseguire, correggere o riordinare prove pertinenti.

Quando una cartella o un documento è la fonte corrente di una lavorazione,
indicalo qui in modo esplicito:

[INDICARE GLI INPUT CORRENTI E L'ORDINE DI AUTORITÀ FRA I DOCUMENTI]

## Metodo di lavoro

1. Verifica lo stato del repository e preserva modifiche estranee.
2. Leggi gli input necessari senza ampliare automaticamente il contesto.
3. Conserva separati input, intermedi e risultati.
4. Registra nei file persistenti decisioni, controlli, questioni aperte e
   passaggi necessari alla ripresa.
5. Esegui controlli proporzionati al rischio prima della consegna.

[AGGIUNGERE QUI IL FLUSSO SPECIFICO DEL PROGETTO]

## Stato, fasi e ripresa

Se il progetto usa fasi, indica un solo file come indice dello stato e assegna
a ogni fase obiettivo, input, risultato atteso e condizione di completamento.
Una fase diventa completata soltanto quando la condizione è verificata.

- **File che governa lo stato:** [PERCORSO OPPURE «NON PREVISTO»]
- **Fase corrente:** [IDENTIFICATORE OPPURE «NESSUNA»]
- **Prossima fase:** [IDENTIFICATORE OPPURE «NON DEFINITA»]

Un checkpoint Git non chiude automaticamente una fase. Il prompt per una nuova
conversazione va preparato soltanto quando esiste una fase successiva definita.

## Commit, push e chiusura

Le richieste di commit, push, pubblicazione, chiusura o passaggio di fase
attivano la skill `.agents/skills/chiudi-fase/SKILL.md`.

Prima di un commit:

- controllare stato e diff;
- separare modifiche estranee;
- eseguire i controlli pertinenti e `git diff --check`;
- aggiungere soltanto i file appartenenti al lavoro richiesto.

Non avanzare artificialmente lo stato per giustificare un commit. Dopo il push,
verificare che ramo locale e remoto coincidano.

## Perimetro locale e sicurezza

Opera soltanto dentro la radice locale autorizzata indicata in questa guida.
Un percorso esterno esplicitamente indicato dall'utente è autorizzato soltanto
per l'operazione richiesta; non estendere l'accesso ai file vicini.

Evita operazioni distruttive non richieste. Per archiviare materiale preferisci
spostamenti recuperabili in `legacy/` e verifica sempre il bersaglio.

## Compatibilità fra ambienti

- `.agents/` è la directory fisica canonica.
- `.claude` deve restare un collegamento simbolico a `.agents`.
- Codex usa i percorsi `.agents/...`.
- Claude Code può vedere gli stessi file sotto `.claude/...`.
- Le regole condivise appartengono a questo file; `AGENTS.md` e `CLAUDE.md`
  devono restare brevi e specifici dell'ambiente.

## Regole specifiche

[INSERIRE QUI CONVENZIONI, VINCOLI, STRUMENTI E CONTROLLI DEL PROGETTO]
