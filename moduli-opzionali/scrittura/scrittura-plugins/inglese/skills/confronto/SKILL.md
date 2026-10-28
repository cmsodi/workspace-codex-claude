---
name: confronto
description: Confronta le due versioni, italiana e inglese americana, di uno stesso documento (una traduzione dell'altra, con la stessa struttura) e segnala le divergenze: numeri, nomi, omissioni, aggiunte, cautele e modalità cambiate, termini resi in modo diverso, calchi in un senso o nell'altro. Non riscrive niente: produce un rapporto in italiano. Per correggere si usano scrittore e stilista della lingua interessata (plugin italiano o inglese), poi si ripete il confronto. Usala quando l'utente indica una cartella con i due file nelle due lingue.
argument-hint: "[cartella con i due file] [originale: it | en]"
---

Confronti le due versioni di un documento, italiana e inglese, e riferisci dove dicono cose diverse. Non correggi e non riscrivi: lo stile di ciascuna versione è compito dello stilista della sua lingua (`/italiano:stilista`, `/inglese:stilista`), i fatti sono compito di scrittore e verificatore. Tu stabilisci se le due versioni **dicono la stessa cosa**.

Argomenti: $ARGUMENTS

## File condivisi e convenzioni

Gli strumenti stanno due livelli sopra questa skill: `${CLAUDE_SKILL_DIR}/../../strumenti/` (`controlla.py`, `verifica_allineamento.py`). Se la variabile non risulta sostituita, cercali con Glob (`~/.claude/plugins/**/inglese/strumenti/controlla.py`) o relativamente a questo file (`../../strumenti/`). Leggi `${CLAUDE_SKILL_DIR}/../../riferimenti/contratto.md` (cautele, date, traduzione dall'italiano) e, per i calchi sul lato inglese, la sezione 5 di `diagnosi.md` nella stessa cartella. Le convenzioni del progetto (cartelle di output, sezione Note) prevalgono sui default.

## 1. Ingresso

- L'utente indica una **cartella** che contiene i due file. Se indica un file, usa la cartella che lo contiene e dillo.
- Elenca i `.md` della cartella (senza scendere nelle sottocartelle). Due file: procedi. Più di due: mostra l'elenco e chiedi quali confrontare. Meno di due: fermati e dillo.
- Rileva la lingua di ciascuno dalle prime righe del corpo (non dal nome del file). Devono essere uno in italiano e uno in inglese americano. Altre combinazioni non sono previste: fermati e dillo.
- **Originale:** se negli argomenti c'è `originale: it` o `originale: en`, ricordalo. Se manca, non chiedere: le due versioni si trattano alla pari e le divergenze si descrivono senza dire chi ha torto.
- I file sono in Markdown. Se uno è PDF o Word, fermati: la conversione va fatta prima con la skill adatta.

## 2. Allineamento (se fallisce, ti fermi)

```
python3 -I ${CLAUDE_SKILL_DIR}/../../strumenti/verifica_allineamento.py FILE_A FILE_B
```

- **Codice 1 (non allineati):** mostra il rapporto dello script, di' che non procedi perché le strutture non coincidono (titoli, tabelle, link, note, esponenti, commenti diversi), e **fermati**. Non creare niente.
- **Codice 0:** procedi. Gli avvisi non bloccanti (elenchi puntati o URL diversi) si riportano in una riga.

## 3. Controllo meccanico

```
python3 -I ${CLAUDE_SKILL_DIR}/../../strumenti/controlla.py confronta FILE_ITALIANO FILE_INGLESE
```

Il comando mette a fronte, sezione per sezione, numeri, nomi, lunghezza e cautele con l'equivalente nell'altra lingua (*secondo / according to*, *potrebbe / could*, *circa / about*…). Sono **indizi**: i numeri scritti in lettere, i nomi a inizio frase e i cambi di senso non li vede, e un nome che cambia forma nella traduzione (*Regno Unito / United Kingdom*) compare fra le differenze senza essere un errore. Se non puoi eseguire il programma, fai a mano gli stessi confronti.

## 4. Lettura a fronte

Leggi le due versioni sezione per sezione, frase per frase. Fino a circa 4.000 parole per file lavori su tutto il documento; oltre, procedi per gruppi di sezioni e tieni un file `lavoro/stato.md` (sezioni fatte, divergenze trovate) per poter riprendere. Per ogni coppia di frasi controlla:

- **Fatti:** numeri, date, nomi, unità, sigle, URL e riferimenti coincidono. I formati si convertono (*1.000* e *1,000*, *3,5* e *3.5*, «30 giugno 1908» e *June 30, 1908*): la conversione non è una divergenza.
- **Cautele e modalità:** *secondo* e *according to*, il condizionale e *could / might / may*, *si crede* e *is thought to*, *circa* e *about*, *probabilmente* e *probably*. Una cautela che sparisce, o che compare dove non c'era, è una divergenza **importante**.
- **Omissioni, aggiunte, spostamenti di senso:** una frase presente in una sola versione, una negazione, un quantificatore (*most* contro «quasi tutto»), un tempo verbale che cambia il senso.
- **Termini tecnici e nomi:** sempre resi allo stesso modo (costruisci un glossario mentre leggi); istituzioni nella forma inglese ufficiale; sigle sciolte allo stesso modo.
- **Calchi:** nella versione che deriva dall'altra (se `originale` è noto), altrimenti in entrambe. Sul lato inglese: falsi amici, reggenze, articoli (`diagnosi.md`, sezione 5). Sul lato italiano: passivi evitati per calco, gerundi appesi, aggettivo anteposto, nomi accatastati senza preposizioni, possessivi superflui (se è installato il plugin `italiano`, la sezione 5 del suo `diagnosi.md`).

**Che cosa conta come divergenza.** Uno scarto di contenuto tra le due frasi: fatti, numeri, nomi, modalità, quantificatori, tempi che cambiano il senso, termini resi in modo scorretto, aggiunte o omissioni. Sono **importanti** quelle che cambiano ciò che il testo afferma o gli errori di resa evidenti (*astronauts* reso «cosmonauti»); **minori** le sfumature di resa.

**Che cosa non è una divergenza.** I ritocchi di stile legittimi in una sola lingua, purché il contenuto resti lo stesso: un *si* passivante italiano reso con un attivo inglese il cui agente è nel testo, una nominalizzazione trasformata in verbo, una frase spezzata, una scelta di registro ricorrente. Vanno solo notati se toccano una cautela.

**Tagli e ristrutturazioni vanno in coppia.** Una frase tolta come ovvia o come fronzolo in una versione e non nell'altra crea una divergenza: segnalala, non decidere tu.

**Una divergenza non si risolve da sola.** Non correggere né l'una né l'altra versione. Riporta le due frasi affiancate e, se `originale` è noto, ciò che dice l'originale.

## 5. Che cosa produci

Nella cartella dei due file (o dove dice il progetto) crea una sottocartella `confronto-AAAA-MM-GG` (data da `date +%F`; se esiste, aggiungi `-2`, `-3`: non sovrascrivere), con **un solo file**, `problemi-AAAA-MM-GG.md`, in italiano:

1. **Intestazione:** i due file, la data, `originale` se noto, i controlli eseguiti, e che cosa non è stato verificato (i fatti non si verificano in rete: per quello c'è il verificatore).
2. **Divergenze tra le versioni:** tabella numerata `D01…` con la riga in ciascun file, la frase italiana, la frase inglese, la gravità (importante o minore) e una nota. Il totale e la ripartizione in coda.
3. **Controllo meccanico:** il riepilogo di `controlla.py confronta`, con gli avvisi che hai verificato e riconosciuto come falsi allarmi.
4. **Terminologia:** termini resi in più modi, con la forma da tenere ferma.
5. **Calchi trovati,** per lingua, con la riga.
6. **Problemi aperti per l'autore:** ciò che richiede una decisione (quale versione ha ragione, che cosa tagliare in coppia).

I due originali non si modificano mai e non produci versioni corrette. Se l'utente vuole correggere, chiedi quale versione, e rimanda a `/inglese:scrittore` o `/inglese:stilista` (per l'inglese) e `/italiano:scrittore` o `/italiano:stilista` (per l'italiano); poi si ripete il confronto.

## Regole di scrittura

- Ciò che scrivi è italiano naturale. Le frasi citate restano nella loro lingua.
- Non inventare citazioni, numeri o riferimenti. Un dato non verificabile si segnala, non si riempie.
- Distingui ciò che dicono le due versioni da ciò che inferisci tu.
- Chiedi conferma solo per azioni distruttive; sui punti dubbi scegli e annota.

## Prima di consegnare

- Ogni divergenza ha la riga in entrambi i file e la gravità.
- Gli avvisi del programma sono stati letti uno per uno: o confluiti in una divergenza, o scartati con il motivo.
- Il rapporto dice se `originale` era noto e che i fatti non sono stati verificati in rete.
- Nessun file originale è stato toccato.
