#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Controlli meccanici per il metodo in tre ruoli (scrittore, verificatore, stilista).

Solo libreria standard, nessun accesso alla rete, nessuna scrittura di file.
Misura e segnala: sono indizi da valutare, non verdetti.

  python3 -I controlla.py [--lingua it|en] integrita ORIGINE RISULTATO [--consenti-aggiunte] [--ignora-id] [--righe DA-A]
  python3 -I controlla.py [--lingua it|en] struttura ORIGINE RISULTATO
  python3 -I controlla.py [--lingua it|en] ritmo [--registro regolare|cerniere|tecnico] FILE [FILE ...]
  python3 -I controlla.py [--lingua it|en] tic FILE [FILE ...]
  python3 -I controlla.py [--lingua it|en] scorrevolezza FILE [FILE ...]
  python3 -I controlla.py [--lingua it|en] tic-confronto ORIGINE RISULTATO
  python3 -I controlla.py confronta FILE_ITALIANO FILE_INGLESE

«confronta» mette a fronte le due versioni (italiana e inglese) dello stesso documento, sezione per sezione:
numeri, nomi, lunghezza e cautele. Non usa --lingua: applica a ciascun file il profilo della sua lingua.

--lingua è la lingua del testo (it per l'italiano, en per l'inglese americano); senza l'opzione vale it.
Per l'inglese le soglie di ritmo e di scorrevolezza sono PROVVISORIE: derivate da quelle italiane,
non ancora calibrate su campioni inglesi.

