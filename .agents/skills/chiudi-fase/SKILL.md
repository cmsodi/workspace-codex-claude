---
name: chiudi-fase
description: Verifica e pubblica un punto di ripristino quando l'utente chiede commit, push, pubblicazione, fine fase o passaggio alla fase successiva, senza avanzare artificialmente lo stato.
---

# Chiudi o pubblica il lavoro

## 1. Determina lo stato

1. Leggi `PROJECT_GUIDE.md` e il file che vi è indicato come fonte dello
   stato, quando esiste.
2. Distingui fra checkpoint intermedio e chiusura effettiva di una fase.
3. Dichiara completata una fase soltanto se la sua condizione di completamento
   è verificata. Una richiesta di commit o push, da sola, non basta.

## 2. Conserva la memoria necessaria

Quando una fase si chiude, trasferisci nei file persistenti risultati,
decisioni, controlli, questioni aperte e rinvii. Aggiorna il file di stato e
designa una sola fase successiva soltanto se è realmente definita.

Prepara un prompt di ripresa soltanto quando esiste una fase successiva. Il
prompt deve rinviare ai file che custodiscono lo stato senza ricostruire
l'intera conversazione.

## 3. Crea il punto di ripristino

1. Controlla stato e diff e separa modifiche estranee.
2. Esegui i controlli proporzionati al lavoro e `git diff --check`.
3. Aggiungi soltanto i file pertinenti.
4. Crea un commit descrittivo quando la richiesta o la guida lo prevede.
5. Esegui il push quando autorizzato e tecnicamente possibile.
6. Verifica infine la pulizia del repository e l'allineamento del ramo remoto.

Non modificare i file di stato soltanto per inserirvi l'hash del commit appena
creato.

## 4. Consegna

Comunica:

- se una fase è stata chiusa o è rimasta invariata;
- l'eventuale fase successiva;
- i file che custodiscono lo stato;
- hash del commit ed esito del push;
- il prompt di ripresa, soltanto quando è stato effettivamente preparato.
