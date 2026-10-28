# Diagnosi: il modello di buona prosa inglese e i suoi nemici

Riferimento per la fase 3. Le sezioni 1-4 servono prima e durante la scrittura. La 5, la 6 e la 7 si consultano dopo la prima stesura, come controllo. È il gemello di `diagnosi.md` del plugin `italiano`, con la stessa numerazione fino alla 10: il modello e i principi sono gli stessi, cambiano i tic, i calchi e il trattamento dei passivi. La sezione 11, solo inglese, dice che cosa *non* è un segno.

**Stato della calibrazione.** Questo file nasce senza che sia stato analizzato nessun testo inglese di un autore reale. Il modello positivo è quello italiano, riletto per l'inglese; le soglie di ritmo (sezione 3) sono derivate da quelle italiane e dichiarate provvisorie; le liste di tic vengono dalla conoscenza dei testi da LLM, della prosa aziendale, accademica e giornalistica, dal file di stile `en-us.md` del plugin `revisione` e dal repertorio dei segni di scrittura automatica che la comunità di Wikipedia ha raccolto (vedi `NOTE-LEGALI.md`: le famiglie e le parole da tenere d'occhio sono riformulate, non copiate). Quando l'utente fornirà i campioni (3-5 brani di autori reali anteriori al 2023, 2-3 testi noiosi o artefatti), la sezione 3 si ricalibra e la 1 si arricchisce con ciò che i brani mostrano.

## 1. Modello positivo

Principi validi in qualunque lingua, tradotti in pratica inglese. Sono tratti da imitare per principio, non per forma.

1. **Apri con un'immagine concreta e verificabile.** Un luogo, un'ora, un gesto, un numero. L'interesse nasce dal fatto, mai da una premessa sul perché il tema conta («In today's fast-paced world…»).
2. **Una persona dentro i fatti,** quando il materiale ne offre una. Il racconto passa da lei e si chiude, se serve, tornando a lei.
3. **Dì con precisione ciò che non si sa.** Attribuisci con nome e ruolo: chi, di quale università, quando. Distingui ciò che è accertato da ciò che si crede.
4. **Numeri con un termine di paragone,** sempre attribuiti.
5. **Pochi aggettivi di valore.** Verbi e gesti concreti. Il soggetto della frase è un personaggio o una cosa concreta, il verbo è un'azione: *Kulik found no crater*, non *The absence of a crater was observed by Kulik*.
6. **Titoletti brevi e vari,** non tutti nella stessa forma.
7. **Ritmo che viene dal contenuto.** Si alternano scena, dato, ipotesi, cifra. La frase di base è piana. Le frasi brevi compaiono dove il discorso svolta.
8. **Contrasti solo se reali.** *Not a rock but a comet* va bene se qualcuno ha sostenuto la pietra.
9. **Una chiusura precisa.** Un ritorno all'immagine di apertura oppure ciò che si sa e ciò che resta aperto. Nessuna morale.

Due abitudini della prosa inglese piana, utili per la scorrevolezza:

- **Il noto prima, il nuovo dopo.** La frase parte da ciò che il lettore sa già e finisce sull'informazione nuova, che è anche il punto su cui cade l'accento. *The trees at the center still stood, stripped of their branches.* L'informazione importante a metà frase si perde.
- **Un'idea per frase, parallelismo negli elenchi.** Le voci di un elenco hanno la stessa forma grammaticale.

## 2. Le cinque prove

1. Dopo il primo capoverso il lettore sa perché la cosa lo riguarda?
2. Ogni capoverso si riassume in una frase concreta?
3. Una frase potrebbe stare identica in un altro testo? Se sì, è generica.
4. Un collega competente la direbbe a pranzo?
5. Letta ad alta voce, scorre?

## 3. Indicatori di ritmo (PROVVISORI)

Si misurano con `strumenti/controlla.py --lingua en ritmo`. Sono diagnosi: guardano il ritmo e non lo producono. Un testo scritto per rientrare nei numeri diventa un altro tic.

**Nessuna misura è stata fatta su testi inglesi di autori reali.** Le soglie in uso sono quelle italiane, scalate di circa 0,85 perché a parità di contenuto l'inglese usa meno parole dell'italiano:

