# Diagnosi: il modello di buona prosa e i suoi nemici

Riferimento per la fase 3. Le sezioni 1-4 servono prima e durante la scrittura. La 5, la 6 e la 7 si consultano dopo la prima stesura, come controllo. La sezione 11 dice che cosa *non* è un segno, per non correggere troppo.

## 1. Modello positivo

Ricavato dall'analisi di un articolo di divulgazione scientifica scritto da un giornalista prima del 2023 (*Il Post*, 30 giugno 2018, su Tunguska) e da un testo professionale dell'utente. Sono tratti da imitare per principio, non per forma.

1. **Apri con un'immagine concreta e verificabile.** Un luogo, un'ora, un gesto, un numero. L'interesse nasce dal fatto, mai da una premessa sul perché il tema conta.
2. **Una persona dentro i fatti,** quando il materiale ne offre una. Il racconto passa da lei e si chiude, se serve, tornando a lei.
3. **Dì con precisione ciò che non si sa.** Attribuisci con nome e ruolo: chi, di quale università, quando. Distingui ciò che è accertato da ciò che si crede.
4. **Numeri con un termine di paragone** («200 volte la bomba di Hiroshima»), sempre attribuiti.
5. **Pochi aggettivi di valore.** Verbi e gesti concreti.
6. **Titoletti brevi e vari,** non tutti nella stessa forma.
7. **Ritmo che viene dal contenuto.** Si alternano scena, dato, ipotesi, cifra. La frase di base è ampia e piana. Le frasi brevi compaiono dove il discorso svolta.
8. **Contrasti solo se reali.** «Non una pietra ma una cometa» va bene se qualcuno ha sostenuto la pietra.
9. **Una chiusura precisa.** Un ritorno all'immagine di apertura oppure ciò che si sa e ciò che resta aperto. Nessuna morale.
10. **Le conclusioni vengono dopo le ragioni.** In un testo che argomenta, un risultato o un'affermazione secca non apre il discorso se ne è la conseguenza: prima la premessa semplice, poi le difficoltà e le ragioni, poi la conclusione, introdotta da un nesso («per questo», «ne nasce», «per evitarlo»).
11. **I nessi legano le frasi.** Concessivi («sebbene», «pur»), causali («perché»), consecutivi («quindi», «per cui»), finali («per evitare»). Il rapporto fra due frasi è detto, non lasciato a un punto, a due punti o a un punto e virgola che lo sottintendono. Essere asciutti non vuol dire essere telegrafici.

## 2. Le cinque prove

1. Dopo il primo capoverso il lettore sa perché la cosa lo riguarda?
2. Ogni capoverso si riassume in una frase concreta?
3. Una frase potrebbe stare identica in un altro testo? Se sì, è generica.
4. Un collega competente la direbbe a pranzo?
5. Letta ad alta voce, scorre?

**Prova di sottrazione.** Dopo le cinque prove, per ogni periodo e per ogni sua parte si chiede che cosa il lettore non saprebbe più se venisse tolta. Se la risposta è «niente», si elimina; se resta un nucleo informativo, si riduce o si incorpora nella frase vicina. Il controllo è obbligatorio soprattutto per aperture e chiusure dei capoversi, frasi molto brevi, incisi e subordinate introduttive. Una frase breve non si salva perché dà ritmo: deve aggiungere un'informazione o segnare una svolta reale.

## 3. Indicatori di ritmo

Si misurano con `strumenti/controlla.py ritmo`. Sono diagnosi: guardano il ritmo e non lo producono. Non vedono i nessi: un testo di frasi di media lunghezza accostate senza legami passa tutti i controlli ed è comunque staccato (sezione 9). Un testo scritto per rientrare nei numeri diventa un altro tic.

Misure su cinque testi (parole per frase):

| Testo | Mediana | Dev. std. | Frasi fino a 8 parole | Frasi oltre 35 |
|---|---|---|---|---|
| Articolo di riferimento (Il Post, 2018) | 28 | 10,9 | 3% | 24% |
| Introduzione dell'utente | 17 | 16,8 | 27% | 18% |
| Versione A (regolare) | 25 | 10,1 | 5% | 14% |
| Versione B (cerniere) | 20 | 14,7 | 20% | 24% |
| Versione C (sintesi) | 24 | 9,7 | 6% | 8% |
| Introduzione completa dell'utente, dopo il ritocco (registro `cerniere`) | 20 | 15,8 | 21% | 21% |