Codici di uscita: 0 nessun problema bloccante, 1 problema bloccante, 2 uso errato.
La sezione "Note" finale di ogni file (titolo "## Note") non fa parte del testo.
Con --righe DA-A, integrita legge solo quelle righe dell'ORIGINE: serve a controllare un pezzo di un documento
lungo (RISULTATO è il file con il solo pezzo rivisto).
"""
import re
import statistics as st
import sys
from collections import Counter

RE_NUM = re.compile(r"\d+(?:[.,]\d+)*")
RE_PAROLA = re.compile(r"[^\W\d_][\w'’\-]*")

LINGUE = ("it", "en")

# Ultimo aggiornamento dei lessici di tic (TIC_IT, TIC_EN, GRAPPOLO_*). Le liste invecchiano con le generazioni di modelli:
# la procedura per aggiornarle è in riferimenti/manutenzione.md.
LESSICI_DATA = "2026-10-28"


# ---------------------------------------------------------------- profili

def normalizza_numero_it(s):
    if re.fullmatch(r"\d{1,3}(?:\.\d{3})+", s):
        return s.replace(".", "")
    return s.replace(",", ".")


def normalizza_numero_en(s):
    if re.fullmatch(r"\d{1,3}(?:,\d{3})+", s):
        return s.replace(",", "")
    return s


CAUTELE_IT = {
    "secondo": r"\bsecondo\b",
    "si crede / si ritiene": r"\bsi (?:crede|ritiene)\b|\bè ritenut[aoie]\b",
    "condizionale (avrebbe, potrebbe...)": r"\b(?:avrebbe|avrebbero|potrebbe|potrebbero|sarebbe|sarebbero|dovrebbe)\b",
    "ipotesi / ipotizzare": r"\bipotizz\w*|\bipotesi\b",
    "forse / probabilmente": r"\bforse\b|\bprobabil\w*",
    "circa / intorno a": r"\bcirca\b|\bintorno a\b",
    "sembra / pare": r"\bsembr\w*|\bpare\b",
    "stima": r"\bstim\w*",
}

# Per l'inglese i modelli sono sensibili alle maiuscole: "May" è un mese, "may" è una cautela.
CAUTELE_EN = {
    "according to": r"\b[Aa]ccording to\b",
    "is believed / thought / said": r"\b(?:is|are|was|were|been|be) (?:believed|thought|said|reported|considered|assumed|presumed|alleged|claimed|understood)\b|\breportedly\b|\ballegedly\b|\bsupposedly\b",
    "modali (would, could, might, may, should)": r"\b(?:would|could|might|may|should)\b",
    "hypothesis / hypothesize": r"\b[Hh]ypothes\w*",
    "perhaps / probably / possibly / likely": r"\b[Pp]erhaps\b|\b[Pp]robabl\w+|\b[Pp]ossibl\w+|\b[Ll]ikel(?:y|ihood)\b|\b[Mm]aybe\b|\bseemingly\b",
    "about / around / approximately": r"\b(?:about|around|roughly|approximately|nearly|almost|some) (?=[\d$€£])|\b[Aa]pproximately\b|\b[Rr]oughly\b",
    "seems / appears": r"\b[Ss]eem\w*|\b[Aa]ppear\w*",
    "estimate": r"\b[Ee]stimat\w*",
}

STOP_IT = set("""che con per una uno dei del della delle degli dello nel nella nelle negli sono come più anche dopo
prima poi tra fra questo questa questi queste quella quello quelli loro dove quando mentre perché però cosa
essere stato stata hanno aveva erano fosse molto tutti tutte ogni altri altre altro altra ancora quale quali
solo ormai verso senza sotto sopra oltre stesso stessa proprio propria propri proprie""".split())

STOP_EN = set("""about above after again against also another because been before being between both could did does
doing down during each from further have having here hers herself himself into itself just more most myself once only other
ought ours ourselves over same shall should some such than that their theirs them themselves then there these they this those
through under until very was were what when where which while who whom whose will with would your yours yourself yourselves
among around however though although since whether within without often many much even still""".split())

ABBREVIAZIONI_EN_SEMPRE = (r"(?:\b(?:Mr|Mrs|Ms|Dr|Prof|Sr|Jr|St|vs|Fig|Eq|cf|Gen|Col|Lt|Sgt|Capt|Gov|Sen|Rep|Rev|Hon|Mt|Ft|Messrs)\.|"
                           r"\b[A-Z]\.|\b(?:[A-Za-z]\.){2,})$")


def frasi_it(p):
    pezzi = re.split(r"(?<=[.!?])\s+(?=[*_]{0,2}[A-ZÀ-Ù«\"“])", p)
    unite = []
    for s in pezzi:
        if unite and re.search(r"\s[A-Z]\.$", unite[-1]):
            unite[-1] += " " + s
        else:
            unite.append(s)
    return unite


def frasi_en(p):
    pezzi = re.split(r"(?:(?<=[.!?])|(?<=[.!?][\"”’)]))\s+(?=[*_]{0,2}[\"“‘(]?[A-Z])", p)
    unite = []
    for s in pezzi:
        if unite and re.search(ABBREVIAZIONI_EN_SEMPRE, unite[-1]):
            unite[-1] += " " + s
        else:
            unite.append(s)
    return unite


# ---- tic italiani

TIC_IT = [
    ("trattino lungo, medio o spaziato", r"—|–| - "),
    ("errore ortografico", r"\bqual'è\b|\bun pò\b|\bperchè\b|\bnè\b|\bun'altro\b|\bpoichè\b|\bafinchè\b"),
    ("virgolette inglesi", r"\"[^\"\n]{2,}\"|“[^”\n]{2,}”"),
    ("apertura o chiusura formulaica", r"nel mondo di oggi|nel panorama|nell'era (?:digitale|di)|oggi più che mai|in conclusione|in definitiva|per tirare le somme|spero che"),
    ("annuncio di rilevanza", r"è importante (?:sottolineare|notare|ricordare)|vale la pena|degno di nota|giova ricordare|non si può non"),
    ("meta-annuncio", r"come abbiamo visto|andiamo a vedere|vediamo insieme|scopriamo insieme|entriamo nel merito|ora proviamo"),
    ("domanda al lettore", r"ti sei mai chiesto|hai mai pensato|ti starai chiedendo"),
    ("perifrasi della copula", r"\bsi configura come\b|\briveste (?:un|il) ruolo\b|\bgioca un ruolo\b|\bsvolge un ruolo\b|\bsi erge\b|\bfunge da\b"),
    ("«non solo X ma anche Y»", r"\bnon solo\b[^.?!]{0,100}\bma anche\b"),
    ("contrasto «non X, è/ma Y» da valutare", r"\bnon (?:è|sono|si tratta di|significa)\b[^.?!;]{0,80}[,;:]\s*(?:ma|bensì|è|sono|si tratta)\b"),
    ("negazione seguita da due punti, da valutare", r"\bnon\b[^.?!;:]{3,80}:\s"),
    ("lessico da brochure", r"\bsinergi\w*|\bolistic\w*|\bproattiv\w*|\bpanorama\b|\bnavigare\b|\bsfaccettat\w*|\bpoliedric\w*"
                            r"|\bincastonat[oaie]\b|\bnel cuore (?:di|del|della|dello|dell['’])|\bmozzafiato\b|\bdi livello mondiale\b|\bdi fama internazionale\b"
                            r"|\bric(?:co|ca|chi|che) (?:patrimonio|di storia|tradizione|offerta)\b|\bbellezze naturali\b|\bsenza pari\b|\bgemma nascosta\b"
                            r"|\bimperdibil\w+|\bvasta gamma\b|\bbussola\b|\bviaggio alla scoperta\b|\bmosaico di\b"),
    ("giudizio generico", r"\b(?:molto interessante|affascinante|straordinari[oa]|fondamentale|cruciale)\b"),
    ("negazione difensiva, da valutare", r"\banziché\b|\bnon tanto\b[^.?!]{0,80}\bquanto\b|\blungi dall['’]essere\b|\bpiuttosto che\b"),
    ("lessico da traduzione o da burocrazia", r"\bimplementa\w*|\bimplementazion\w*|\bimpattar\w*|\bimpatto su\b|\babilitar\w*|\bal fine di\b|\bin termini di\b|\ba livello di\b|\butilizz\w+|\beffettu\w+"),
    ("iperbole", r"\bimprescindibil\w+|\brivoluzionari\w+|\ba 360 gradi\b|\bver[oa] e propri[oa]\b|\bsvolge un ruolo (?:chiave|centrale)\b"),
    ("enfasi sul significato o sull'eredità", r"\bpunto di svolta\b|\b(?:è|rappresenta|costituisce) (?:una|la) testimonianza\b|\bsi inserisce in (?:un|una) (?:più )?(?:ampio|ampia|vasto|vasta)\b"
                                              r"|\bpiù ampi[oa] (?:contesto|quadro|tendenza)\b|\b(?:eredità|lascito) (?:duratur[oa]|indelebile)\b|\bsegno indelebile\b"
                                              r"|\bprofondamente radicat[oa]\b|\bpone le basi per\b|\bha aperto (?:la strada|un nuovo capitolo)\b|\bha acceso il dibattito\b"
                                              r"|\bun momento (?:cruciale|chiave)\b|\bspartiacque\b|\bsegna(?:ndo)? una svolta\b"),
    ("notorietà e copertura mediatica, da valutare", r"\bcopertura mediatica\b|\bfonti indipendenti\b|\bnumerose testate\b|\bpubblicazioni di settore\b"
                                                     r"|\bpresenza attiva sui social\b|\besperto di fama (?:internazionale|mondiale)\b"),
    ("attribuzione vaga (nominare la fonte o togliere)", r"\b(?:esperti|studiosi|analisti|osservatori|critici|ricercatori|storici|commentatori) "
                                                         r"(?:concordano|sostengono|affermano|ritengono|sottolineano|notano|dicono|evidenziano)\b"
                                                         r"|\bsecondo (?:molti|diversi|numerosi|alcuni) (?:esperti|studiosi|analisti|osservatori|critici)\b"
                                                         r"|\b(?:numerosi|diversi|vari) studi (?:dimostrano|mostrano|indicano|suggeriscono|hanno dimostrato)\b"
                                                         r"|\bgli studi (?:dimostrano|mostrano|indicano|suggeriscono)\b|\bda più parti\b|\bsecondo alcune fonti\b"
                                                         r"|\bampiamente (?:considerat[oaie]|riconosciut[oaie]|ritenut[oaie])\b|\brapporti di settore\b"),
    ("formula delle sfide e delle prospettive", r"\bnonostante (?:le|i|gli|queste|questi|tali) (?:\w+ )?(?:sfide|difficoltà|ostacoli|criticità|limiti)\b"
                                                r"|\bdeve affrontare (?:diverse|numerose|molte|alcune) (?:sfide|criticità|difficoltà)\b|\bcontinua a (?:prosperare|ispirare)\b"
                                                r"|\bprospettive future\b|\bfuturo (?:luminoso|promettente|radioso)\b"),
    ("definizione «si riferisce a» e simili, da valutare", r"\bsi riferisce a\b|\bè (?:una|un) (?:completa|esaustiva|curata) (?:raccolta|panoramica|guida|lista)\b"),
    ("associazione vaga, da valutare (se la relazione è nota, nominarla)", r"\bassociat[oaie] (?:a|con)\b|\bin connessione con\b"),
    ("avvertenza didattica", r"\b(?:potrebbe|può) variare\b|\bi risultati possono variare\b|\btieni presente\b|\btenere presente che\b|\bè bene ricordare\b"
                             r"|\b(?:in base a|dipende da) (?:diversi|vari|numerosi|molti) fattori\b"),
    ("residuo della chat", r"\bcertamente!|\bottima domanda\b|\bfammi sapere\b|\bvuoi che (?:ti|io)\b|\becco (?:una|un|a te) (?:versione|riassunto|sintesi|panoramica|elenco|bozza)\b"
                           r"|\bin questa sezione (?:vedremo|esamineremo|analizzeremo)\b|\bcome (?:modello linguistico|intelligenza artificiale)\b|\bnon esitare a\b"
                           r"|\bsentiti libero\b|\bbuona lettura\b"),
    ("disclaimer sul sapere o congetture sulle lacune", r"\b(?:al|fino al) mio ultimo aggiornamento\b|\bnon (?:è|sono) ampiamente (?:documentat[oaie]|not[oaie]|disponibil[ei])\b"
                                                        r"|\bsulla base delle informazioni disponibili\b|\binformazioni (?:dettagliate )?(?:limitate|scarse)\b"
                                                        r"|\bmantiene un profilo basso\b|\bnon sono disponibili informazioni dettagliate\b|\bfonti pubblicamente disponibili\b"),
    ("segnaposto", r"\[(?:il tuo|tuo|inserisci|inserire|aggiungi|descrivi|nome|cognome|azienda|data|url|titolo)\b[^\]\n]{0,40}\](?![(\[])|\bINSERT_[A-Z_]+\b|\b\d{4}-XX-XX\b|\blorem ipsum\b"),
    ("emoji come formattazione", "[\U0001F300-\U0001FAFF☀-➿⭐⬆✅❌]"),
    ("elenco con etichetta in grassetto (da valutare: se le etichette sono dati, restano)",
     r"^\s*(?:[*\-]|\d+[.)])\s+\*\*[^*\n]{1,60}\*\*:|^\s*(?:[*\-]|\d+[.)])\s+\*\*[^*\n]{1,60}:\*\*"),
    ("connettivo o enfasi di moda, da valutare", r"\bdetto (?:questo|ciò),|\bin altre parole,|\ba ben vedere\b|\ba conti fatti\b|\bin fin dei conti\b|\bin sintesi,"
                                                 r"|\bil punto è\b|\bla verità è (?:che|semplice)\b|\bnon è un caso che\b|\bad oggi\b|\bin un contesto di\b|\bin questo scenario\b"
                                                 r"|\bla chiave (?:è|sta)\b|\bil vero (?:problema|punto|nodo)\b|\bin un mondo in cui\b"),
    ("analogia annunciata, da valutare", r"\bpensa(?:la|lo)? come\b|\bimmagina (?:un|una|di|che)\b|\bpensa a (?:un|una)\b"),
    ("ventaglio o coppia simmetrica, da valutare", r"\bda un lato\b[^.?!]{0,150}\bdall['’]altro\b|\bche si tratti di\b|\bun mix di\b|\buna combinazione di\b|\bdal\w* [^,.;]{2,30} al\w* e tutto ciò che sta nel mezzo\b"),
    ("frammenti a effetto o rivelazione annunciata", r"\b(?:niente|nessun[oa]?) \w+(?: \w+)?[.,] (?:niente|nessun[oa]?) \w+(?: \w+)?[.,] (?:solo|soltanto|e basta)\b"
                                                    r"|(?:^|[.!?]\s+)(?:il risultato|il problema|la soluzione|la verità|la risposta|il trucco)[?:]"),
]
# Famiglie le cui segnalazioni, se vicine, sono la firma di un testo da LLM (vedi grappoli).
GRAPPOLO_IT = {
    "apertura o chiusura formulaica", "annuncio di rilevanza", "meta-annuncio", "perifrasi della copula", "lessico da brochure",
    "giudizio generico", "iperbole", "enfasi sul significato o sull'eredità", "attribuzione vaga (nominare la fonte o togliere)",
    "formula delle sfide e delle prospettive", "avvertenza didattica",
}
CONNETTIVI_IT =r"\b(?:inoltre|tuttavia|pertanto|infatti|dunque|altresì|ciononostante)\b"

# ---- tic inglesi (americano)

BRITANNICO = (
    r"\b(?:organi[sz]|real[iy]s|recogni[sz]|apologi[sz]|civili[sz]|critici[sz]|emphasi[sz]|minimi[sz]|maximi[sz]|"
    r"prioriti[sz]|summari[sz]|standardi[sz]|utili[sz]|categori[sz]|characteri[sz]|finali[sz]|moderni[sz]|"
    r"normali[sz]|optimi[sz]|specialis|sympathi[sz]|authori[sz]|capitali[sz]|customi[sz]|digiti[sz]|"
    r"globali[sz]|legali[sz]|memori[sz]|mobili[sz]|neutrali[sz]|stabili[sz])(?:e|es|ed|ing|ation|ations)\b"
    r"|\banalys(?:e|es|ed|ing)\b|\b(?:colour|favour|honour|labour|behaviour|neighbour|rumour|harbour|flavour|humour)\w*"
    r"|\b(?:centre|metre|litre|theatre|fibre|calibre|sombre)s?\b|\bprogramme\b|\b(?:defence|offence|licence|pretence)\b"
    r"|\bjudgement\b|\b(?:travell|labell|modell|cancell|fuell|signall|channell|counsell)(?:ed|ing|er|ers)\b"
    r"|\b(?:towards|whilst|amongst|learnt|spelt|burnt|dreamt|fulfil|enrol|grey|cheque|aluminium|sceptic\w*|tyre|kerb|mum|catalogue|dialogue|analogue)\b"
)
DATA_NON_US = (r"\b\d{1,2}(?:st|nd|rd|th)?\s+(?:of\s+)?(?:January|February|March|April|May|June|July|August|September|October|November|December)"
               r"(?:,)?\s+\d{4}\b")
CALCHI_IT_EN = (
    r"\bactual\b|\beventual(?:ly)?\b|\bsensible\b|\bactually\b|\bassist(?:ed|s|ing)? (?:to|at)\b|\bpretend(?:s|ed|ing)? to\b"
    r"|\b(?:to|will|would|can|may) evidence\b|\bconjunctures?\b|\bpreoccupations?\b|\bformations? (?:of|for) (?:staff|personnel|engineers|teachers)\b"
    r"|\binformations\b|\badvices\b|\bknowledges\b|\bfeedbacks\b|\bequipments\b|\bresearches\b|\bthe people is\b|\bthe police is\b"
    r"|\bdepends? from\b|\bparticipat\w+ to\b|\bdiscuss\w* about\b|\bsince (?:two|three|four|five|six|seven|eight|nine|ten|\d+) years\b"
    r"|\bin the (?:nineties|eighties|seventies|sixties|fifties)\b|\bfrom (?:the )?one side\b|\bas it is known\b|\bin agreement of\b"
    r"|\bin fact\b|\bin relation to\b|\bwith reference to\b|\bas regards\b|\bthe latter\b|\b(?:the )?same\b (?=(?:is|are|was|were|has|have)\b)"
    r"|\b(?:enters?|entered|entering) (?:in )?an? (?:new )?phase of\b|\b(?:establish|affirm)(?:es|ed)? itself as\b"
    r"|\bmake(?:s)? part of\b|\bconsist(?:s)? in\b|\btake(?:s)? (?:place|part) to\b"
)
TIC_EN = [
    ("trattino spaziato, doppio o en dash usato come pausa", r" - |--| – "),
    ("virgolette caporali", r"[«»]"),
    ("punto o virgola fuori dalle virgolette (uso britannico)", r"\w[”\"][.,]"),
    ("ortografia britannica", BRITANNICO),
    ("data in formato non americano", DATA_NON_US),
    ("apertura o chiusura formulaica", r"in today(?:'s|’s) (?:fast-paced|digital|ever[- ]\w+|modern|rapidly)|in an? (?:ever|increasingly)[- ]\w+ (?:world|landscape|age|era)"
                                         r"|in the (?:ever[- ]\w+ )?(?:world|landscape|realm|age|era) of|in the realm of|when it comes to|at its core|at the end of the day"
                                         r"|\bin conclusion\b|\bin summary\b|\bto sum up\b|\bto conclude\b|\ball in all\b|\bultimately,|\boverall,|first and foremost|let(?:'s|’s) dive"),
    ("annuncio di rilevanza", r"it(?:'s|’s| is) (?:worth|important to) (?:noting|note|mention|emphasi[sz]e|remember|stress)|it(?:'s|’s| is) worth|\bnotably,|\bimportantly,"
                              r"|it should be noted|needless to say|it goes without saying|it bears (?:mentioning|repeating)"),
    ("meta-annuncio", r"let(?:'s|’s) (?:explore|unpack|take a look|break (?:this|it) down|delve)|here(?:'s|’s) (?:the thing|the key|what|why)|as we(?:'ve| have) seen|as mentioned (?:above|earlier)|without further ado|buckle up"),
    ("domanda retorica con risposta", r"\?\s+(?:The answer|It(?:'s|’s| is)|Simple|Because|Well|Simply)\b"),
    ("perifrasi della copula", r"\b(?:serves|stands|acts|functions) as\b|\bboasts\b|\bplays an? (?:crucial|key|pivotal|vital|important|significant|central|critical) role\b|\ba testament to\b|\bstands as a\b"),
    ("«not X, it's Y» / «not just X but Y»", r"\bnot (?:just|only|merely|simply)\b[^.?!]{0,120}\bbut\b"
                                         r"|(?:\b(?:is|are|was|were)(?:n['’]t| not)|\b(?:it|this|that)['’]s not)\s+(?:just |only |merely |simply )?(?:about )?[^.?!;]{2,70}"
                                         r"[,;:—–]\s*(?:it|this|that|they|but|rather)\b"
                                         r"|\b(?:(?:it|this|that)(?:['’]s not| is not| isn['’]t| was not| wasn['’]t)|(?:they|these|those)(?: are not| aren['’]t| were not| weren['’]t))"
                                         r"\s+(?:just |only |merely |simply )?(?:about )?[^.?!;]{2,70}\.\s+(?:it|this|that|they)(?:['’]s|['’]re|\s+(?:is|are|was|were))\b"
                                         r"|\bmore than just\b|\bfar from (?:being|a|an)\b"),
    ("negazione difensiva «rather than / instead of», da valutare", r"\brather than\b|\binstead of\b|\bas opposed to\b|\bnot so much\b"),
    ("lessico da LLM", r"\bdelv\w+|\btapestry\b|\bpivotal\b|\bunderscor\w+|\bintricate\b|\bmultifaceted\b|\bnuanced\b|\bseamless\w*|\bholistic\w*|\bvibrant\b|\bbustling\b"
                       r"|\brealm\b|\blandscape\b|\bjourney\b|\bnavigat\w+|\bleverag\w+|\bharness\w*|\bfoster\w*|\bunlock\w*|\bempower\w*|\belevat\w+|\bshowcas\w+"
                       r"|\bshed(?:s|ding)? light\b|\bgame-chang\w+|\bcutting-edge\b|\btransformative\b|\bgroundbreaking\b|\bbeacon\b|\bembark\w*|\btreasure trove\b"
                       r"|\bever-(?:evolving|changing)\b|\bfast-paced\b|\bmeticulous\w*|\bcommendable\b|\brobust\b|\bparadigm\b"
                       r"|\bgarner\w*|\binterplay\b|\bbolster\w*|\benhanc\w+|\bintricacies\b|\balign(?:s|ed|ing)? with\b|\bvaluable insights?\b|\bresonat\w+ with\b"),
    ("iperbole o giudizio generico", r"\b(?:crucial|vital|essential|remarkable|unprecedented|truly|genuinely|deeply|fundamentally|incredibly|extremely|absolutely|undeniabl\w+|undoubtedly)\b"),
    ("corporate-speak", r"\bsynerg\w+|\bcircle back\b|\btouch base\b|\bbandwidth\b|\bdeep[- ]dive\b|\blow[- ]hanging fruit\b|\bmove the needle\b|\bgoing forward\b|\bstakeholders?\b"
                        r"|\butili[sz]\w+|\blearnings\b|\btake-?aways?\b|\bparadigm shift\b|\bbest practices?\b|\bvalue[- ]add\w*|\becosystems?\b|\bmission-critical\b"
                        r"|\bscalab\w+|\bactionable\b|\bimpactful\b|\bonboard\w*|\bstreamlin\w+|\bthought leader\w*|\bkey drivers?\b"),
    ("accademichese o burocratese", r"\bin the context of\b|\bwith respect to\b|\bwith regard to\b|\bin terms of\b|\ba plethora of\b|\ba myriad of\b|\bthe extent to which\b"
                                    r"|\baforementioned\b|\bhereinafter\b|\bwhereby\b|\bthereof\b|\bherein\b|\bin order to\b|\bdue to the fact that\b|\ba number of\b"
                                    r"|\bat this point in time\b|\bin the event that\b|\bprior to\b|\bsubsequent to\b"),
    ("giornalese", r"\bslammed\b|\bblasted\b|\bin a bid to\b|\bsparked\b|\bamid\b|\bembattled\b|\bvowed\b|\bwar of words\b|\bfierce debate\b|\bperfect storm\b"
                   r"|\btip of the iceberg\b|\bgrowing chorus\b|\bsources say\b|\braised eyebrows\b|\bhot-button\b|\bspearhead\w*|\bramp(?:ing|ed|s)? up\b"),
    ("participio o gerundio appeso, da valutare", r",\s+(?:highlighting|ensuring|reflecting|underscoring|showcasing|demonstrating|illustrating|emphasizing|signaling|marking|reinforcing|enabling|allowing|making|paving|solidifying)\b"),
    ("possibile calco dall'italiano (falso amico, reggenza, plurale)", CALCHI_IT_EN),
    ("enfasi sul significato o sull'eredità", r"\breflects? (?:the )?broader\b|\bbroader (?:trends?|context|significance|implications)\b|\benduring (?:legacy|impact|significance)\b"
                                              r"|\blasting (?:legacy|impact)\b|\bindelible mark\b|\bdeeply rooted\b|\bsetting the stage for\b|\bturning point\b"
                                              r"|\bmarks? a (?:shift|new chapter)\b|\bmarking a (?:pivotal|significant|key|new)\b|\bevolving landscape\b|\bfocal point\b"
                                              r"|\bhas generated debate\b|\bprompted broader\b|\bcontributing to the (?:broader|wider|ongoing)\b"
                                              r"|\bstands? as a (?:reminder|symbol)\b|\bsymboli[sz]ing its\b"),
    ("notorietà e copertura mediatica, da valutare", r"\bindependent coverage\b|\b(?:national|local|regional) media outlets?\b|\btrade publications?\b"
                                                     r"|\b(?:featured|profiled|cited) in\b|\bactive social media presence\b|\bleading experts?\b"),
    ("linguaggio da brochure", r"\bnestled\b|\bin the heart of\b|\bbreathtaking\b|\bstunning\b|\bworld-class\b|\bstate-of-the-art\b|\brenowned\b"
                               r"|\bdiverse array\b|\brich (?:cultural )?(?:heritage|history)\b|\bnatural beauty\b|\bcommitment to (?:excellence|quality|sustainability)\b"
                               r"|\bunparalleled\b|\bsecond to none\b|\bone-of-a-kind\b|\bhidden gem\b|\bmust-visit\b|\btop-notch\b"),
    ("attribuzione vaga (nominare la fonte o togliere)", r"\b(?:experts|critics|observers|analysts|scholars|historians|commentators|researchers|many people|some people)"
                                                         r" (?:say|argue|note|suggest|believe|agree|have (?:noted|cited|argued|suggested|pointed out))\b"
                                                         r"|\bindustry (?:reports?|observers|experts|insiders)\b|\bstudies (?:show|suggest|indicate|have shown)\b"
                                                         r"|\bresearch (?:shows|suggests|indicates)\b|\bwidely (?:regarded|considered|recognized|acclaimed)\b"
                                                         r"|\bsome critics\b|\bseveral sources\b|\bobservers have\b|\bmany (?:experts|critics|scholars|historians)\b"),
    ("formula delle sfide e delle prospettive", r"\bdespite (?:its|these|the|this)\b[^.?!]{0,80}\b(?:challenges|setbacks|obstacles|limitations|hurdles)\b"
                                                r"|\bfaces (?:several|a number of|numerous|some|many|ongoing) (?:challenges|obstacles|hurdles)\b|\bcontinues to (?:thrive|inspire)\b"
                                                r"|\bfuture (?:outlook|prospects)\b|\bbright future\b"),
    ("definizione «X refers to» e perifrasi di is/has, da valutare", r"\brefers? to\b|\bis a (?:curated|comprehensive) (?:list|compilation|collection|overview)\b"
                                                                    r"|\brepresents (?:a|an|the)\b|\boperates as\b|\bembodies\b|\bconstitutes\b"
                                                                    r"|\b(?:features|offers) (?:a|an|the|over|more than|several|numerous) |\bbegan (?:his|her|their) career as\b|\bventured into\b"),
    ("associazione vaga, da valutare (se la relazione è nota, nominarla)", r"\bassociated with\b|\bin connection with\b"),
    ("avvertenza didattica", r"\bmay vary\b|\bkeep in mind\b|\bdepending on (?:various|several|many|a number of) factors\b|\bresults may differ\b"),
    ("parola ricercata al posto di una semplice, da valutare", r"\bpassed away\b|\bauthored\b|\battempted\b|\brelocated\b|\bcommenc\w+|\bendeavou?r\w*|\bascertain\w*|\bfacilitat\w+"),
    ("residuo della chat", r"\bi hope this helps\b|\bcertainly!|\bgreat question\b|\bof course!|\blet me know if\b|\bwould you like me to\b"
                           r"|\bhere is (?:a|an|the) (?:revised|rewritten|updated|summary|overview)\b|\bin this section,? we(?: will|['’]ll)\b"
                           r"|\bas an ai\b|\bas a language model\b|\bi['’]d be happy to\b|\bfeel free to\b"),
    ("disclaimer sul sapere o congetture sulle lacune", r"\bas of my (?:last|latest|knowledge)\b|\bknowledge cut-?off\b|\bwhile specific details\b"
                                                        r"|\bnot widely (?:documented|disclosed|available|reported|known)\b|\bbased on (?:the )?available information\b"
                                                        r"|\bmaintains a low profile\b|\blimited information (?:is )?available\b|\bdetails are (?:limited|scarce)\b"),
    ("segnaposto", r"\[(?:your|insert|add|describe|company|date|url|title|name)\b[^\]\n]{0,40}\](?![(\[])|\bINSERT_[A-Z_]+\b|\b\d{4}-XX-XX\b|\blorem ipsum\b"),
    ("emoji come formattazione", "[\U0001F300-\U0001FAFF☀-➿⭐⬆✅❌]"),
    ("elenco con etichetta in grassetto (da valutare: se le etichette sono dati, restano)",
     r"^\s*(?:[*\-]|\d+[.)])\s+\*\*[^*\n]{1,60}\*\*:|^\s*(?:[*\-]|\d+[.)])\s+\*\*[^*\n]{1,60}:\*\*"),
    ("connettivo o enfasi di moda, da valutare", r"\bthat said,|\bthat being said\b|\bput simply\b|\bsimply put\b|\bin other words,|\bmore importantly,|\bwhat['’]s more,"
                                                 r"|\bnot only that\b|\bthe bottom line\b|\bthe (?:key )?takeaway\b|\bthe reality is\b|\bthe truth is\b|\bin a nutshell\b"
                                                 r"|\bit['’]s no secret\b|\bone thing is clear\b|\bmake no mistake\b|\bplain and simple\b"),
    ("analogia annunciata, da valutare", r"\bthink of (?:it|this|them|[a-z]+) (?:as|like)\b|\bimagine (?:a|an|if|that|you)\b|\bpicture (?:a|an|this)\b"),
    ("ventaglio o coppia simmetrica, da valutare", r"\branging from\b|\ba blend of\b|\ba mix of\b|\bwhether you['’]re\b|\bon the one hand\b|\bfrom \w+ to \w+ and everything in between\b"
                                                   r"|\bwhether (?:it['’]s|it is|you are)\b[^.?!]{0,80}\bor\b"),
    ("frammenti a effetto o rivelazione annunciata", r"\bno \w+(?: \w+)?[.,] no \w+(?: \w+)?[.,] (?:just|only)\b|\bnot \w+(?: \w+)?\. not \w+(?: \w+)?\. (?:just|only)\b"
                                                    r"|(?:^|[.!?]\s+)(?:the|here['’]s the) (?:result|catch|problem|solution|answer|truth|kicker|upshot|twist)[?:]"),
]
# Famiglie le cui segnalazioni, se vicine, sono la firma di un testo da LLM (vedi grappoli).
GRAPPOLO_EN = {
    "apertura o chiusura formulaica", "annuncio di rilevanza", "meta-annuncio", "perifrasi della copula", "lessico da LLM",
    "iperbole o giudizio generico", "corporate-speak", "participio o gerundio appeso, da valutare",
    "enfasi sul significato o sull'eredità", "linguaggio da brochure", "attribuzione vaga (nominare la fonte o togliere)",
    "formula delle sfide e delle prospettive", "avvertenza didattica",
}
CONNETTIVI_EN =r"\b(?:moreover|furthermore|additionally|in addition|however|therefore|thus|consequently|nevertheless|hence|indeed)\b"

# ---- scorrevolezza italiana

ASTRATTI_IT = re.compile(r"\w{4,}(?:zione|zioni|sione|sioni|mento|menti|ità|ismo)", re.I)
CONCRETI_IT = re.compile(r"^(costellazion|mission|stazion|navigazion|collision|esplosion|introduzion|televis|"
                         r"ispezion|operazion|nazion|settor|element|document|component|monument|strument|"
                         r"argoment|investiment|frammento|fondamento|accordo)", re.I)
PRONOMI_PESANTI_IT = r"\b(?:quest'ultim\w+|\btale\b|\btali\b|suddett\w+|medesim\w+|il quale|la quale|i quali|le quali|del quale|della quale)\b"
DOPPIA_NEGAZIONE_IT = (r"\bnon (?:senza|poco|raramente|inutilmente|irrilevante|insignificante|trascurabile)\b"
                       r"|\bnon\b[^.?!;:,]{0,40}\bsenza\b|\bnon è che non\b|\bnon (?:è|sarebbe) (?:un caso|raro|improbabile)\b")

# ---- scorrevolezza inglese

ASTRATTI_EN = re.compile(r"\w{4,}(?:tion|tions|sion|sions|ment|ments|ity|ities|ism|isms|ance|ances|ence|ences|ness)", re.I)
CONCRETI_EN = re.compile(r"^(question|government|department|document|environment|equipment|instrument|experiment|monument|segment|"
                         r"fragment|settlement|apartment|ornament|pavement|supplement|compartment|testament|station|section|"
                         r"mention|position|condition|addition|edition|collection|connection|competition|production|reference|"
                         r"conference|difference|presence|absence|evidence|science|audience|experience|sentence|silence|"
                         r"university|community|security|facility|authority|majority|minority|city|identity|quality|"
                         r"capacity|opportunity|nationality|ability|activity|property|society|variety|entity)", re.I)
PRONOMI_PESANTI_EN = r"\b(?:the latter|the former|aforementioned|aforesaid|the foregoing|whereby|thereof|herein|hereinafter|respectively)\b"
DOPPIA_NEGAZIONE_EN = (r"\bnot (?:un\w{3,}|without|insignificant|irrelevant|unlikely|infrequent|inconsiderable|negligible)\b"
                       r"|\bnot\b[^.?!;:,]{0,30}\bwithout\b|\bcannot (?:not|fail to)\b|\bno (?:less|fewer) than\b[^.?!]{0,20}\bnot\b"
                       r"|\bnot (?:a )?(?:rare|small|bad|minor|trivial)\b")
IRREGOLARI_EN = ("made|done|shown|seen|known|taken|given|found|built|held|led|put|set|kept|left|brought|thought|bought|sold|told|paid|"
                 "begun|chosen|written|driven|broken|spoken|stolen|worn|torn|born|hidden|forgotten|drawn|grown|thrown|lost|sent|"
                 "spent|met|won|caught|taught|struck|laid|fed|dealt|meant|understood|proven|beaten|ridden|risen|shaken|eaten")
PASSIVO_EN = re.compile(r"\b(?:is|are|was|were|be|been|being|gets?|got|gotten)\s+(?:(?:not|also|often|then|still|already|never|always|now|\w+ly)\s+){0,2}"
                        r"(?:(?:" + IRREGOLARI_EN + r")|\w{3,}ed)\b", re.I)


def etichette_it(s):
    """Elenco di indizi di lettura faticosa in una frase italiana."""
    t = s.lower()
    n = len(s.split())
    virgole = s.count(",")
    out = []
    if n > 45:
        out.append(f"lunga ({n} parole)")
    if n > 30 and virgole >= 4 and ":" not in s and ";" not in s:
        out.append(f"incassata ({virgole} virgole in {n} parole)")
    k_che = len(re.findall(r"\bche\b", t))
    if k_che >= 3:
        out.append(f"{k_che} «che»")
    if re.search(DOPPIA_NEGAZIONE_IT, t):
        out.append("doppia negazione")
    if re.search(PRONOMI_PESANTI_IT, t):
        out.append("pronome o aggettivo burocratico (tale, suddetto, quest'ultimo, il quale)")
    k_di = len(re.findall(r"\b(?:di|del|dello|della|dei|degli|delle|dell')\b", t))
    if k_di >= 5:
        out.append(f"catena di complementi ({k_di} «di»)")
    astratti = [w for w in re.findall(r"[^\W\d_][\w'’]*", s) if ASTRATTI_IT.fullmatch(w) and not CONCRETI_IT.match(w)]
    if len(astratti) >= 3:
        out.append(f"{len(astratti)} nomi astratti ({', '.join(a.lower() for a in astratti[:4])})")
    if re.search(r",\s+\w+(?:ando|endo)\b[^.?!]{0,60}[.?!]?$", t) and n > 20:
        out.append("gerundio di coda")
    if len(re.findall(r"\b(?:viene|vengono|venne|vennero|è stat[oaie]|sono stat[oaie])\b", t)) >= 2:
        out.append("passivi ripetuti")
    return out


def etichette_en(s):
    """Elenco di indizi di lettura faticosa in una frase inglese. Soglie provvisorie."""
    t = s.lower()
    n = len(s.split())
    virgole = s.count(",")
    out = []
    if n > 38:
        out.append(f"lunga ({n} parole)")
    if n > 26 and virgole >= 4 and ":" not in s and ";" not in s:
        out.append(f"incassata ({virgole} virgole in {n} parole)")
    k_che = len(re.findall(r"\b(?:that|which|who|whom|whose)\b", t))
    if k_che >= 4:
        out.append(f"{k_che} «that/which/who»")
    if re.search(DOPPIA_NEGAZIONE_EN, t):
        out.append("doppia negazione")
    if re.search(PRONOMI_PESANTI_EN, t):
        out.append("pronome o aggettivo burocratico (the latter, aforementioned, whereby, thereof)")
    if re.match(r"[\W_]*(?:this|that|these|those)\s+(?:is|was|are|were|has|have|had|will|would|can|could|may|might|means|shows|allows|makes|leads|suggests|reflects|highlights)\b", t):
        out.append("«This/That» come soggetto senza nome (riferimento vago)")
    if re.match(r"[\W_]*(?:it|there)\s+(?:is|are|was|were|seems|appears)\b", t) and n > 12:
        out.append("apertura espletiva (it is / there is)")
    k_of = len(re.findall(r"\bof\b", t))
    if k_of >= 4:
        out.append(f"catena di complementi ({k_of} «of»)")
    astratti = [w for w in re.findall(r"[^\W\d_][\w'’]*", s) if ASTRATTI_EN.fullmatch(w) and not CONCRETI_EN.match(w)]
    if len(astratti) >= 4:
        out.append(f"{len(astratti)} nomi astratti ({', '.join(a.lower() for a in astratti[:4])})")
    if re.search(r",\s+(?!including|according|following|regarding|depending|given)\w+ing\b[^.?!]{0,70}[.?!]?$", t) and n > 18:
        out.append("participio di coda")
    if len(PASSIVO_EN.findall(s)) >= 2:
        out.append("passivi ripetuti")
    if re.search(r"\b(?:may|might|could|can) (?:potentially|possibly|perhaps|somewhat|arguably)\b|\b(?:potentially|possibly|perhaps) (?:may|might|could)\b", t):
        out.append("cautele accumulate")
    return out


PROFILI = {
    "it": {
        "nome": "italiano",
        "note": re.compile(r"^#+\s*Note\s*$", re.IGNORECASE),
        "normalizza_numero": normalizza_numero_it,
        "cautele": CAUTELE_IT,
        "cautele_minuscolo": True,
        "stop": STOP_IT,
        "frasi": frasi_it,
        "inizio_frase": ".!?«“\"",
        "ritmo": {"provvisorio": False, "mediana": (18, 32), "breve": 8, "medio": 20, "lungo": 35, "serie": 45,
                  "dev_piatta": 8, "dev_uniforme": 10},
        "codice": "it",
        "tic": TIC_IT,
        "grappolo": GRAPPOLO_IT,
        "connettivi": CONNETTIVI_IT,
        "etichette": etichette_it,
        "breve_staccato": 8,
    },
    "en": {
        "nome": "inglese americano",
        "note": re.compile(r"^#{1,2}\s*Notes?\s*$", re.IGNORECASE),
        "normalizza_numero": normalizza_numero_en,
        "cautele": CAUTELE_EN,
        "cautele_minuscolo": False,
        "stop": STOP_EN,
        "frasi": frasi_en,
        "inizio_frase": ".!?“\"‘",
        # PROVVISORIE: soglie italiane scalate di circa 0,85 (l'inglese usa meno parole per la stessa cosa).
        "ritmo": {"provvisorio": True, "mediana": (15, 27), "breve": 7, "medio": 17, "lungo": 30, "serie": 38,
                  "dev_piatta": 7, "dev_uniforme": 8.5},
        "codice": "en",
        "tic": TIC_EN,
        "grappolo": GRAPPOLO_EN,
        "connettivi": CONNETTIVI_EN,
        "etichette": etichette_en,
        "breve_staccato": 7,
    },
}

PRF = PROFILI["it"]


def imposta_lingua(codice):
    global PRF
    PRF = PROFILI[codice]


AVVISO_PROVVISORIO = ("ATTENZIONE: le soglie per l'inglese sono provvisorie (derivate da quelle italiane, "
                      "non calibrate su campioni inglesi). Leggile come ordini di grandezza.")


def leggi_righe(percorso, ignora_id=False, intervallo=None):
    """Righe di testo senza la sezione Note, senza linee orizzontali e senza esponenti.

    Con intervallo=(da, a) si leggono solo le righe da..a del file (1-based, estremi inclusi)."""
    righe = []
    with open(percorso, encoding="utf-8") as f:
        tutte = f.read().splitlines()
        if intervallo:
            tutte = tutte[intervallo[0] - 1:intervallo[1]]
        for riga in tutte:
            if PRF["note"].match(riga.strip()):
                break
            if riga.strip() == "---":
                continue
            riga = re.sub(r"[¹²³⁴⁵⁶⁷⁸⁹⁰]+", "", riga)
            riga = re.sub(r"<!--.*?-->", "", riga)  # i commenti HTML non sono prosa (li controlla «struttura»)
            if ignora_id:
                if riga.startswith("Tipi:"):
                    continue
                riga = riga.replace("**", "")
                riga = re.sub(r"\b[A-F]\d+[a-z]?\b", "", riga)
                riga = re.sub(r"\((?:F|S|I|T)\)", "", riga)
            righe.append(riga)
    return righe


def testo_di(righe):
    return "\n".join(righe)


# ---------------------------------------------------------------- integrità

def numeri(righe):
    trovati = set()
    for r in righe:
        r = re.sub(r"^\s*\d+[.)]\s+", "", r)
        for m in RE_NUM.findall(r):
            trovati.add(PRF["normalizza_numero"](m))
    return trovati


def nomi(righe):
    """Parole con iniziale maiuscola che non aprono una frase (nomi propri, sigle)."""
    trovati = set()
    for r in righe:
        r = re.sub(r"^[\s#>*\-]+", "", r)
        r = re.sub(r"^\d+[.)]\s+", "", r)
        for m in RE_PAROLA.finditer(r):
            parti = re.split(r"[’']", m.group(0))
            prima = r[:m.start()].rstrip()
            inizio_frase = (not prima) or prima[-1] in PRF["inizio_frase"]
            if re.search(r"(?:^|\s)[A-ZÀ-Ý]\.$", prima):  # iniziale di un nome, non fine frase
                inizio_frase = False
            for i, p in enumerate(parti):
                p = p.strip("-")
                if len(p) < 2 or not p[0].isupper():
                    continue
                if i == 0 and inizio_frase:
                    continue
                trovati.add(p)
    return trovati


def conta_cautele(testo):
    t = testo.lower() if PRF["cautele_minuscolo"] else testo
    return {k: len(re.findall(rx, t)) for k, rx in PRF["cautele"].items()}


def radici(testo):
    """Prime cinque lettere delle parole significative: tollera flessioni e cambi di forma."""
    return {w[:5] for w in re.findall(r"[^\W\d_]{5,}", testo.lower()) if w not in PRF["stop"]}


def copertura(righe_origine, righe_risultato):
    """Frasi dell'origine non ritrovate nel risultato.

    Ogni frase dell'origine viene cercata in una finestra di 1-3 frasi consecutive del risultato:
    la copertura è la quota delle sue parole significative che vi compaiono. Sotto il 70% si segnala."""
    frasi_r = [s for p in paragrafi(righe_risultato) for s in PRF["frasi"](p)]
    radici_r = [radici(s) for s in frasi_r]
    mancanti = []
    for i, p in enumerate(paragrafi(righe_origine), 1):
        for s in PRF["frasi"](p):
            r = radici(s)
            if len(r) < 4:
                continue
            migliore, miglior_assenti = 0.0, sorted(r)
            for a in range(len(radici_r)):
                finestra = set()
                for b in range(a, min(a + 3, len(radici_r))):
                    finestra |= radici_r[b]
                    q = len(r & finestra) / len(r)
                    if q > migliore:
                        migliore, miglior_assenti = q, sorted(r - finestra)
            if migliore < 0.7:
                mancanti.append((i, s, miglior_assenti))
    return mancanti


def cmd_integrita(args):
    consenti = "--consenti-aggiunte" in args
    ignora = "--ignora-id" in args
    intervallo = None
    if "--righe" in args:
        i = args.index("--righe")
        m = re.fullmatch(r"(\d+)-(\d+)", args[i + 1]) if i + 1 < len(args) else None
        if not m or int(m.group(1)) < 1 or int(m.group(2)) < int(m.group(1)):
            return uso()
        intervallo = (int(m.group(1)), int(m.group(2)))
        args = args[:i] + args[i + 2:]
    file_ = [a for a in args if not a.startswith("--")]
    if len(file_) != 2:
        return uso()
    o, r = leggi_righe(file_[0], ignora, intervallo), leggi_righe(file_[1], ignora)
    bloccante = False

    no, nr = numeri(o), numeri(r)
    nuovi_n, persi_n = sorted(nr - no), sorted(no - nr)
    mo, mr = nomi(o), nomi(r)
    testo_o, testo_r = testo_di(o), testo_di(r)
    # un nome che l'altro testo ha solo a inizio frase (dove il programma non lo vede) non è né nuovo né perso
    nuovi_m = sorted(m for m in mr - mo if not re.search(r"\b" + re.escape(m) + r"\b", testo_o))
    persi_m = sorted(m for m in mo - mr if not re.search(r"\b" + re.escape(m) + r"\b", testo_r))

    print(f"Origine:   {file_[0]}" + (f" (solo righe {intervallo[0]}-{intervallo[1]})" if intervallo else ""))
    print(f"Risultato: {file_[1]}")
    print()
    if nuovi_n:
        tag = "AVVISO" if consenti else "ERRORE"
        print(f"{tag} numeri nel risultato e non nell'origine: {', '.join(nuovi_n)}")
        bloccante = bloccante or not consenti
    if nuovi_m:
        tag = "AVVISO" if consenti else "ERRORE"
        print(f"{tag} nomi o sigle nel risultato e non nell'origine: {', '.join(nuovi_m)}")
        bloccante = bloccante or not consenti
    if persi_n:
        print(f"AVVISO numeri dell'origine assenti nel risultato (il taglio è dichiarato nel rapporto?): {', '.join(persi_n)}")
    if persi_m:
        print(f"AVVISO nomi o sigle dell'origine assenti nel risultato (il taglio è dichiarato nel rapporto?): {', '.join(persi_m)}")

    co, cr = conta_cautele(testo_di(o)), conta_cautele(testo_di(r))
    for k in PRF["cautele"]:
        if cr[k] < co[k]:
            print(f"AVVISO cautela forse persa, «{k}»: {co[k]} nell'origine, {cr[k]} nel risultato")
        elif cr[k] > co[k]:
            print(f"AVVISO cautela forse aggiunta, «{k}»: {co[k]} nell'origine, {cr[k]} nel risultato")

    cop = copertura(o, r)
    if cop:
        print(f"\nAVVISO possibili omissioni: {len(cop)} frasi dell'origine con meno del 70% delle parole significative nel risultato")
        for i, s, m in cop[:20]:
            print(f"   p{i:02d} mancano: {', '.join(m[:8])}")
            print(f"        {s[:170]}{'…' if len(s) > 170 else ''}")
        print("   Una frase spezzata o riformulata può comparire qui: si controlla che niente di ciò che diceva sia andato perso.")

    pw_o, pw_r = len(testo_di(o).split()), len(testo_di(r).split())
    print(f"\nParole: origine {pw_o}, risultato {pw_r} ({100 * (pw_r - pw_o) / max(pw_o, 1):+.0f}%)")
    print("Limiti: i numeri scritti in lettere e i nomi a inizio frase non sono visti.")
    if not (nuovi_n or nuovi_m or persi_n or persi_m):
        print("Numeri e nomi coincidono.")
    return 1 if bloccante else 0


# -------------------------------------------------------------------- ritmo

def paragrafi(righe, con_lista=False):
    out = []
    for r in righe:
        t = r.strip()
        if not t or t.startswith("#"):
            continue
        era_lista = bool(re.match(r"(?:[*\-]\s+|\d+[.)]\s+)", t))
        t = re.sub(r"^(?:[*\-]\s+|\d+[.)]\s+|>\s*)", "", t)
        # etichetta in grassetto che chiude con punto o due punti: non è una frase
        t = re.sub(r"^\*\*[^*]{1,80}[.:]\*\*\s*", "", t)
        if t:
            out.append((t, era_lista) if con_lista else t)
    return out


SOGLIA_BREVI = {"regolare": 15, "cerniere": 25, "tecnico": 10}


def cmd_ritmo(args):
    registro = "regolare"
    if "--registro" in args:
        i = args.index("--registro")
        registro = args[i + 1] if i + 1 < len(args) else ""
        args = args[:i] + args[i + 2:]
    if not args or registro not in SOGLIA_BREVI:
        return uso()
    R = PRF["ritmo"]
    frasi = PRF["frasi"]
    if R["provvisorio"]:
        print(f"(lingua: {PRF['nome']})")
        print(AVVISO_PROVVISORIO)
    print(f"(registro: {registro}; soglia frasi brevi {SOGLIA_BREVI[registro]}%)\n")
    b, m, l = R["breve"], R["medio"], R["lungo"]
    for indice, percorso in enumerate(args):
        if indice:
            print()
        con_tipo = paragrafi(leggi_righe(percorso), True)
        pars = [p for p, _ in con_tipo]
        seqs = [[len(s.split()) for s in frasi(p)] for p in pars]
        L = [x for s in seqs for x in s]
        n = len(L)
        parole = sum(L)
        brevi = sum(1 for x in L if x <= b)
        pct = lambda f: 100 * sum(1 for x in L if f(x)) / n
        run = best = 0
        for x in L:
            run = run + 1 if x > R["serie"] else 0
            best = max(best, run)
        print(f"== {percorso}")
        print(f"   {len(pars)} paragrafi, {n} frasi, {parole} parole")
        print(f"   media {st.mean(L):.1f}  mediana {st.median(L):.0f}  dev.std {st.pstdev(L):.1f}  min {min(L)}  max {max(L)}")
        print(f"   fino a {b}: {pct(lambda x: x <= b):.0f}%   {b + 1}-{m}: {pct(lambda x: b + 1 <= x <= m):.0f}%   "
              f"{m + 1}-{l}: {pct(lambda x: m + 1 <= x <= l):.0f}%   oltre {l}: {pct(lambda x: x > l):.0f}%")
        print(f"   frasi per paragrafo {n / len(pars):.1f}   parole per paragrafo {parole / len(pars):.0f}")
        print(f"   una frase breve (fino a {b}) ogni {parole / max(brevi, 1):.0f} parole")
        avvisi = []
        lo, hi = R["mediana"]
        if not lo <= st.median(L) <= hi:
            avvisi.append(f"mediana {st.median(L):.0f} fuori dall'intervallo indicativo {lo}-{hi}")
        if st.pstdev(L) < R["dev_piatta"]:
            avvisi.append(f"deviazione standard {st.pstdev(L):.1f}: ritmo piatto")
        elif st.pstdev(L) < R["dev_uniforme"]:
            avvisi.append(f"deviazione standard {st.pstdev(L):.1f}: ritmo tendente all'uniforme")
        if pct(lambda x: x <= b) > SOGLIA_BREVI[registro]:
            avvisi.append(f"frasi brevi al {pct(lambda x: x <= b):.0f}%: sono cerniere o effetto?")
        if best > 2:
            avvisi.append(f"{best} frasi consecutive oltre {R['serie']} parole")
        # i paragrafi con etichetta e le voci di elenco sono costruzioni in parallelo, non ripetizioni
        attacchi = Counter(" ".join(p.split()[:2]).lower() for p, lista in con_tipo
                           if not lista and not p.startswith("**"))
        for a, k in attacchi.items():
            if k >= 3:
                avvisi.append(f"{k} paragrafi aprono con «{a}»")
        for a in avvisi:
            print(f"   AVVISO {a}")
        if not avvisi:
            print("   nessun avviso")
    return 0


# ---------------------------------------------------------------------- tic

def grappoli(righe):
    """Capoversi con tre o più indizi delle famiglie tipiche dei LLM.

    Un indizio isolato (una parola come «crucial») è normale; più indizi vicini sono la firma."""
    out = []
    for i, p in enumerate(paragrafi(righe), 1):
        k = sum(len(re.findall(rx, p, re.IGNORECASE)) for nome, rx in PRF["tic"] if nome in PRF["grappolo"])
        if k >= 3:
            out.append(f"grappolo: il capoverso {i} ha {k} indizi di famiglie tipiche dei LLM (un indizio isolato è normale, più indizi vicini sono una firma)")
    return out


PAROLE_FUNZIONE = {
    "en": set("""about after against among and around before between but during from into like near once onto over per than that the their these this