| Misura | Italiano (calibrato su due testi) | Inglese (provvisorio) |
|---|---|---|
| Mediana, parole per frase | 18-32 | 15-27 |
| Frase breve | fino a 8 parole | fino a 7 |
| Frase lunga | oltre 35 | oltre 30 |
| Serie di frasi molto lunghe | più di 2 oltre 45 parole | più di 2 oltre 38 |
| Deviazione standard: piatto / uniforme | sotto 8 / sotto 10 | sotto 7 / sotto 8,5 |
| Frasi brevi per registro (regolare, cerniere, tecnico) | 15%, 25%, 10% | 15%, 25%, 10% (da rivedere) |

Il rapporto 0,85 è un'ipotesi, non una misura. Un testo inglese buono può cadere fuori da questi intervalli, e un testo mediocre può rientrarci. Finché i campioni non sono stati misurati, gli avvisi di ritmo si leggono come «guarda meglio qui» e non come errori, e il rapporto lo dice.

Restano valide, perché non dipendono dalla lingua: nessuna struttura di paragrafo identica più di due volte; almeno qualche periodo lungo dove il ragionamento si sviluppa; una frase breve isolata in un paragrafo proprio al massimo una volta in tutto il testo.

## 4. La cerniera guadagnata

Una frase breve vale se **capovolge un'attesa creata dal paragrafo che la precede.** *There was no crater.* funziona perché il lettore ha appena seguito chi lo cercava. *There are three main theories.* annuncia una classificazione e si può togliere o unire alla frase vicina.

## 5. Le famiglie di tic

Da consultare dopo la prima stesura. Una voce isolata è una svista, più voci vicine sono una firma: `controlla.py --lingua en tic` segnala come «grappolo» il capoverso con tre o più indizi delle famiglie tipiche dei LLM.

**I segni sono sintomi.** I modelli ripiegano sulla formulazione più frequente, e così un fatto specifico si liscia in un'affermazione generica che suona importante. Cambiare la parola segnalata con un sinonimo, o un em dash con un altro trattino, nasconde il sintomo e lascia la causa. Davanti a una frase segnalata ci si chiede *che cosa sta facendo* (gonfiare il significato, coprirsi con un'autorità senza nome, smentire un'idea che nessuno ha espresso, riassumere sé stessa) e si interviene su quello: si cancella la frase, o la si sostituisce con il fatto specifico che sosteneva l'effetto. Se il fatto non c'è nel testo, non lo si inventa: si scrive la versione semplice e si fa la domanda all'autore nel rapporto.

**Tic tipici degli LLM**