Indicazioni di ordine di grandezza, da confermare su altri campioni:

- mediana tra 18 e 32 parole;
- deviazione standard tra 10 e 15; sotto 8 il ritmo è piatto (la versione C è al limite);
- frasi fino a 8 parole: poche, circa una ogni 150-250 parole nel registro `regolare`, una ogni 100 nel registro `cerniere`;
- nessuna sequenza di più di due frasi consecutive oltre 45 parole;
- nessuna struttura di paragrafo identica più di due volte;
- almeno qualche periodo lungo (oltre 35 parole) dove il ragionamento si sviluppa. Se manca del tutto, il testo si appiattisce.

Una regola del tipo «in ogni paragrafo una frase sotto le sei parole e una sopra le trentacinque» non descrive la buona prosa: la soddisfa un paragrafo su ventitré nell'articolo di riferimento.

## 4. La cerniera guadagnata

Una frase breve vale se **aggiunge un'informazione autonoma o capovolge un'attesa creata dal paragrafo che la precede.** «Il cratere non c'era» funziona perché il lettore ha appena seguito chi lo cercava. «Le ipotesi in campo sono tre» annuncia una classificazione e si può togliere. Anche una frase-etichetta come «Il primo scoglio è temporale» si elimina o si incorpora quando la frase successiva espone già per intero il problema del tempo. Una frase breve isolata in un proprio paragrafo si usa al massimo una volta in tutto il testo, di solito per la svolta più forte.

## 5. Le due famiglie di tic

Da consultare dopo la prima stesura. Una voce isolata è una svista, più voci vicine sono una firma: `controlla.py tic` segnala come «grappolo» il capoverso con tre o più indizi delle famiglie tipiche dei LLM.

**I segni sono sintomi.** I modelli ripiegano sulla formulazione più frequente, e così un fatto specifico si liscia in un'affermazione generica che suona importante. Cambiare la parola segnalata con un sinonimo nasconde il sintomo e lascia la causa. Davanti a una frase segnalata ci si chiede *che cosa sta facendo* (gonfiare il significato, coprirsi con un'autorità senza nome, smentire un'idea che nessuno ha espresso, riassumere sé stessa) e si interviene su quello: si cancella la frase, o la si sostituisce con il fatto specifico che sosteneva l'effetto. Se il fatto non c'è nel testo, non lo si inventa: si scrive la versione semplice e si fa la domanda all'autore nel rapporto.

**Tic tipici degli LLM**