those through under until upon what when where which while whom whose with within without your""".split()),
    "it": set("""alla alle allo agli anche come con dalla dalle dallo dagli dell della delle dello degli nella nelle nello negli sulla sulle sullo sugli
dopo prima senza sotto sopra verso tra fra per che non più ogni quale quali questo questa questi queste loro essere""".split()),
}


def forma_titolo(testo):
    """'titolo' se i titoli hanno le iniziali maiuscole sulle parole piene, 'frase' se solo la prima, None se non si può dire."""
    t = re.sub(r"[*_`]", "", testo)
    parole = re.findall(r"[^\W\d_][\w'’\-]*", t)
    piene = [w for w in parole[1:] if len(w) >= 4 and w.lower() not in PAROLE_FUNZIONE[PRF["codice"]]]
    if len(piene) < 2:
        return None
    maiuscole = sum(1 for w in piene if w[0].isupper()) / len(piene)
    return "titolo" if maiuscole >= 0.75 else "frase" if maiuscole <= 0.25 else None


def titoli_incoerenti(righe):
    """Inglese: titoli dello stesso livello con convenzioni diverse (Title Case e prima maiuscola).
    Italiano: titoli in Title Case all'inglese, da valutare (i nomi propri sono normali)."""
    per_livello = {}
    for r in righe:
        m = re.match(r"^(#{1,6})\s+(.*?)\s*#*\s*$", r)
        if m:
            f = forma_titolo(m.group(2))
            if f:
                per_livello.setdefault(len(m.group(1)), []).append((f, m.group(2)))
    out = []
    for livello, voci in sorted(per_livello.items()):
        if PRF["codice"] == "en":
            t, s = [v for f, v in voci if f == "titolo"], [v for f, v in voci if f == "frase"]
            if t and s:
                out.append(f"titoli di livello {livello} incoerenti: {len(t)} in Title Case (es. «{t[0][:50]}») e {len(s)} con la sola prima maiuscola "
                           f"(es. «{s[0][:50]}»). Si sceglie una convenzione per livello (`convenzioni-us.md`).")
        else:
            t = [v for f, v in voci if f == "titolo"]
            if t:
                out.append(f"titoli di livello {livello} in Title Case all'inglese ({len(t)}, es. «{t[0][:50]}»), da valutare: in italiano l'iniziale maiuscola è solo la prima parola e i nomi propri.")
    return out