- contrasto fittizio: *it's not X, it's Y*, *this isn't just X, it's Y*, *not just X but also Y*, *more than just X*, *far from being X*. In inglese è il segno più riconoscibile;
- negazioni difensive: *A, rather than B*, *instead of B*, *as opposed to B*, *not so much B as A*, quando nessuno ha sostenuto B. Prova: B compare prima nel testo, o è una posizione realmente sostenuta? Se no, si dice «è A»;
- aperture e chiusure formulaiche: *In today's fast-paced world*, *In the ever-evolving landscape of*, *In the realm of*, *When it comes to*, *At its core*, *Let's dive in*, *In conclusion*, *Overall,*, *Ultimately,*, *At the end of the day*;
- annunci di rilevanza e meta-annunci: *It's worth noting that*, *It is important to note*, *Notably,*, *Importantly,*, *Here's the thing*, *Here's the key:*, *Let's unpack this*;
- frasi ovvie (prova del contrario: se il contrario è assurdo, la frase non dice niente): *Collaboration is key.*, *A balanced approach is needed.*;
- iperboli ed enfasi vuota: *crucial*, *pivotal*, *vital*, *groundbreaking*, *game-changing*, *transformative*, *unprecedented*, *remarkable*, *truly*, *genuinely*, *deeply*, *fundamentally*;
- lessico da LLM: *delve*, *tapestry*, *testament*, *landscape*, *realm*, *journey*, *navigate* (in senso figurato), *leverage* (verbo), *robust*, *seamless*, *holistic*, *foster*, *harness*, *unlock*, *empower*, *underscore*, *showcase*, *shed light on*, *intricate*, *multifaceted*, *nuanced* (quando è vuoto), *vibrant*, *beacon*. Non vanno segnalati nel senso proprio o di settore (*landscape* in geografia, *robust* in statistica, *leverage* in finanza);
- perifrasi al posto di *is* e *has*: *serves as*, *stands as*, *represents*, *marks*, *boasts*, *features*, *plays a pivotal role*;
- triadi sistematiche (tre nomi, tre aggettivi, tre verbi) e serie di frasi brevi a effetto (*No hype. No fluff. Just results.*);
- participi appesi a fine frase che commentano la frase (*, highlighting its importance*, *, ensuring long-term success*, *, reflecting a broader trend*) quando sono sistematici;
- **abuso dell'em dash:** più di una coppia per capoverso, o più di tre o quattro per pagina, o un em dash al posto di una virgola o di un punto per puro effetto. È fra i tic più noti. Il rimedio non è sostituire il carattere con un trattino spaziato (peggio): è cambiare la struttura della frase;
- connettivi a rotazione a ogni capoverso: *Moreover*, *Furthermore*, *Additionally*, *In addition*, *However*, *Therefore*, *Thus*, *Consequently*;
- paragrafi con la stessa architettura (tesi, spiegazione, frase di chiusura) più di due volte; battuta finale ripetuta a ogni sezione; morale in chiusura;
- domande retoriche seguite dalla risposta (*The result? Chaos.*);
- elenchi puntati con intestazione in grassetto e due punti su ogni voce dove servirebbe prosa; titoletti e grassetti ovunque;
- **enfasi sul significato e sull'eredità:** il fatto ordinario seguito da una frase su perché conta o su che cosa «riflette» (*reflects broader trends*, *enduring legacy*, *marking a pivotal moment*, *setting the stage for*, *a key turning point*, *has generated debate about*). Rimedio: cancellare la frase, o sostituirla con un fatto che mostri l'importanza (*The institute was set up in 1989. It was the first regional statistics office in the country.*);
- **notorietà dimostrata con l'elenco delle testate** (*independent coverage*, *featured in national media outlets*, *active social media presence*). Si dice che cosa la cosa è o ha fatto; la copertura si cita solo come fonte di un'affermazione precisa;
- **linguaggio da brochure** per soggetti neutri (*nestled in the heart of*, *breathtaking*, *world-class*, *renowned*, *a diverse array of*, *rich heritage*, *commitment to excellence*). Si sostituisce l'aggettivo con il fatto che lo meriterebbe, o lo si toglie;
- **attribuzioni vaghe:** opinioni appese a autorità senza nome o una fonte presentata come molte (*experts say*, *observers have noted*, *industry reports*, *studies show*, *widely regarded as*, *some critics argue*). Si nomina la fonte, oppure si presenta l'affermazione come tesi propria dell'autore, oppure si taglia. **Nel nostro metodo:** lo stilista non può inventare la fonte, quindi segnala l'attribuzione nel rapporto come domanda per l'autore (o per il verificatore) e, se resta senza fonte, la scrive come tesi dell'autore o la toglie dichiarandolo. Non vale per le cautele con cui la fonte originale si protegge (*is thought to be*, *according to*): sono informazione e si conservano;
- **formula delle sfide e delle prospettive:** *Despite its…, X faces several challenges… Despite these challenges, X continues to thrive*, spesso in una sezione finale. Un problema reale si dice dove serve, con i fatti; l'epilogo ottimista si toglie;
- **definizione del titolo come cosa** (*X refers to…*, *The list of Y is a curated compilation of…*): si parte dal soggetto (*A catchment area is the area a hospital draws patients from.*);
- **relazione vaga** quando è nota: *associated with*, *in connection with*, al posto di dire che cosa è accaduto (*In 2017 she was CEO of ExampleCorp.*);
- **perifrasi di *is* e *has* oltre quelle già elencate:** *represents*, *operates as*, *embodies*, *constitutes*, *features* e *offers* nel senso di «ha», *began his career as* per «era», *ventured into*. Sono segnalate «da valutare»: sono verbi normali quando dicono qualcosa;
- **avvertenze didattiche:** *may vary*, *keep in mind*, *depending on various factors*. Si dice la cosa (*Hours change in winter.* invece di *Hours may vary.*);
- **lessico di nuova generazione**, oltre quello già elencato: *garner*, *interplay*, *bolster*, *enhance*, *intricacies*, *align with*, *resonate with*, *valuable insights*, *additionally* in apertura di frase. Una parola isolata non prova niente; contano il numero e la vicinanza;
- **elegant variation:** *the artist… the painter… the visionary* per un solo soggetto. Il rimedio è ripetere il nome o usare il pronome; lo strumento non lo vede, lo vede chi legge;
- **residui della conversazione con il modello:** *I hope this helps*, *Certainly!*, *Great question*, *Let me know if…*, *Here is a revised version*, *In this section, we will…*, *As an AI*;
- **congetture sulle lacune e disclaimer sul sapere:** *As of my last update*, *not widely documented*, *based on available information*, *maintains a low profile*, seguiti da ipotesi su ciò che l'informazione mancante «probabilmente» è. Se qualcosa non si sa, lo si dice una volta, in modo concreto, con ciò che il lettore deve fare (*Opening hours aren't posted; call ahead.*);
- **segnaposto dimenticati:** `[Your Name]`, `[Describe the section]`, `INSERT_URL`, `2026-XX-XX`. Le etichette di lavoro del metodo (`[MANCA: …]`, `[DA VERIFICARE]`) non sono segnaposto dimenticati e `controlla.py` non le segnala;
- **formattazione:** emoji davanti a titoli e voci, grassetto sparso nel corpo, tabelle di due o tre righe che starebbero in una frase, intestazioni in Title Case dove il documento usa un'altra convenzione. La formattazione appartiene alla struttura: lo stilista non la cambia (vedi la skill) e la segnala nel rapporto.