- contrasto fittizio «non è X, è Y», «non solo X ma anche Y», «non si tratta di X ma di Y»;
- **negazioni difensive** («è A, non B», «non tanto B quanto A», «anziché B», «lungi dall'essere B»): chi scrive sembra difendersi dall'affermazione di qualcuno che sostiene B. Prova per ogni caso: B è stato davvero affermato nel testo, o è la tesi di qualcuno citato o discusso nel documento? Se no, B è un avversario inventato e si dice semplicemente «è A». La negazione resta quando B compare prima nel testo, quando è una posizione realmente sostenuta (una tesi che il documento sta confutando) o quando distingue due concetti che il lettore confonderebbe davvero. Anche una negazione che serve da cautela è informazione;
- **frasi ovvie**, che nessuno oserebbe contraddire («la sicurezza è importante», «serve un approccio equilibrato», «bisogna agire per il bene dell'umanità»). Prova del contrario: si scrive la frase opposta, e se suona assurda la frase non dice niente. Si salva solo se porta un'informazione specifica nel contesto (un dato, un compromesso, una scelta fra alternative reali, un vincolo) o se il suo contrario è una posizione che qualcuno sostiene davvero. Le frasi che introducono una distinzione o un passaggio del ragionamento («occorre sapere che cosa si sta contando») non sono ovvie solo perché il tono è metodologico. Nel dubbio si segnalano e non si eliminano;
- iperboli ed enfasi vuota («fondamentale», «cruciale», «imprescindibile», «rivoluzionario», «a 360 gradi», «vero e proprio», «svolge un ruolo chiave»), aggettivi di valore al posto di fatti;
- aperture e chiusure formulaiche («nel mondo di oggi», «in conclusione»);
- annunci di rilevanza («è importante sottolineare», «vale la pena notare») e meta-annunci («come abbiamo visto», «vediamo insieme»);
- elenchi di tre elementi o tre aggettivi, sistematici;
- perifrasi al posto di «è» («rappresenta», «si configura come», «riveste un ruolo»);
- gerundi di coda che commentano la frase («confermando la sua leadership»);
- metafore da brochure (panorama, tessuto, bussola, viaggio, navigare);
- battuta finale ripetuta a ogni sezione;
- paragrafi con la stessa architettura (apertura, sviluppo, battuta) più di due volte;
- morale in chiusura;
- **punteggiatura sostitutiva:** quando il trattino lungo è vietato, i due punti, il punto e virgola e le parentesi usati come pausa a effetto prendono il suo posto e restano lo stesso tic. Il rimedio è scrivere il nesso o cambiare la struttura della frase (sezione 8). `controlla.py tic` ne misura la densità (soglie provvisorie, nessun campione reale misurato) e la segnala sopra una certa quota in un testo di almeno 150 parole;
- connettivi a rotazione («inoltre», «tuttavia», «pertanto»). Il difetto è la rotazione meccanica di connettivi vuoti, ripetuti a ogni capoverso, non l'uso di nessi che esprimono un rapporto reale: togliere tutti i connettivi per eliminare il tic produce un testo telegrafico (sezione 9);
- **enfasi sul significato e sull'eredità:** il fatto ordinario seguito da una frase su perché conta o su che cosa «testimonia» («un vero punto di svolta», «si inserisce in un più ampio quadro», «un segno indelebile», «pone le basi per», «ha acceso il dibattito»). Rimedio: cancellare la frase, o sostituirla con un fatto che mostri l'importanza («L'istituto nacque nel 1989. Fu il primo ufficio regionale di statistica del Paese.»);
- **notorietà dimostrata con l'elenco delle testate** («numerose testate», «copertura mediatica», «presenza attiva sui social»). Si dice che cosa la cosa è o ha fatto; la copertura si cita solo come fonte di un'affermazione precisa;
- **linguaggio da brochure** per soggetti neutri («incastonato nel cuore di», «mozzafiato», «di fama internazionale», «ricco patrimonio», «imperdibile», «vasta gamma»). Si sostituisce l'aggettivo con il fatto che lo meriterebbe, o lo si toglie;
- **attribuzioni vaghe:** opinioni appese ad autorità senza nome o una fonte presentata come molte («secondo molti esperti», «numerosi studi dimostrano», «da più parti», «ampiamente considerato»). Si nomina la fonte, oppure si presenta l'affermazione come tesi dell'autore, oppure si taglia. **Nel nostro metodo:** lo stilista non può inventare la fonte, quindi segnala l'attribuzione nel rapporto come domanda per l'autore (o per il verificatore) e, se resta senza fonte, la scrive come tesi dell'autore o la toglie dichiarandolo. Non vale per le cautele con cui la fonte originale si protegge («si ritiene che», «secondo» seguito da un nome): sono informazione e si conservano;
- **formula delle sfide e delle prospettive:** «nonostante le difficoltà, X deve affrontare diverse sfide… continua a prosperare», spesso in una sezione finale. Un problema reale si dice dove serve, con i fatti; l'epilogo ottimista si toglie;
- **relazione vaga** quando è nota («associato a», «in connessione con»): si dice che cosa è accaduto («Nel 2017 era amministratrice delegata di ExampleCorp.»);
- **avvertenze didattiche:** «può variare», «tieni presente che», «dipende da diversi fattori». Si dice la cosa («Gli orari cambiano in inverno.» invece di «Gli orari possono variare.»);
- **residui della conversazione con il modello:** «Certamente!», «Ottima domanda», «Spero che questo ti sia utile», «Fammi sapere se…», «Ecco una versione…», «In questa sezione vedremo…»;
- **congetture sulle lacune e disclaimer sul sapere:** «al mio ultimo aggiornamento», «non è ampiamente documentato», «sulla base delle informazioni disponibili», seguiti da ipotesi su ciò che l'informazione mancante «probabilmente» è. Se qualcosa non si sa, lo si dice una volta, in modo concreto, con ciò che il lettore deve fare («Gli orari non sono pubblicati: telefonare prima.»);
- **segnaposto dimenticati:** `[Il tuo nome]`, `[Descrivi la sezione]`, `INSERT_URL`, `2026-XX-XX`. Le etichette di lavoro del metodo (`[MANCA: …]`, `[DA VERIFICARE]`) non sono segnaposto dimenticati e `controlla.py` non le segnala;
- **formattazione:** emoji davanti a titoli e voci, grassetto sparso nel corpo, tabelle di due o tre righe che starebbero in una frase, titoli con le iniziali maiuscole all'inglese («Il Museo Del Porto»). La formattazione appartiene alla struttura: lo stilista non la cambia e la segnala nel rapporto;
- **elegant variation:** «l'artista… il pittore… il creativo… il visionario» per un solo soggetto. Il rimedio è ripetere il nome o usare il pronome; lo strumento non la vede, la vede chi legge;
- domande retoriche generiche («ti sei mai chiesto…?»);
- elenchi con intestazione in grassetto dentro la riga.

**Tic tipici degli autori umani**

- burocratese e accademichese («alla luce di», «si pone l'accento», «stante»);
- **lessico da traduzione o da brochure:** «implementare», «impattare», «abilitare», «scalare», «leva», «sinergia», «paradigma», «approccio olistico», «delineare», «al fine di», «in termini di», «a livello di», «attualmente», «fornire» per tutto; Title Case all'inglese nei titoli;
- **vocabolario d'uso reale:** parole che un italiano non userebbe parlando o scrivendo a mano («utilizzare» dove basta «usare», «effettuare» dove basta «fare»), senza forzare un registro più basso di quello del documento;
- giornalese («fiume di polemiche», «braccio di ferro», «scenario»);
- paternalismo didattico («come vedremo», «è bene ricordare»);
- ironia compiaciuta e ammiccamenti al lettore;
- citazioni dotte decorative, usate per mostrare cultura e non per illuminare;
- periodi barocchi, con subordinate incassate una dentro l'altra;
- tono da coach o da guru;
- aneddoto personale di maniera in apertura;
- giudizi generici («molto interessante», «affascinante»);
- articoli omessi in stile telegrafico e aggettivi anteposti per calco dall'inglese («un importante risultato»).

**Calchi dall'inglese** (da cercare nei testi tradotti o scritti con un modello)

- **Passivi evitati per calco.** In italiano il *si* passivante e l'impersonale sono naturali. «Un Paese non si giudica da questo» è meglio di «questo non giudica un Paese». Si evita invece di far agire cose inanimate («il documento abilita», «la strategia guida»).
- gerundi appesi a fine frase («garantendo…», «permettendo di…»);
- aggettivo anteposto («un importante risultato» invece di «un risultato importante»);
- nomi accatastati senza preposizioni («gestione rischio cyber»);
- articoli omessi in stile telegrafico («riduce rischio di errori»);
- possessivi e pronomi soggetto superflui («il loro team», «egli»);
- virgola prima della «e» nelle enumerazioni («A, B, e C»); virgolette inglesi "..." al posto delle caporali «...»; pronomi soggetto espliciti («esso», «essa», «egli») dove l'italiano omette il soggetto;
- preposizioni calcate («focalizzarsi su», «avere un impatto su»);
- verbi d'azione dati a soggetti astratti («il piano abilita», «l'approccio guida»).

Le liste di parole sono un gusto editoriale e non un rilevatore: una parola isolata non prova niente.

**Oltre al lessico.** `controlla.py tic` guarda anche la struttura: capoversi lunghi senza numeri, nomi propri o date (il testo generico, che potrebbe stare identico in un altro testo), battute finali ripetute a ogni capoverso, aperture ripetute e tre frasi di fila con lo stesso attacco, punteggiatura sostitutiva e grappoli. Sono indizi con soglie provvisorie. I tic di moda più recenti («Detto questo», «Il punto è», «Pensala come», «da un lato… dall'altro», «Niente fronzoli. Niente slogan. Solo risultati.», «Il risultato?») sono segnalati «da valutare»: la lista è un'ipotesi da confermare sui testi reali e invecchia (vedi `manutenzione.md`, che ne dà la data). `controlla.py tic-confronto ORIGINE RISULTATO` conta le segnalazioni per famiglia prima e dopo la riscrittura e avverte se una famiglia è aumentata, cioè se un tic ne ha sostituito un altro.

## 6. Errori di architettura ricorrenti

Visti nella prova su Tunguska. Nessun ritocco di stile li risolve.

- L'immagine più forte del materiale sepolta in un inciso o in una subordinata, e un'apertura più debole al suo posto.
- Un argomento diviso in due punti del testo, o un'ipotesi finita sotto il titolo di un'altra.
- Il nome del soggetto che compare solo a metà del testo.
- Un salto cronologico (1908, poi 1930, poi 1927) senza che il testo lo dichiari.
- Uno scenario ipotetico presentato come se fosse la conseguenza naturale del caso trattato.
- Una sezione con tre argomenti diversi sotto un unico titolo.

## 7. Errori di fedeltà ricorrenti

Sei casi trovati in una prima stesura che si credeva fedele.

- «Visto dalle colline» diventato «sopra le colline».
- «Paragonabile a un terremoto di magnitudo 5» diventato «di magnitudo 5».
- «Ostacolando la coltivazione» diventato «impedendo di coltivare».
- «Hanno ipotizzato» diventato «dicono».
- La spedizione del 1927 diventata «la prima spedizione».
- Il Regno Unito diventato Inghilterra.

Il controllo di integrità e il confronto riga per riga servono a questo.

## 8. Preferenze di stile emerse dall'utente

Registrate dopo la prova sull'Introduzione (26 ottobre 2026). Si applicano per default quando lavora lo stesso utente, e si ampliano con nuovi casi.

- **Cornice asciutta.** «Per un fisico… fu un evento fisico» migliora su «Un fisico… risponderà che fu un evento fisico». Vale in generale per le cornici ripetute: meglio la forma breve e diretta.
- **Il gerundio di coda diventa una frase propria.** «…ad altissima velocità, cambiando l'ambiente di detriti» → «…ad altissima velocità. Cambiarono l'ambiente di detriti».
- **Nomi astratti da verbi o participi** quando la frase ci guadagna in concretezza («il perseguimento non coordinato di missioni» → «missioni perseguite senza coordinamento»), purché il senso resti uguale e l'inciso resti chiaro.
- **Asciutto vuol dire senza fronzoli, non meno informazione.** Una chiusura a effetto senza contenuto o un'immagine non preparata sono fronzoli e si segnalano. Una cautela, un distinguo o una conclusione che dicono qualcosa si conservano, anche se la frase si accorcia. Una negazione che serve da cautela è informazione: «Un Paese non si giudica da questo» (si passivante) o «Non si può giudicare un Paese sulla base di questo».
- **La scorrevolezza vale più di una forma che affatica,** anche se corretta e anche se dell'autore. Frasi ampollose, barocche e ridondanti si riducono; i periodi troppo lunghi si spezzano; ma senza cadere nello staccato.
- **I nessi non sono fronzoli.** «Una cosa è essere senza fronzoli ed evitare frasi inutili e prive di significato, un'altra è essere telegrafici.» Un testo asciutto ma privo di legami fra le frasi è secco e spigoloso. Spezzare un periodo senza che la frase seguente riprenda il filo con un nesso produce staccato anche con frasi di media lunghezza (caso del 26 ottobre 2026, testo su safety e security: quattro versioni prima di arrivare al ritmo giusto).
- **Le conclusioni dopo le ragioni.** Un'affermazione apodittica o un risultato enunciato prima del discorso di cui è conseguenza nuoce alla chiarezza. Si riordina anche spostando frasi.
- **Due punti e punto e virgola** non per sottintendere un rapporto logico: si scrive il nesso («perché», «mentre», «quindi»). Restano per elenchi, citazioni e definizioni. Vale per l'autore anche dove non è un divieto assoluto come quello dei trattini lunghi.
- **Il nesso entra nella frase quando il rapporto è stretto.** «La sicurezza operativa pone un problema di attribuzione: un investimento può ridurre il rischio…» scorre meglio come «La sicurezza operativa pone un problema di attribuzione poiché un investimento può ridurre il rischio…». Non si sostituisce meccanicamente il segno con un punto e un connettivo in apertura: una nuova frase si crea solo se porta un passaggio autonomo e la pausa è guadagnata.
- **Frasi-etichetta e incisi passano la prova di sottrazione.** Se «Il primo scoglio è temporale» non aggiunge nulla alla spiegazione che segue, si elimina o si incorpora. Lo stesso vale per un inciso o una subordinata introduttiva che ripete il contesto già noto. Per ogni elemento si sceglie fra conservare, ridurre, incorporare ed eliminare; il ritmo, da solo, non giustifica la conservazione.
- **La cadenza con cerniere brevi** dell'autore si conserva quando ogni cerniera supera la prova di sottrazione: l'utente ha chiesto di intervenire sugli effetti retorici e non di appiattire il ritmo, ma il ritmo da solo non salva una frase priva di informazione.
- **La fonte resta dietro il fatto verificato.** Formule come «la documentazione descrive», «il rapporto attesta» e «le fonti mostrano» non devono proteggere l'autore da un'affermazione che può formulare direttamente e sostenere con una nota. L'attribuzione resta quando identifica chi dichiara, stima o valuta qualcosa oppure quando segnala un conflitto o un limite probatorio.

## 9. Intoppi di lettura

Si cercano con `strumenti/controlla.py scorrevolezza` e si giudicano leggendo ad alta voce. Indizi: periodo molto lungo; molte virgole in poco spazio; tre o più «che»; doppia negazione; «tale», «suddetto», «quest'ultimo», «il quale»; catena di complementi con molti «di»; tre o più nomi astratti in una frase; gerundio di coda; passivi ripetuti; quattro frasi brevi di fila (staccato); **frase-etichetta che la frase successiva ripete per intero**; **inciso o premessa che non cambia il senso**; **frasi accostate senza nessi**, anche di media lunghezza, di cui il lettore deve indovinare il rapporto; **due punti o punto e virgola che sottintendono un nesso**; **conclusione o affermazione secca detta prima delle ragioni**. Gli ultimi cinque non li vede nessun programma. Sono indizi: un elenco chiaro può essere lungo, e una frase breve può essere un buon punto di svolta quando aggiunge informazione.

Rimedi, in ordine: eliminare o incorporare le frasi e le parti di frase che falliscono la prova di sottrazione; avvicinare soggetto e verbo; spezzare dove l'idea cambia, alternando le lunghezze e legando i pezzi con un nesso; sostituire il nome astratto con un verbo; ripetere il nome al posto di un pronome ambiguo; dire in positivo ciò che è detto per negazione doppia; scrivere il nesso che manca (e riordinare, se la conclusione precede le ragioni).

## 10. Avvertenze

- Il modello positivo nasce da due testi. Va ampliato con altri campioni di autori diversi, di data anteriore al 2023, nel registro che interessa (per esempio rapporti e analisi).
- Un testo senza i tic può essere comunque noioso. Le cinque prove e il giudizio di una persona valgono più dei numeri.
- Altre risorse, da attaccare alla fase 3 quando disponibili: le guide di grammatica normativa, lessico, pattern e registri di `italiano-scrittura-anti-ai` (cartella `references/`).

## 11. Che cosa non è un segno

Il livello di intervento dello stilista è alto, ed è qui che si rischia di correggere troppo. Questi tratti non indicano scrittura automatica, e cambiarli peggiora il testo:

- grammatica e ortografia corrette;
- registro formale, parole lunghe, prosa «neutra» in genere;
- un registro che mescola tono colloquiale e formale;
- un singolo connettivo («tuttavia», «pertanto») o una singola parola dell'elenco dei tic: contano il numero e la vicinanza, e per questo `controlla.py` segnala i grappoli;
- affermazioni senza fonte (di quelle si occupa il verificatore, non lo stile);
- formattazione corretta e uniforme;
- parole usate in senso proprio o di settore («panorama» per un dipinto, «robusto» in statistica, «navigare» in mare) e nomi propri;
- citazioni di persone o di fonti, titoli di opere, testo legale: non si riscrivono mai per togliere un segno.

Un segno tenuto di proposito (una citazione, un nome proprio, una parola in senso letterale) si dichiara nel rapporto. Un testo con zero segnalazioni non è per questo un buon testo: valgono sempre le cinque prove della sezione 2.