def tipografia_mista(righe, doppie):
    """Apostrofi dritti e ricurvi nello stesso testo (e, in inglese, virgolette doppie dritte e ricurve)."""
    t = "\n".join(righe)
    t = re.sub(r"```.*?```", "", t, flags=re.S)
    t = re.sub(r"`[^`\n]*`", "", t)
    t = re.sub(r"<[^>\n]+>", "", t)
    t = re.sub(r"\]\([^)\n]*\)", "]", t)
    t = re.sub(r"https?://\S+", "", t)
    out = []
    d, c = len(re.findall(r"(?<=\w)'(?=\w)", t)), len(re.findall(r"(?<=\w)’(?=\w)", t))
    if d and c:
        out.append(f"apostrofi misti: {d} dritti e {c} ricurvi nello stesso testo; si segue il documento e si resta coerenti.")
    if doppie:
        d, c = t.count('"'), t.count("“") + t.count("”")
        if d and c:
            out.append(f"virgolette doppie miste: {d} dritte e {c} ricurve nello stesso testo; si segue il documento e si resta coerenti.")
    return out


def punteggiatura_di_pausa(righe):
    """Densità di due punti, punto e virgola e parentesi.

    Chi non può usare il trattino lungo tende a sostituirlo con questi segni: la sostituzione è lo stesso tic.
    Soglie PROVVISORIE (nessun campione di autori reali misurato) e un testo breve non si misura."""
    pars = paragrafi(righe)
    parole = sum(len(p.split()) for p in pars)
    if parole < 150:
        return []

    def pulito(p):
        p = re.sub(r"https?://\S+", "", p)
        p = re.sub(r"\]\([^)\n]*\)", "]", p)
        p = re.sub(r"&\w+;", "", p)
        return p

    segni = (
        ("due punti", r":(?=\s)", 8, 5),
        ("punto e virgola", r";", 6, 4),
        ("parentesi", r"\(", 10, 6),
    )
    out = []
    for nome, rx, per_mille, minimo in segni:
        per_par = [len(re.findall(rx, pulito(p))) for p in pars]
        k = sum(per_par)
        dens = 1000 * k / parole
        if k >= minimo and dens >= per_mille:
            piu = sorted(range(len(pars)), key=lambda i: -per_par[i])[:3]
            dove = ", ".join(f"{i + 1} ({per_par[i]})" for i in piu if per_par[i] > 1)
            out.append(f"{nome}: {k} in {parole} parole ({dens:.1f} ogni mille, soglie provvisorie)"
                       + (f"; più fitti nei capoversi {dove}" if dove else "")
                       + ". Se il trattino lungo è vietato, controlla che questo segno non lo stia sostituendo: si cambia la struttura della frase, non il segno.")
    return out