**Tic tipici degli autori umani**

- **parole ricercate al posto delle semplici:** *authored* per *wrote*, *passed away* per *died*, *relocated* per *moved*, *attempted* per *tried*, *commenced* per *began*, *facilitate*, *endeavor*, *ascertain*. L'inglese piano usa le parole corte e dice «è» e «ha»;
- **corporate-speak:** *synergy*, *circle back*, *touch base*, *bandwidth* (figurato), *deep dive*, *low-hanging fruit*, *move the needle*, *going forward*, *stakeholders*, *learnings*, *takeaways*, *best practices*, *paradigm shift*, *value-add*, *utilize* al posto di *use*, *impactful*, *actionable*, *scalable*;
- **accademichese e burocratese:** *it should be noted that*, *in the context of*, *with respect to*, *in terms of*, *a plethora of*, *the extent to which*, *aforementioned*, *whereby*, *thereof*, *in order to* al posto di *to*, *due to the fact that*, *a number of*, *at this point in time*, *prior to*; nominalizzazioni (*the implementation of the evaluation of*), soggetti astratti che «guidano» o «abilitano» (*the framework drives alignment*);
- **giornalese:** *slammed*, *in a bid to*, *sparked*, *amid*, *embattled*, *vowed*, *war of words*, *fierce debate*, *perfect storm*, *tip of the iceberg*, *a growing chorus*, *sources say*;
- paternalismo didattico (*as we will see*, *it bears repeating*), ironia compiaciuta, ammiccamenti al lettore;
- citazioni dotte decorative, usate per mostrare cultura e non per illuminare;
- periodi barocchi, con subordinate incassate una dentro l'altra;
- tono da coach o da guru; aneddoto personale di maniera in apertura;
- giudizi generici (*very interesting*, *fascinating*).

**Calchi dall'italiano** (da cercare nei testi tradotti o scritti con un modello, anche se l'autore non lo sa)

