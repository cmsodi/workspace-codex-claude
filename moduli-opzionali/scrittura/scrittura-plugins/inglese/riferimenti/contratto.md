# Contratto tra le fasi

Regole comuni ai tre ruoli (scrittore, verificatore, stilista). Le legge ogni modello insieme alla propria skill. È il gemello di `contratto.md` del plugin `italiano`: la struttura è la stessa, cambiano la lingua dei testi e le convenzioni tipografiche.

## Lingua

Le istruzioni, i rapporti, le note e le domande all'autore sono in italiano. I testi che si scrivono, si verificano e si rifiniscono sono in **inglese americano**. Le citazioni, le riscritture proposte e gli esempi dentro i rapporti restano in inglese. Le etichette di lavoro dentro il testo (`[MANCA: …]`, `[DA VERIFICARE]`) restano quelle italiane, perché le legge l'autore e non il pubblico, e vanno tolte prima della consegna.

## Convenzioni del progetto e tipografia

Se il progetto che ospita il testo ha un `CLAUDE.md` o un file simile con convenzioni (cartelle di input e output, sezione Note, lingua, tipografia), valgono quelle e prevalgono su questi default. Un testo che l'utente incolla nel prompt si salva prima verbatim dove il progetto lo prevede. L'originale non si modifica mai.

I default di ortografia e tipografia (Chicago Manual of Style: ortografia americana, virgola seriale, virgolette, trattini, date, titoli) stanno in `convenzioni-us.md`. Un'eccezione da ricordare: il Chicago ammette l'em dash senza spazi, ma molti progetti lo vietano (per esempio quelli che vietano i trattini lunghi in tutti i documenti). Se il progetto lo vieta, nel testo inglese non ce n'è nessuno.

## File di scambio

Per ogni testo c'è una cartella di lavoro. `NOME` è il nome breve del testo.

| File | Prodotto da | Contenuto |
|---|---|---|
| `NOME-origine.md` | l'utente | materiale o testo di partenza; non si modifica mai |
| `NOME-1-stesura.md` | fase 1 | la prima stesura, con sezione `## Note` (in italiano) |
| `NOME-1-affermazioni.md` | fase 1 | registro delle affermazioni verificabili |
| `NOME-1-note.md` | fase 1 | scelte, lacune e segnalazioni, quando il testo ha già una propria sezione Notes |
| `NOME-2-verificato.md` | fase 2 | il testo dopo la verifica |
| `NOME-2-fonti.md` | fase 2 | registro delle fonti e registro delle affermazioni aggiornato |
| `NOME-3-prosa.md` | fase 3 | il testo finale |
| `NOME-3-rapporto.md` | fase 3 | che cosa è cambiato e perché (in italiano) |

Se una fase viene saltata, la successiva legge l'ultimo file prodotto e il rapporto finale lo dichiara.

## Elementi che non sono prosa

Non si riscrivono e restano identici in ogni fase: la sezione di note del testo (testo e link), i richiami a esponente o `[^n]`, i link e gli URL, i commenti HTML, il frontespizio, i blocchi di codice, le tabelle, le formule, le etichette in grassetto a inizio paragrafo e il segno degli elenchi. I titoli si cambiano solo in fase 3 e il cambiamento si dichiara. Un richiamo a nota resta in fondo alla frase o alla voce a cui appartiene.

Se il testo ha già una sezione `Notes` o `Note` propria (note del libro, bibliografia), nessuna fase la tocca, e le note della fase 1 vanno in `NOME-1-note.md`. Le note per capitolo (`### Notes` dentro un capitolo) fanno parte del capitolo e si trattano come prosa o come note del testo secondo il caso: nel dubbio, non si toccano.

## Il registro delle affermazioni

Una tabella Markdown con una riga per affermazione verificabile (numeri, date, nomi, attribuzioni, eventi, rapporti di causa). Il testo dell'affermazione può restare in inglese.

| ID | Tipo | Affermazione | Stato | Fonte |
|---|---|---|---|---|
| 001 | fatto | The light was seen at 7:17 a.m. local time | non verificata | |

- **Tipi:** fatto, stima, ipotesi, testimonianza, inferenza.
- **Stati:** non verificata, confermata, smentita, datata, in conflitto, non verificabile.
- La **fonte** compare solo dopo la fase 2 oppure quando il materiale di partenza la indica.

## Chi può toccare i fatti