def concretezza(righe):
    """Capoversi lunghi senza numeri, nomi propri o date: la forma tipica del testo generico.

    Un capoverso argomentativo può esserne privo; conta la quota. Soglie PROVVISORIE."""
    pars = [(i, p) for i, p in enumerate(paragrafi(righe), 1) if len(p.split()) >= 40]
    if len(pars) < 4:
        return []
    senza = [i for i, p in pars if not numeri([p]) and not nomi([p])]
    if len(senza) >= 3 and len(senza) / len(pars) >= 0.5:
        elenco = ", ".join(str(i) for i in senza[:8]) + ("…" if len(senza) > 8 else "")
        return [f"concretezza: {len(senza)} capoversi su {len(pars)} (di almeno 40 parole) senza numeri né nomi propri ({elenco}). "
                "È la forma tipica del testo generico, che potrebbe stare identico in un altro testo (cinque prove, terza); "
                "un capoverso argomentativo può esserne privo. Soglie provvisorie."]
    return []


APERTURE_NEUTRE = {
    "en": set("the a an in on of to and but as at for with by from".split()),
    "it": set("il lo la i gli le un uno una in di a da su per con e ma".split()),
}


def strutture_ripetute(righe):
    """Chiusure a battuta, aperture ripetute e tre frasi di fila con lo stesso attacco."""
    R = PRF["ritmo"]
    neutre = APERTURE_NEUTRE[PRF["codice"]]
    pars = paragrafi(righe)
    out = []
    validi = chiusure = 0
    aperture = Counter()
    n_frasi = 0
    di_fila = []
    for i, p in enumerate(pars, 1):
        fr = PRF["frasi"](p)
        n_frasi += len(fr)
        if len(fr) >= 3:
            validi += 1
            n = [len(s.split()) for s in fr]
            if n[-1] <= R["breve"] and n[-2] >= R["medio"]:
                chiusure += 1
        attacchi = []
        for s in fr:
            w = re.findall(r"[^\W\d_][\w'’\-]*", s.lower())
            a = " ".join(w[:2]) if len(w) >= 4 and w[0] not in neutre else None
            attacchi.append(a)
            if a:
                aperture[a] += 1
        for j in range(len(attacchi) - 2):
            if attacchi[j] and attacchi[j] == attacchi[j + 1] == attacchi[j + 2]:
                di_fila.append((i, attacchi[j]))
                break
    if validi >= 4 and chiusure >= 3 and chiusure / validi >= 0.4:
        out.append(f"chiusure a battuta: {chiusure} capoversi su {validi} finiscono con una frase breve dopo una lunga. "
                   "Una battuta finale ripetuta a ogni capoverso è un tic; vale solo se capovolge un'attesa (diagnosi, sezione 4).")
    for a, k in aperture.most_common(2):
        if k >= 4 and k / max(n_frasi, 1) >= 0.1:
            out.append(f"apertura ripetuta: {k} frasi su {n_frasi} cominciano con «{a}».")
    for i, a in di_fila[:3]:
        out.append(f"tre frasi di fila con lo stesso attacco («{a}») nel capoverso {i}.")
    return out