- **Falsi amici:** *actually* per «attualmente» (è *currently*), *actual* per «attuale» (*current*), *eventually* per «eventualmente» (*possibly*), *eventual* per «eventuale» (*possible*), *to realize* per «realizzare» nel senso di «fare» (*carry out*, *build*), *sensible* per «sensibile» (*sensitive*), *to assist* per «assistere» nel senso di «essere presente» (*attend*), *to pretend* per «pretendere» (*claim*, *demand*), *to evidence* per «evidenziare» (*show*, *highlight*), *conjuncture* per «congiuntura» (*situation*, *economic cycle*), *formation* per «formazione» nel senso di addestramento (*training*), *preoccupation* per «preoccupazione» (*concern*), *to elaborate* per «elaborare» (*develop*, *process*), *logic* per «logica» nel senso di «criterio» (*rationale*), *politics* e *policy* scambiati per «politica», *economy* ed *economics* scambiati. Un termine non si segnala solo perché somiglia a una parola italiana: si segnala quando il senso inglese è diverso da quello voluto.
- **Verbi riflessivi resi alla lettera:** *establishes itself as* per «si afferma come», *enters a phase of* per «entra in una fase di», *the process realizes itself*.
- **Articolo determinativo sui nomi generici:** *The power is shifting*, *The demography is predictable* dove l'inglese dice *Power is shifting*, *Demography is predictable*.
- **Reggenze e preposizioni calcate:** *depends from*, *participate to*, *discuss about*, *since three years*, *in the nineties* (è *in the 1990s*), *in agreement of*, *interested to* (è *interested in*), *different than/from*.
- **Strutture:** *from one side… from the other side* (è *on the one hand… on the other*), *as it is known*, *in fact* usato come «infatti», *the same* come pronome, *the latter* ripetuto, periodi lunghissimi con subordinate annidate in stile italiano, presente perfetto e passato semplice scambiati (*I live here since 2015*).
- **Registro troppo alto:** *in relation to*, *with reference to*, *as regards* ovunque.
- **Sintassi dell'aggettivo:** aggettivo dopo il nome (*a country developed*).
- **Plurali e articoli sbagliati:** *informations*, *advices*, *knowledges*, *researches*, *equipments*, *the people is*, *the police are* contro *is*.
- **Possessivi e pronomi superflui:** *the their team*, *he, the minister,* ripetuto.
- **Ortografia britannica per inerzia di scuola:** *organise*, *colour*, *centre*, *towards* (vedi `convenzioni-us.md`).

**Passivi.** In italiano il *si* passivante e l'impersonale sono naturali e non si eliminano per calco. **Questa regola non vale per l'inglese**: in inglese il passivo è più sconsigliato. Si preferisce la voce attiva con un soggetto concreto. Il passivo resta quando:

- l'agente è ignoto o irrilevante (*Seismic stations recorded the shock* va bene; *The samples were frozen overnight* anche);
- il tema del paragrafo è il paziente e va tenuto come soggetto;
- il passivo porta una cautela di attribuzione che non si può attivare senza inventare chi parla (*It is thought that…*): vedi il contratto, sezione sulle cautele.

Non si trasforma mai un passivo in attivo inventando l'agente.

Le liste di parole sono un gusto editoriale e non un rilevatore: una parola isolata non prova niente.

## 6. Errori di architettura ricorrenti

Gli stessi dell'italiano. Nessun ritocco di stile li risolve.

- L'immagine più forte del materiale sepolta in un inciso o in una subordinata, e un'apertura più debole al suo posto.
- Un argomento diviso in due punti del testo, o un'ipotesi finita sotto il titolo di un'altra.
- Il nome del soggetto che compare solo a metà del testo.
- Un salto cronologico (1908, poi 1930, poi 1927) senza che il testo lo dichiari.
- Uno scenario ipotetico presentato come se fosse la conseguenza naturale del caso trattato.
- Una sezione con tre argomenti diversi sotto un unico titolo.

## 7. Errori di fedeltà ricorrenti

Quelli visti sull'italiano, resi in inglese, più quelli propri dell'inglese.

- *Seen from the hills* diventato *above the hills*.
- *Comparable to a magnitude 5 earthquake* diventato *a magnitude 5 earthquake*.
- *Hindering farming* diventato *preventing farming*.
- *Researchers hypothesize* diventato *researchers say*.
- La spedizione del 1927 diventata *the first expedition*.
- *The United Kingdom* diventato *England*; *U.S.* e *America* scambiati; *the Soviet Union* e *Russia* scambiati.
- *Is thought to be* diventato *is*; *could have* diventato *did*; *may* diventato *will*.
- *About 2,000* diventato *2,000*; *at least* diventato *about*.
- Un attivo costruito su un passivo che non nominava l'agente (*The decision was criticized* → *Critics slammed the decision*).

Il controllo di integrità e il confronto riga per riga servono a questo.

## 8. Preferenze di stile emerse dall'utente

