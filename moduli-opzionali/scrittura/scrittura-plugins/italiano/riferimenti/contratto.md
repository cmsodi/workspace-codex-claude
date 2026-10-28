# Contratto tra le fasi

Regole comuni ai tre ruoli (scrittore, verificatore, stilista). Le legge ogni modello insieme alla propria skill.

## Convenzioni del progetto e tipografia

Se il progetto che ospita il testo ha un `CLAUDE.md` o un file simile con convenzioni (cartelle di input e output, sezione Note, lingua, tipografia), valgono quelle e prevalgono su questi default. Un testo che l'utente incolla nel prompt si salva prima verbatim dove il progetto lo prevede. L'originale non si modifica mai.

Default tipografici in italiano: caporali « » per citazioni e dialoghi; niente trattini lunghi (né lineetta lunga né media, né il trattino spaziato usato come pausa: si usano virgola, punto, due punti o parentesi; restano i trattini nelle parole composte e negli intervalli di numeri); titoli con la sola prima maiuscola; tre puntini; niente virgola prima della «e» finale di un elenco.

## File di scambio

Per ogni testo c'è una cartella di lavoro. `NOME` è il nome breve del testo.

| File | Prodotto da | Contenuto |
|---|---|---|
| `NOME-origine.md` | l'utente | materiale o testo di partenza; non si modifica mai |
| `NOME-1-stesura.md` | fase 1 | la prima stesura, con sezione `## Note` |
| `NOME-1-affermazioni.md` | fase 1 | registro delle affermazioni verificabili |
| `NOME-1-note.md` | fase 1 | scelte, lacune e segnalazioni, quando il testo ha già una propria sezione Note |
| `NOME-2-verificato.md` | fase 2 | il testo dopo la verifica |
| `NOME-2-fonti.md` | fase 2 | registro delle fonti e registro delle affermazioni aggiornato |
| `NOME-3-prosa.md` | fase 3 | il testo finale |
| `NOME-3-rapporto.md` | fase 3 | che cosa è cambiato e perché |

Se una fase viene saltata, la successiva legge l'ultimo file prodotto e il rapporto finale lo dichiara.

## Elementi che non sono prosa

Non si riscrivono e restano identici in ogni fase: la sezione di note del testo (testo e link), i richiami a esponente o `[^n]`, i link e gli URL, i commenti HTML, il frontespizio, i blocchi di codice, le tabelle, le formule, le etichette in grassetto a inizio paragrafo e il segno degli elenchi. I titoli si cambiano solo in fase 3 e il cambiamento si dichiara. Un richiamo a nota resta in fondo alla frase o alla voce a cui appartiene.

Se il testo ha già una sezione `Note` propria (note del libro, bibliografia), nessuna fase la tocca, e le note della fase 1 vanno in `NOME-1-note.md`.

## Il registro delle affermazioni

Una tabella Markdown con una riga per affermazione verificabile (numeri, date, nomi, attribuzioni, eventi, rapporti di causa).

| ID | Tipo | Affermazione | Stato | Fonte |
|---|---|---|---|---|
| 001 | fatto | Il bagliore fu visto alle 7:17 locali | non verificata | |

- **Tipi:** fatto, stima, ipotesi, testimonianza, inferenza.
- **Stati:** non verificata, confermata, smentita, datata, in conflitto, non verificabile.
- La **fonte** compare solo dopo la fase 2 oppure quando il materiale di partenza la indica.

## Chi può toccare i fatti

- **Fasi 1 e 2:** sì. Sono le sole che stabiliscono, correggono o aggiungono affermazioni.
- **Fase 3:** no. Può riordinare, tagliare (con elenco nel rapporto), unire, riformulare e titolare. Non può aggiungere un fatto, un numero, un nome, una citazione, un aneddoto o un dettaglio sensoriale che non sono nel testo di partenza. Se le serve un fatto che manca, lo scrive nel rapporto come domanda per l'autore.

## Le cautele fanno parte dell'affermazione

«Secondo alcune stime», «si crede», «ipotizzano», il condizionale e i «circa» si conservano con lo stesso peso. «Ipotizzano» non diventa «dicono», «potrebbe» non diventa «può». Un'ipotesi non diventa un fatto, un fatto non diventa un'ipotesi. Chi ha detto una cosa si cita con il nome e il ruolo che il materiale gli dà.

## La fonte sostiene l'affermazione, non la sostituisce

Nel corpo del testo, formula direttamente un fatto verificato e lascia che il richiamo alla nota ne renda ricostruibile la fonte. Evita ponti difensivi come «la documentazione descrive», «il rapporto attesta», «la pagina indica» o «le fonti mostrano» quando servono soltanto a introdurre un'affermazione che il testo può assumersi.

Mantieni invece l'attribuzione quando ciò che conta è proprio chi parla o il valore probatorio della fonte: dichiarazioni e posizioni di un attore, stime, previsioni, giudizi, contenuti promozionali, testimonianze, conflitti fra fonti, divergenze fra versioni o limiti di ciò che si può provare. In questi casi nomina l'attore o il documento con precisione e non trasformare una sua affermazione in un fatto indipendente.

La regola riguarda la prosa destinata al lettore. Nei registri, nelle note e nei rapporti di verifica è invece corretto scrivere esplicitamente che cosa sostiene, non sostiene o permette di concludere ciascuna fonte.

## Date e tempo

Una data relativa («di recente», «l'anno scorso», «una decina di anni fa») si trasforma in data assoluta, con l'anno. Se la fonte è del 2018 e non è stata aggiornata, il testo dice «al 2018» oppure la nota dichiara lo stato delle conoscenze. Un'inferenza sulle date (per esempio «circa 2008» da «una decina di anni fa» in un articolo del 2018) va in nota.

## Controllo di integrità

Dopo la fase 3 (e dopo la 1, se si tratta di una ripulitura) si confronta il testo con quello di partenza:

```
python3 -I strumenti/controlla.py integrita NOME-2-verificato.md NOME-3-prosa.md
```

- **Errore** (codice 1): numeri o nomi presenti nel risultato e assenti dall'origine. La fase 3 non può introdurli. Si corregge e si ripete il controllo.
- **Avviso:** numeri o nomi assenti dal risultato (si controlla che il taglio sia nel rapporto) e cautele aumentate o diminuite (si controlla che sia una scelta).
- Per la fase 2, che può aggiungere fatti, si usa `--consenti-aggiunte`: gli errori diventano avvisi e le aggiunte vanno nel registro.
- Il controllo non vede i numeri scritti in lettere né i nomi a inizio frase: resta una lettura attenta del confronto.
- Per gli elementi che non sono prosa si esegue anche `python3 -I strumenti/controlla.py struttura ORIGINE RISULTATO`: confronta titoli, richiami, link, commenti HTML, etichette, elenchi e sezione Note, e dà codice 1 alla prima differenza non dichiarata nel rapporto.

Senza possibilità di eseguire il programma, si confrontano a mano numeri, nomi, date, attribuzioni e cautele, riga per riga.

## Note e fonti

Un documento che usa fonti ha in fondo una sezione `## Note`, dopo una riga `---`: per ogni fonte l'URL, la data di consultazione, che cosa sostiene e se la pagina è stata aperta o vista solo nei risultati. Nel testo non ci sono link. Le scelte fatte nei punti dubbi vanno nelle note. Un dato non verificabile si segnala; non si riempie.

## Lingua e tono

Il testo ha la lingua del materiale. I rapporti e le note sono in italiano. Nei punti dubbi sul significato si sceglie la lettura più probabile e si annota la scelta; si chiede conferma solo per azioni distruttive, come sovrascrivere un file.