APERTURA_SPIEGAZIONE = {
    "it": r"^(?:Cioè|Infatti|Ovvero|In altre parole|Significa|Vuol dire|Questo (?:significa|vuol dire)|Ciò (?:significa|vuol dire)|La ragione è|Il motivo è)\b",
    "en": r"^(?:That is|In other words|This means|Put simply|Simply put|The reason is)\b",
}


def aperture_secche(righe):
    """Capoversi che cominciano con una frase breve e netta, spiegata da quelle che seguono («to lecture»).

    La prima frase è breve (al più il doppio della soglia di frase breve) e la seconda è molto più lunga, oppure è
    introdotta da un marcatore di spiegazione. Soglie PROVVISORIE."""
    limite = 2 * PRF["ritmo"]["breve"]
    n_par = 0
    secche = []
    for i, p in enumerate(paragrafi(righe), 1):
        fr = PRF["frasi"](p)
        if len(fr) < 3:
            continue
        n_par += 1
        a, b = len(fr[0].split()), len(fr[1].split())
        spiega = re.match(APERTURA_SPIEGAZIONE[PRF["codice"]], fr[1].lstrip("*_ "))
        if (a <= limite and b >= 1.8 * a) or (a <= limite + 3 and spiega):
            secche.append(i)
    if n_par >= 6 and len(secche) >= 4 and len(secche) / n_par >= 0.25:
        elenco = ", ".join(str(i) for i in secche[:8]) + ("…" if len(secche) > 8 else "")
        return [f"aperture secche: {len(secche)} capoversi su {n_par} cominciano con una frase breve che la frase seguente spiega ({elenco}). "
                "Prova del contrario: se togliendola non si perde niente, si toglie; altrimenti la conclusione va dopo le ragioni (diagnosi, sezione 5). Soglie provvisorie."]
    return []


