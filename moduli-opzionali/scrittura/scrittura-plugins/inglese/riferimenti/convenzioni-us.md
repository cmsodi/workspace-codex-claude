# Convenzioni dell'inglese americano

Riferimento per i tre ruoli. Guida di base: il *Chicago Manual of Style*, salvo diversa indicazione del progetto o del documento. Il testo deriva da una precedente guida di stile del plugin di revisione; le parti sul controllo dei tic sono ora in `diagnosi.md`. Esempi e forme corrette sono in inglese.

La regola generale: **coerenza dentro il documento**. Dove il documento usa in modo coerente una forma lecita (virgolette dritte o ricurve, Title Case o prima maiuscola nei titoli), la si rispetta.

## Ortografia

- **-ize / -ization**, non -ise: *organize*, *recognize*, *realization*. Eccezioni che restano -ise: *advise*, *revise*, *exercise*, *surprise*, *otherwise*, *premise*.
- **-or**, non -our: *color*, *favor*, *behavior*, *neighbor*.
- **-er**, non -re: *center*, *meter*, *liter*, *theater*.
- **Consonante non raddoppiata**: *modeled*, *labeled*, *traveled*, *canceled*.
- Altre forme americane: *program*, *analyze*, *judgment*, *defense*, *offense*, *license* (anche nome), *gray*, *check* (assegno), *skeptic*, *aluminum*.
- *Toward*, *while*, *among*, *learned*, *spelled* (non *towards*, *whilst*, *amongst*, *learnt*, *spelt*).
- Citazioni da fonti britanniche e nomi propri (*Labour Party*, *Ministry of Defence*, *Royal Air Force*) non si toccano.

## Punteggiatura

- **Virgola seriale** (Oxford comma): sempre, *A, B, and C*. Un'omissione si segnala una volta, con qualche esempio, non occorrenza per occorrenza.
- **Virgolette.** Doppie per le citazioni, semplici per le citazioni dentro citazioni, mai le caporali. **Il punto fermo e la virgola stanno dentro le virgolette di chiusura** (*"the plan."*); punto e virgola e due punti fuori; punto interrogativo ed esclamativo dentro solo se appartengono alla citazione. Dritte o ricurve: si segue il documento.
- **Trattini.**
  - Il **trattino** (-) serve nei composti (*well-known*, *long-term*).
  - L'**en dash** (U+2013) serve per gli intervalli (*1990–2000*, *pp. 12–18*).
  - L'**em dash** (U+2014) scritto **senza spazi** è corretto in americano, ma con parsimonia. È uno dei tic più noti dei testi da LLM: si controlla quando ce n'è più di uno per capoverso, più di tre o quattro per pagina, o quando sostituisce una virgola o un punto per puro effetto. La sostituzione migliore cambia la struttura della frase (virgola, due punti, punto, parentesi).
  - Sono sbagliati: il trattino semplice spaziato come pausa (` - `), il doppio trattino (`--`) e l'en dash spaziato come pausa (uso britannico). Un trattino semplice senza spazi dove serve una pausa (*the past-all countries decide*) è quasi sempre un em dash scritto male: è un errore del testo.
  - **Se il progetto vieta i trattini lunghi**, nel testo non c'è nessun em dash: vale il divieto del progetto, non la tolleranza del Chicago.
- **Contrazioni** (*don't*, *it's*): si lasciano come sono. Si segnala solo un'incoerenza di registro dentro lo stesso documento.
- **Due punti e punto e virgola**: il punto e virgola separa due frasi complete o le voci complesse di un elenco; i due punti introducono un elenco o una spiegazione. Un attacco a effetto con due punti (*Here's the key: …*) è un tic.

## Numeri, date, unità

- **Date**: formato americano, *October 22, 2026*; con giorno ordinale solo nel parlato. *22 October 2026* e *22nd of October* sono britannici.
- **Numeri nel testo**: il Chicago scrive in lettere gli interi da zero a cento e le cifre tonde (*twenty*, *three hundred*), in cifre gli altri e le misure tecniche. Il documento può avere una regola propria (per esempio cifre per tutto ciò che è misurato): si segue e si resta coerenti.
- **Migliaia e decimali**: virgola per le migliaia (*1,000,000*), punto per i decimali (*3.5*). Con il materiale italiano si converte (*1.000.000* diventa *1,000,000*, *3,5* diventa *3.5*).
- *U.S.* o *US*: una forma sola in tutto il documento. *e.g.,* e *i.e.,* con la virgola dopo.
- **Ora**: *7:17 a.m.* (con i punti, minuscolo).

## Titoli

*Title Case* o solo la prima maiuscola, secondo la convenzione del documento; si segnala solo l'incoerenza fra titoli dello stesso livello. I titoli senza articolo, in stile telegrafico, sono normali in inglese: non si segnalano. In un testo prodotto da zero, per l'inglese editoriale la scelta consigliata è *sentence case* per i sottotitoli e *Title Case* per il titolo del documento, salvo diversa indicazione.

## Controlli sul testo prodotto

`controlla.py --lingua en tic` segnala ortografia britannica, date non americane, punto o virgola fuori dalle virgolette, caporali, trattini spaziati, em dash (con densità) e virgola seriale mancante. Controlla anche la coerenza dentro il documento: titoli dello stesso livello con convenzioni diverse (Title Case e prima maiuscola), apostrofi e virgolette doppie dritti mescolati ai ricurvi, *U.S.* e *US* insieme, *e.g.* e *i.e.* senza la virgola dopo, contrazioni e forme estese mescolate. Non controlla ancora l'uniformità di cifre e lettere nei numeri. Sono indizi: i nomi propri britannici e le citazioni non si toccano.