Ricavate sui testi italiani (prova sull'Introduzione, 26 ottobre 2026). Valgono per principio anche in inglese e si confermano sui primi testi inglesi.

- **Cornice asciutta.** *For a physicist, it was a physical event* migliora su *A physicist will answer that it was a physical event*. Vale in generale per le cornici ripetute.
- **Il participio o gerundio di coda diventa una frase propria.** *…at very high speed, changing the debris environment* diventa *…at very high speed. They changed the debris environment.*
- **Nominalizzazioni sostituite da verbi o participi** quando la frase ci guadagna in concretezza, purché il senso resti uguale.
- **Asciutto vuol dire senza fronzoli, non meno informazione.** Una chiusura a effetto senza contenuto o un'immagine non preparata sono fronzoli e si segnalano. Una cautela, un distinguo o una conclusione che dicono qualcosa si conservano, anche se la frase si accorcia. Una negazione che serve da cautela è informazione.
- **La scorrevolezza vale più di una forma che affatica,** anche se corretta e anche se dell'autore. Frasi ampollose, barocche e ridondanti si riducono; i periodi troppo lunghi si spezzano; ma senza cadere nello staccato.
- **La cadenza con cerniere brevi** dell'autore si conserva: l'utente ha chiesto di intervenire sugli effetti retorici e non di appiattire il ritmo.

## 9. Intoppi di lettura

Si cercano con `strumenti/controlla.py --lingua en scorrevolezza` e si giudicano leggendo ad alta voce. Indizi in inglese:

- periodo molto lungo (oltre 38 parole) o incassato (molte virgole);
- quattro o più *that/which/who* nella stessa frase;
- doppia negazione (*not uncommon*, *not without*);
- **riferimento vago:** frase che apre con *This is…*, *That means…* senza un nome che dica a che cosa si riferisce (*This is a problem* → *This delay is a problem*);
- **apertura espletiva** (*It is…*, *There are…*) dove un soggetto concreto sarebbe più diretto;
- **pila di nomi** (tre o più nomi di seguito che si modificano, *climate policy risk assessment framework*) e catena di *of* (quattro o più);
- **nominalizzazioni** (*implementation*, *utilization*, *consideration*) al posto del verbo;
- *the latter*, *the former*, *aforementioned*, *whereby*, *thereof*;
- participio di coda (*, highlighting…*);
- passivi ripetuti nella stessa frase;
- cautele accumulate (*may potentially perhaps*);
- quattro frasi brevi di fila (staccato).

Sono indizi: un elenco chiaro può essere lungo, e una frase breve può essere un buon punto di svolta.

Rimedi, in ordine: avvicinare soggetto e verbo; spezzare dove l'idea cambia, alternando le lunghezze; sostituire il nome astratto con un verbo; dare un nome al posto di *this*; trasformare il passivo in attivo quando l'agente è nel testo; sciogliere la pila di nomi con preposizioni o con un verbo; ripetere il nome al posto di un pronome ambiguo; dire in positivo ciò che è detto per negazione doppia.

## 10. Avvertenze

- Il modello positivo non è stato verificato su campioni inglesi. Va ampliato con altri campioni di autori diversi, di data anteriore al 2023, nel registro che interessa.
- Un testo senza i tic può essere comunque noioso. Le cinque prove e il giudizio di una persona valgono più dei numeri.
- Il testo inglese di un autore italiano ha un altro difetto tipico oltre ai calchi: la sintassi italiana (periodi lunghi, subordinate annidate, soggetto in fondo). Lo stilista lo tratta come un intoppo di lettura.

## 11. Che cosa non è un segno (solo inglese)

Il livello di intervento dello stilista è alto, ed è qui che si rischia di correggere troppo. Questi tratti non indicano scrittura automatica, e cambiarli peggiora il testo:

- grammatica e ortografia perfette;
- registro formale, parole lunghe, prosa «neutra» in genere;
- un registro che mescola tono colloquiale e formale;
- un singolo connettivo (*However*, *Therefore*) o una singola parola dell'elenco dei tic: contano il numero e la vicinanza, e per questo `controlla.py` segnala i grappoli;
- affermazioni senza fonte (di quelle si occupa il verificatore, non lo stile);
- formattazione corretta e uniforme;
- parole usate in senso proprio o di settore (*landscape* per un dipinto, *robust* in statistica, *leverage* in finanza, *Key Largo* come nome proprio);
- citazioni di persone o di fonti, titoli di opere, testo legale: non si riscrivono mai per togliere un segno.

Un segno tenuto di proposito (una citazione, un nome proprio, una parola in senso letterale) si dichiara nel rapporto. Un testo con zero segnalazioni non è per questo un buon testo: valgono sempre le cinque prove della sezione 2.