def capoversi_costanti(righe):
    """Capoversi di lunghezza quasi costante, che danno un ritmo a blocchi uguali.

    Si misurano i capoversi di almeno 30 parole: se almeno il 60% sta entro il 25% della mediana, oppure cinque di fila.
    Soglie PROVVISORIE."""
    valori = [len(p.split()) for p in paragrafi(righe) if len(p.split()) >= 30]
    if len(valori) < 8:
        return []
    med = st.median(valori)
    entro = [abs(n - med) <= 0.25 * med for n in valori]
    run = best = 0
    for e in entro:
        run = run + 1 if e else 0
        best = max(best, run)
    quota = sum(entro) / len(valori)
    if quota >= 0.6 or best >= 5:
        cv = st.pstdev(valori) / st.mean(valori)
        return [f"capoversi di lunghezza quasi costante: {len(valori)} capoversi, mediana {med:.0f} parole, {100 * quota:.0f}% entro il 25% della mediana, "
                f"al più {best} di fila (coefficiente di variazione {cv:.2f}). Si spezza o si fonde dove il ragionamento lo chiede (diagnosi, sezione 9). Soglie provvisorie."]
    return []


def aggiuntivi_comuni(righe):
    """Controlli di entrambe le lingue che non si riducono a un'espressione regolare per riga."""
    out = grappoli(righe)
    out += aperture_secche(righe)
    out += capoversi_costanti(righe)
    out += concretezza(righe)
    out += strutture_ripetute(righe)
    out += punteggiatura_di_pausa(righe)
    testo = testo_di(righe)
    parole = len(testo.split())
    k_b = len(re.findall(r"\*\*[^*\n]+\*\*", testo))
    if k_b >= 5 and 1000 * k_b / max(parole, 1) > 8:
        out.append(f"grassetto: {k_b} passaggi in {parole} parole ({1000 * k_b / max(parole, 1):.1f} ogni mille). Nel corpo della prosa il grassetto non serve; "
                   "le etichette a inizio paragrafo e i termini di un glossario sono legittimi.")
    out += titoli_incoerenti(righe)
    out += tipografia_mista(righe, doppie=PRF["codice"] == "en")
    return out


def tic_aggiuntivi_it(righe):
    """Controlli italiani che non si riducono a un'espressione regolare per riga."""
    return aggiuntivi_comuni(righe)


def tic_aggiuntivi_en(righe):
    """Controlli inglesi che non si riducono a un'espressione regolare per riga: coerenza, em dash e virgola seriale."""
    out = aggiuntivi_comuni(righe)
    pars = [p for p in paragrafi(righe)]
    testo = testo_di(righe)
    parole = len(testo.split())
    k_us, k_usa = len(re.findall(r"\bU\.S\.", testo)), len(re.findall(r"\bUS\b", testo))
    if k_us and k_usa:
        out.append(f"U.S. e US nello stesso testo ({k_us} e {k_usa}): una forma sola in tutto il documento.")
    senza_virgola = re.findall(r"\b(?:e\.g|i\.e)\.(?!,)", testo)
    if senza_virgola:
        out.append(f"e.g. / i.e. senza la virgola dopo: {len(senza_virgola)} occorrenze (il Chicago vuole «e.g.,» e «i.e.,»).")
    contratte = len(re.findall(r"\b\w+n['’]t\b|\b(?:it|that|there|he|she|we|they|you|i)['’](?:s|re|ve|ll|d|m)\b", testo, re.I))
    estese = len(re.findall(r"\b(?:do|does|did|is|are|was|were|have|has|had|would|could|should|will|can) not\b|\bcannot\b", testo, re.I))
    if contratte >= 3 and estese >= 3:
        out.append(f"registro incoerente, da valutare: {contratte} contrazioni e {estese} forme estese (do not, is not, cannot) nello stesso testo.")
    k_em = testo.count("—")
    if k_em:
        densi = [i for i, p in enumerate(pars, 1) if p.count("—") > 2]
        dens = 1000 * k_em / max(parole, 1)
        msg = f"em dash: {k_em} in {parole} parole ({dens:.1f} ogni mille)"
        if densi:
            msg += f"; più di una coppia nei capoversi {', '.join(map(str, densi))}"
        if dens > 6:
            msg += "; densità alta: l'em dash è un tic noto dei testi da LLM"
        msg += ". Il Chicago Manual of Style lo ammette senza spazi e con parsimonia; le convenzioni del progetto possono vietarlo."
        out.append(msg)
    # virgola seriale mancante: tre voci brevi «a, b and c»
    senza = re.findall(r"(?<![,;:] )\b(?!(?:However|Moreover|Furthermore|Therefore|Thus|Instead|Meanwhile|Finally|Also|Then)\b)([a-z][\w-]*), ([a-z][\w-]*) (?:and|or) ([a-z][\w-]*)\b", testo)
    con = len(re.findall(r"\b\w[\w-]*, [\w-]+(?: [\w-]+)?, (?:and|or) \w", testo))
    if senza:
        esempi = "; ".join(f"«{a}, {b} and {c}»" for a, b, c in senza[:3])
        out.append(f"virgola seriale: {len(senza)} possibili elenchi senza virgola prima di and/or ({esempi}), contro {con} con la virgola. "
                   "Il Chicago Manual of Style la vuole sempre; da valutare nel contesto.")
    return out


def cmd_tic(args):
    if not args:
        return uso()
    for indice, percorso in enumerate(args):
        if indice:
            print()
        righe = leggi_righe(percorso)
        print(f"== {percorso}")
        totale = 0
        for nome, rx in PRF["tic"]:
            for i, r in enumerate(righe, 1):
                for m in re.finditer(rx, r, re.IGNORECASE):
                    a, b = max(0, m.start() - 25), min(len(r), m.end() + 25)
                    print(f"   riga {i:3d} [{nome}] …{r[a:b].strip()}…")
                    totale += 1
        aggiuntivi = tic_aggiuntivi_en if PRF is PROFILI["en"] else tic_aggiuntivi_it
        for msg in aggiuntivi(righe):
            print(f"   [{PRF['codice']}] {msg}")
            totale += 1
        parole = len(testo_di(righe).split())
        k = len(re.findall(PRF["connettivi"], testo_di(righe), re.IGNORECASE))
        print(f"   connettivi di rotazione: {k} in {parole} parole ({1000 * k / max(parole, 1):.1f} ogni mille)")
        print(f"   segnalazioni: {totale}. Sono indizi da leggere nel contesto, non errori certi.")
    return 0


def conta_tic(righe):
    """Segnalazioni per famiglia di tic (stesse espressioni di `tic`)."""
    c = Counter()
    for nome, rx in PRF["tic"]:
        for r in righe:
            c[nome] += len(re.findall(rx, r, re.IGNORECASE))
    return c


def cmd_tic_confronto(args):
    """Confronto prima/dopo dei tic: serve al rapporto della stilista (misure) e a vedere i tic sostituiti da altri."""
    file_ = [a for a in args if not a.startswith("--")]
    if len(file_) != 2:
        return uso()
    o, r = leggi_righe(file_[0]), leggi_righe(file_[1])
    po, pr = len(testo_di(o).split()), len(testo_di(r).split())
    co, cr = conta_tic(o), conta_tic(r)
    aggiuntivi = tic_aggiuntivi_en if PRF is PROFILI["en"] else tic_aggiuntivi_it
    ao, ar = aggiuntivi(o), aggiuntivi(r)
    print(f"Origine:   {file_[0]} ({po} parole)")
    print(f"Risultato: {file_[1]} ({pr} parole)")
    print(f"(lessici dei tic aggiornati al {LESSICI_DATA}; sono indizi, non verdetti)\n")
    print(f"   {'famiglia':<62} {'prima':>5} {'dopo':>5}   ogni mille")
    for nome in sorted(set(co) | set(cr), key=lambda n: (-co[n], n)):
        a, b = co[nome], cr[nome]
        if a or b:
            print(f"   {nome[:62]:<62} {a:>5} {b:>5}   {1000 * a / max(po, 1):.1f} → {1000 * b / max(pr, 1):.1f}")
    k_o = len(re.findall(PRF["connettivi"], testo_di(o), re.IGNORECASE))
    k_r = len(re.findall(PRF["connettivi"], testo_di(r), re.IGNORECASE))
    print(f"   {'connettivi di rotazione':<62} {k_o:>5} {k_r:>5}   {1000 * k_o / max(po, 1):.1f} → {1000 * k_r / max(pr, 1):.1f}")
    g_o, g_r = sum(1 for m in ao if m.startswith("grappolo")), sum(1 for m in ar if m.startswith("grappolo"))
    print(f"   {'capoversi a grappolo':<62} {g_o:>5} {g_r:>5}")
    print(f"   {'controlli aggiuntivi (coerenza, punteggiatura, struttura)':<62} {len(ao) - g_o:>5} {len(ar) - g_r:>5}")
    tot_o, tot_r = sum(co.values()) + len(ao), sum(cr.values()) + len(ar)
    print(f"\nSegnalazioni in totale: {tot_o} → {tot_r}")
    aumentate = [n for n in cr if cr[n] > co[n]]
    if aumentate:
        print("AVVISO famiglie aumentate (un tic sostituito da un altro?): " + "; ".join(f"{n} {co[n]}→{cr[n]}" for n in aumentate))
    nuovi = sorted({m.split(":")[0] for m in ar} - {m.split(":")[0] for m in ao})
    if nuovi:
        print("AVVISO controlli aggiuntivi comparsi nel risultato: " + "; ".join(nuovi))
    return 0


# ------------------------------------------------------------ scorrevolezza