- **Fasi 1 e 2:** sì. Sono le sole che stabiliscono, correggono o aggiungono affermazioni.
- **Fase 3:** no. Può riordinare, tagliare (con elenco nel rapporto), unire, riformulare e titolare. Non può aggiungere un fatto, un numero, un nome, una citazione, un aneddoto o un dettaglio sensoriale che non sono nel testo di partenza. Se le serve un fatto che manca, lo scrive nel rapporto come domanda per l'autore.

## Le cautele fanno parte dell'affermazione

*According to*, *is believed to*, *reportedly*, i modali (*could*, *might*, *may*, *would*) e gli *about*, *roughly*, *approximately* si conservano con lo stesso peso. *Hypothesize* non diventa *say*, *could* non diventa *can*, *may have* non diventa *did*. Un'ipotesi non diventa un fatto, un fatto non diventa un'ipotesi. Chi ha detto una cosa si cita con il nome e il ruolo che il materiale gli dà.

In inglese una cautela si perde facilmente nel passaggio da passivo ad attivo: «It is thought that the blast happened in the air» non diventa «The blast happened in the air». Se si attiva la frase, il soggetto dell'attribuzione resta («Researchers think the blast happened in the air») e deve essere nel materiale: chi pensa, lo dice la fonte, non lo stilista. Se la fonte non lo dice, il passivo con la cautela resta.

## Date e tempo

Una data relativa («recently», «last year», «a decade ago») si trasforma in data assoluta, con l'anno. Se la fonte è del 2018 e non è stata aggiornata, il testo dice «as of 2018» oppure la nota dichiara lo stato delle conoscenze. Un'inferenza sulle date (per esempio «circa 2008» da «a decade ago» in un articolo del 2018) va in nota. Formato delle date nel testo: americano (October 22, 2026).

## Controllo di integrità

Dopo la fase 3 (e dopo la 1, se si tratta di una ripulitura) si confronta il testo con quello di partenza. **In inglese si passa sempre `--lingua en`:** senza, il programma applica le regole dell'italiano.

```
python3 -I strumenti/controlla.py --lingua en integrita NOME-2-verificato.md NOME-3-prosa.md
```

- **Errore** (codice 1): numeri o nomi presenti nel risultato e assenti dall'origine. La fase 3 non può introdurli. Si corregge e si ripete il controllo.
- **Avviso:** numeri o nomi assenti dal risultato (si controlla che il taglio sia nel rapporto) e cautele aumentate o diminuite (si controlla che sia una scelta).
- Per la fase 2, che può aggiungere fatti, si usa `--consenti-aggiunte`: gli errori diventano avvisi e le aggiunte vanno nel registro.
- Il controllo non vede i numeri scritti in lettere (*three*, *twenty*) né i nomi a inizio frase: resta una lettura attenta del confronto.
- Per gli elementi che non sono prosa si esegue anche `python3 -I strumenti/controlla.py --lingua en struttura ORIGINE RISULTATO`: confronta titoli, richiami, link, commenti HTML, etichette, elenchi e sezione Note, e dà codice 1 alla prima differenza non dichiarata nel rapporto.

Senza possibilità di eseguire il programma, si confrontano a mano numeri, nomi, date, attribuzioni e cautele, riga per riga.

## Note e fonti

Un documento che usa fonti ha in fondo una sezione `## Note` (in italiano), dopo una riga `---`: per ogni fonte l'URL, la data di consultazione, che cosa sostiene e se la pagina è stata aperta o vista solo nei risultati. Nel testo non ci sono link. Le scelte fatte nei punti dubbi vanno nelle note. Un dato non verificabile si segnala; non si riempie.

## Traduzione dall'italiano

Se il materiale è in italiano e si chiede un testo inglese, si scrive in inglese originale, non si traduce parola per parola. Valgono in più queste regole.

- Nomi propri, istituzioni e titoli: la forma inglese ufficiale quando esiste (per esempio *European Space Agency*, non *Agenzia Spaziale Europea*), altrimenti il nome originale con una breve spiegazione alla prima occorrenza. La scelta si annota.
- Citazioni dall'italiano: la traduzione è dello scrittore, e la nota lo dichiara («traduzione mia»). Non si presenta una traduzione come testo ufficiale.
- Unità e formati: i numeri seguono l'uso americano (virgola per le migliaia, punto per i decimali), le date il formato americano. Le unità del materiale restano quelle del materiale; una conversione è un'aggiunta e va nel registro.
- Falsi amici e calchi: si controllano con `diagnosi.md`, sezione 5.

## Tono

Il testo ha il tono del materiale. Nei punti dubbi sul significato si sceglie la lettura più probabile e si annota la scelta; si chiede conferma solo per azioni distruttive, come sovrascrivere un file.