def cmd_scorrevolezza(args):
    if not args:
        return uso()
    frasi = PRF["frasi"]
    etichette = PRF["etichette"]
    staccato = PRF["breve_staccato"]
    if PRF["ritmo"]["provvisorio"]:
        print(f"(lingua: {PRF['nome']})")
        print(AVVISO_PROVVISORIO + "\n")
    for indice, percorso in enumerate(args):
        if indice:
            print()
        pars = paragrafi(leggi_righe(percorso))
        tot = Counter()
        elenco = []
        n_frasi = 0
        n_passive = 0
        run = 0
        for i, p in enumerate(pars, 1):
            for s in frasi(p):
                n_frasi += 1
                et = etichette(s)
                for e in et:
                    tot[re.sub(r"^\d+ ", "", e.split(" (")[0].split(" «")[0]).strip() or e] += 1
                if et:
                    elenco.append((i, s, et))
                if PRF is PROFILI["en"] and PASSIVO_EN.search(s):
                    n_passive += 1
                run = run + 1 if len(s.split()) <= staccato else 0
                if run == 4:
                    elenco.append((i, "(quattro frasi brevi di fila)", ["staccato"]))
                    tot["staccato"] += 1
        print(f"== {percorso}: {n_frasi} frasi, {len(elenco)} segnalate")
        for i, s, et in elenco:
            print(f"   p{i:02d} [{'; '.join(et)}]")
            print(f"        {s[:230]}{'…' if len(s) > 230 else ''}")
        if tot:
            print("   riepilogo: " + ", ".join(f"{k} {v}" for k, v in tot.most_common()))
        if PRF is PROFILI["en"] and n_frasi:
            quota = 100 * n_passive / n_frasi
            nota = ("; in inglese il passivo va giustificato (agente ignoto o irrilevante, oppure il paziente è il tema della frase)"
                    if quota > 20 else "")
            print(f"   passivi: {n_passive} frasi su {n_frasi} ({quota:.0f}%){nota}")
        print("   Sono indizi di possibile fatica di lettura, da giudicare leggendo ad alta voce.")
    return 0


# ----------------------------------------------------------------- confronta

# Nomi propri inglesi che in italiano si scrivono minuscoli (mesi, giorni): non sono differenze di contenuto.
NOMI_COMUNI_EN = set("""January February March April May June July August September October November December
Monday Tuesday Wednesday Thursday Friday Saturday Sunday""".split())

# Cautele che hanno un equivalente diretto nell'altra lingua: (etichetta, modello italiano, modello inglese).
EQUIVALENTI = [
    ("attribuzione «secondo / according to»", r"\bsecondo\b", r"\b[Aa]ccording to\b"),
    ("«si crede / is believed to»", r"\bsi (?:crede|ritiene|pensa)\b|\bè ritenut[aoie]\b",
     r"\b(?:is|are|was|were|been|be) (?:believed|thought|said|considered|assumed|presumed|alleged|claimed|understood)\b|\breportedly\b|\bsupposedly\b"),
    ("condizionale / modali", r"\b(?:avrebbe|avrebbero|potrebbe|potrebbero|sarebbe|sarebbero|dovrebbe)\b", r"\b(?:would|could|might|may|should)\b"),
    ("ipotesi / hypothesis", r"\bipotizz\w*|\bipotesi\b", r"\b[Hh]ypothes\w*"),
    ("forse, probabilmente / perhaps, probably", r"\bforse\b|\bprobabil\w*",
     r"\b[Pp]erhaps\b|\b[Pp]robabl\w+|\b[Pp]ossibl\w+|\b[Ll]ikel(?:y|ihood)\b|\b[Mm]aybe\b"),
    ("circa / about", r"\bcirca\b|\bintorno a\w*|\ball'incirca\b",
     r"\b(?:about|around|roughly|approximately|nearly|almost|some) (?=[\d$€£])|\b[Aa]pproximately\b|\b[Rr]oughly\b"),
    ("sembra / seems", r"\bsembr\w*|\bpare\b", r"\b[Ss]eem\w*|\b[Aa]ppear\w*"),
    ("stima / estimate", r"\bstim\w*", r"\b[Ee]stimat\w*"),
]


def sezioni_di(percorso, codice):
    """Sezioni (una per titolo) con le misure usate dal confronto, calcolate con il profilo della lingua del file."""
    global PRF
    precedente = PRF
    imposta_lingua(codice)
    try:
        righe = leggi_righe(percorso)
        elenco, titolo, corrente = [], None, []
        for r in righe:
            if re.match(r"^#{1,6}\s", r):
                elenco.append((titolo, corrente))
                titolo, corrente = r.strip(), []
            else:
                corrente.append(r)
        elenco.append((titolo, corrente))
        out = []
        for t, rr in elenco:
            testo = testo_di(rr)
            if t is None and not testo.split():
                continue
            ix = 1 if codice == "en" else 0
            out.append({
                "titolo": t or "(prima del primo titolo)",
                "numeri": numeri(rr),
                "nomi": nomi(rr) - NOMI_COMUNI_EN if codice == "en" else nomi(rr),
                "parole": len(testo.split()),
                "equiv": [len(re.findall(e[1 + ix], testo, re.I if codice == "it" else 0)) for e in EQUIVALENTI],
            })
        return out
    finally:
        PRF = precedente


def cmd_confronta(args):
    file_ = [a for a in args if not a.startswith("--")]
    if len(file_) != 2:
        return uso()
    a, b = sezioni_di(file_[0], "it"), sezioni_di(file_[1], "en")
    print(f"Italiano: {file_[0]}")
    print(f"Inglese:  {file_[1]}\n")
    if len(a) != len(b):
        print(f"NON ALLINEATI: {len(a)} sezioni in italiano, {len(b)} in inglese. Rilancia dopo aver sistemato i titoli "
              "(verifica_allineamento.py mostra le differenze).")
        return 1
    tot = Counter()
    for i, (x, y) in enumerate(zip(a, b), 1):
        righe = []
        solo_a, solo_b = sorted(x["numeri"] - y["numeri"]), sorted(y["numeri"] - x["numeri"])
        if solo_a or solo_b:
            righe.append(f"AVVISO numeri diversi: solo in italiano {', '.join(solo_a) or '-'}; solo in inglese {', '.join(solo_b) or '-'}")
            tot["numeri"] += 1
        na, nb = sorted(x["nomi"] - y["nomi"]), sorted(y["nomi"] - x["nomi"])
        if na or nb:
            righe.append(f"nomi diversi (nomi che cambiano forma nella traduzione sono normali): solo in italiano {', '.join(na[:12]) or '-'}; "
                         f"solo in inglese {', '.join(nb[:12]) or '-'}")
            tot["nomi"] += 1
        if x["parole"] and y["parole"]:
            rapporto = y["parole"] / x["parole"]
            if x["parole"] >= 40 and not 0.60 <= rapporto <= 1.20:
                righe.append(f"AVVISO lunghezza: {x['parole']} parole in italiano, {y['parole']} in inglese (rapporto {rapporto:.2f}; "
                             "tipico 0,8-1,1): omissione o aggiunta?")
                tot["lunghezza"] += 1
        for (et, _, _), ca, cb in zip(EQUIVALENTI, x["equiv"], y["equiv"]):
            if ca != cb:
                righe.append(f"AVVISO cautela, {et}: {ca} in italiano, {cb} in inglese")
                tot["cautele"] += 1
        titolo = x["titolo"] if x["titolo"] == y["titolo"] else f"{x['titolo']} | {y['titolo']}"
        print(f"== sezione {i}: {titolo} ({x['parole']} parole it, {y['parole']} en)")
        for r in righe:
            print(f"   {r}")
        if not righe:
            print("   nessuna differenza rilevata")
    print()
    print("Riepilogo: " + (", ".join(f"{k} {v}" for k, v in tot.most_common()) or "nessuna differenza meccanica."))
    print("Sono indizi: i numeri scritti in lettere, i nomi a inizio frase, le omissioni di mezza frase e i cambi di senso non sono visti. "
          "Il confronto frase per frase resta a chi legge.")
    return 0


# ---------------------------------------------------------------- struttura

def testo_grezzo(percorso):
    with open(percorso, encoding="utf-8") as f:
        return f.read()


def elementi(percorso):
    """Elementi che non sono prosa e devono restare identici fra una fase e l'altra."""
    grezzo = testo_grezzo(percorso)
    righe = grezzo.splitlines()
    idx = next((i for i, r in enumerate(righe) if PRF["note"].match(r.strip())), None)
    corpo = "\n".join(righe if idx is None else righe[:idx])
    note = "" if idx is None else "\n".join(righe[idx:])
    return {
        "titoli": [r.strip() for r in corpo.splitlines() if re.match(r"^#{1,6}\s", r)],
        "richiami a esponente": sorted(set(re.findall(r"[¹²³⁴⁵⁶⁷⁸⁹⁰]+", corpo))),
        "link": sorted(set(re.findall(r"\]\((https?://[^)\s]+)\)", grezzo))),
        "commenti HTML": re.findall(r"<!--.*?-->", grezzo, re.DOTALL),
        "etichette in grassetto a inizio paragrafo": re.findall(r"(?m)^\*\*([^*]{1,80})\*\*", corpo),
        "voci di elenco": len(re.findall(r"(?m)^\s*(?:[*\-]|\d+[.)])\s", corpo)),
        "_note": note,
    }


def cmd_struttura(args):
    if len(args) != 2:
        return uso()
    a, b = elementi(args[0]), elementi(args[1])
    problemi = 0
    print(f"Origine:   {args[0]}")
    print(f"Risultato: {args[1]}\n")
    for k in a:
        if k == "_note":
            continue
        if a[k] != b[k]:
            problemi += 1
            if isinstance(a[k], list) and isinstance(b[k], list):
                persi = [x for x in a[k] if x not in b[k]]
                nuovi = [x for x in b[k] if x not in a[k]]
                print(f"DIFFERENZA {k}: persi {persi or '-'}; nuovi {nuovi or '-'}")
            else:
                print(f"DIFFERENZA {k}: origine {a[k]}, risultato {b[k]}")
    if a["_note"] != b["_note"]:
        problemi += 1
        print("DIFFERENZA sezione Note: non identica all'origine")
    if not problemi:
        print("Titoli, richiami, link, commenti, etichette, elenchi e sezione Note coincidono con l'origine.")
    return 1 if problemi else 0


def uso():
    print(__doc__)
    return 2


def estrai_lingua(argv):
    """Toglie --lingua X dagli argomenti. Ritorna (codice, argomenti) oppure (None, None) se l'uso è errato."""
    args = list(argv)
    codice = "it"
    if "--lingua" in args:
        i = args.index("--lingua")
        if i + 1 >= len(args) or args[i + 1] not in LINGUE:
            return None, None
        codice = args[i + 1]
        args = args[:i] + args[i + 2:]
    return codice, args


def main():
    codice, argv = estrai_lingua(sys.argv[1:])
    if codice is None or not argv:
        return uso()
    imposta_lingua(codice)
    cmd, args = argv[0], argv[1:]
    comandi = {"integrita": cmd_integrita, "struttura": cmd_struttura, "ritmo": cmd_ritmo,
               "tic": cmd_tic, "tic-confronto": cmd_tic_confronto, "scorrevolezza": cmd_scorrevolezza, "confronta": cmd_confronta}
    if cmd not in comandi:
        return uso()
    return comandi[cmd](args)


if __name__ == "__main__":
    sys.exit(main())
