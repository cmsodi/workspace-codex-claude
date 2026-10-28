#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prove di controlla.py (italiano e inglese) e della coerenza fra i due plugin.

Uso, dalla radice del marketplace:  python3 -I prove/test_controlla.py

Solo libreria standard. I file in fixtures/ sono testi di prova scritti da Claude, non campioni di autori reali.
I file in golden/ sono gli output della versione di controlla.py precedente alla generalizzazione
(solo italiano): i test garantiscono che l'italiano non sia cambiato.
"""
import filecmp
import os
import subprocess
import sys
import tempfile
import unittest

RADICE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIX = os.path.join(RADICE, "prove", "fixtures")
GOLD = os.path.join(RADICE, "prove", "golden")
IT = os.path.join(RADICE, "italiano", "strumenti", "controlla.py")
EN = os.path.join(RADICE, "inglese", "strumenti", "controlla.py")


def esegui(script, *args, cwd=FIX):
    p = subprocess.run([sys.executable, "-I", script, *args], cwd=cwd, capture_output=True, text=True)
    return p.returncode, p.stdout


def golden(nome):
    with open(os.path.join(GOLD, nome), encoding="utf-8") as f:
        return f.read()


def file_temporaneo(testo):
    f = tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8")
    f.write(testo)
    f.close()
    return f.name


class CopieIdentiche(unittest.TestCase):
    def test_controlla_uguale_nei_due_plugin(self):
        self.assertTrue(filecmp.cmp(IT, EN, shallow=False), "controlla.py differisce fra italiano e inglese")

    def test_verifica_integrita_uguale_nei_due_plugin(self):
        a = os.path.join(RADICE, "italiano", "strumenti", "verifica_integrita.py")
        b = os.path.join(RADICE, "inglese", "strumenti", "verifica_integrita.py")
        self.assertTrue(filecmp.cmp(a, b, shallow=False))


class ItalianoInvariato(unittest.TestCase):
    """L'italiano deve dare gli stessi output di prima, con e senza --lingua it."""

    def confronta(self, nome_golden, *args, rc_atteso=0):
        for prefisso in ([], ["--lingua", "it"]):
            rc, out = esegui(IT, *prefisso, *args)
            self.assertEqual(rc, rc_atteso)
            self.assertEqual(out, golden(nome_golden))

    def test_ritmo(self):
        self.confronta("it-origine.ritmo.txt", "ritmo", "it-origine.md")

    def test_ritmo_cerniere(self):
        self.confronta("it-origine.ritmo-cerniere.txt", "ritmo", "--registro", "cerniere", "it-origine.md")

    def test_tic(self):
        self.confronta("it-origine.tic.txt", "tic", "it-origine.md")

    def test_scorrevolezza(self):
        self.confronta("it-origine.scorrevolezza.txt", "scorrevolezza", "it-origine.md")

    def test_integrita(self):
        rc_atteso = int(golden("it-integrita.rc").strip())
        self.confronta("it-integrita.txt", "integrita", "it-origine.md", "it-rivisto.md", rc_atteso=rc_atteso)

    def test_struttura(self):
        self.confronta("it-struttura.txt", "struttura", "it-origine.md", "it-rivisto.md")


class ItalianoTicAggiunti(unittest.TestCase):
    def test_negazione_difensiva_lessico_e_iperbole(self):
        t = file_temporaneo("Si deve utilizzare il sistema anziché l'altro, al fine di effettuare un controllo vero e proprio.\n")
        try:
            _, out = esegui(IT, "tic", t)
        finally:
            os.unlink(t)
        for etichetta in ("negazione difensiva", "lessico da traduzione o da burocrazia", "iperbole"):
            self.assertIn(etichetta, out)


class CommentiHtml(unittest.TestCase):
    def test_il_commento_html_non_conta_come_prosa(self):
        con = file_temporaneo("<!-- nota dell'autore -->\nUna frase di prova con dieci parole in tutto, più o meno.\n")
        senza = file_temporaneo("Una frase di prova con dieci parole in tutto, più o meno.\n")
        try:
            for script, lingua in ((IT, "it"), (EN, "en")):
                a = esegui(script, "--lingua", lingua, "ritmo", con)[1].replace(con, "X")
                b = esegui(script, "--lingua", lingua, "ritmo", senza)[1].replace(senza, "X")
                self.assertEqual(a, b)
        finally:
            os.unlink(con)
            os.unlink(senza)


class Correzioni(unittest.TestCase):
    """Difetti trovati provando i plugin installati in una sessione reale."""

    def test_modeling_e_americano_modelling_no(self):
        t = file_temporaneo("The team modeled the flow and labeled the traveled path. Later it was modelling and labelling.\n")
        try:
            _, out = esegui(EN, "--lingua", "en", "tic", t)
        finally:
            os.unlink(t)
        self.assertEqual(out.count("[ortografia britannica]"), 2, out)
        self.assertIn("modelling", out)
        self.assertNotIn("modeled", out.split("[ortografia britannica]")[1])

    def test_nome_a_inizio_frase_non_e_perso(self):
        a = file_temporaneo("The area was reached in 1927 by Leonid Kulik, a mineralogist.\n")
        b = file_temporaneo("Leonid Kulik, a mineralogist, reached the area in 1927.\n")
        try:
            rc, out = esegui(EN, "--lingua", "en", "integrita", a, b)
        finally:
            os.unlink(a)
            os.unlink(b)
        self.assertEqual(rc, 0, out)
        self.assertNotIn("Leonid", out)

    def test_nome_davvero_perso_resta_segnalato(self):
        a = file_temporaneo("The area was reached in 1927 by Leonid Kulik, a mineralogist.\n")
        b = file_temporaneo("The area was reached in 1927 by a mineralogist.\n")
        try:
            _, out = esegui(EN, "--lingua", "en", "integrita", a, b)
        finally:
            os.unlink(a)
            os.unlink(b)
        self.assertIn("Leonid", out)

    def test_it_is_thought_that_e_una_cautela(self):
        a = file_temporaneo("It is thought that the blast happened in the air.\n")
        b = file_temporaneo("The blast happened in the air.\n")
        try:
            _, out = esegui(EN, "--lingua", "en", "integrita", a, b)
        finally:
            os.unlink(a)
            os.unlink(b)
        self.assertIn("cautela forse persa, «is believed / thought / said»", out)


class IntegritaSuUnPezzo(unittest.TestCase):
    def test_righe_dell_origine(self):
        # il primo capoverso di en-origine.md sta alla riga 4; il pezzo rivisto contiene solo quello
        pezzo = file_temporaneo("At about 7:17 a.m. on June 30, 1908, a bluish light crossed the sky. Farmers saw it from the hills. "
                                "The blast flattened roughly 2,000 square kilometers of forest, and the trees lay in a radial pattern.\n")
        try:
            rc, out = esegui(EN, "--lingua", "en", "integrita", "en-origine.md", pezzo, "--righe", "4-4")
            rc_senza, out_senza = esegui(EN, "--lingua", "en", "integrita", "en-origine.md", pezzo)
        finally:
            os.unlink(pezzo)
        self.assertEqual(rc, 0, out)
        self.assertIn("(solo righe 4-4)", out)
        self.assertIn("Numeri e nomi coincidono", out)
        # senza --righe l'origine intera ha cose che il pezzo non ha
        self.assertIn("Kulik", out_senza)

    def test_intervallo_non_valido(self):
        for val in ("3", "5-2", "0-4", "a-b"):
            rc, _ = esegui(EN, "--lingua", "en", "integrita", "en-origine.md", "en-rivisto-ok.md", "--righe", val)
            self.assertEqual(rc, 2, val)

    def test_senza_righe_come_prima(self):
        rc, out = esegui(EN, "--lingua", "en", "integrita", "en-origine.md", "en-rivisto-ok.md")
        self.assertEqual(rc, 0)
        self.assertNotIn("solo righe", out)


class Confronta(unittest.TestCase):
    def test_traduzione_fedele(self):
        rc, out = esegui(EN, "confronta", "bil-it.md", "bil-en-ok.md")
        self.assertEqual(rc, 0, out)
        for segnale in ("AVVISO numeri", "AVVISO cautela", "AVVISO lunghezza"):
            self.assertNotIn(segnale, out)

    def test_traduzione_infedele(self):
        rc, out = esegui(EN, "confronta", "bil-it.md", "bil-en-guasto.md")
        self.assertEqual(rc, 0, out)
        self.assertIn("solo in italiano 40; solo in inglese 60", out)
        self.assertIn("cautela, attribuzione «secondo / according to»", out)
        self.assertIn("cautela, condizionale / modali", out)
        self.assertIn("cautela, stima / estimate", out)
        self.assertIn("AVVISO lunghezza", out)
        self.assertIn("England", out)

    def test_sezioni_non_allineate(self):
        monca = file_temporaneo("# The Event\n\nOne section only.\n")
        try:
            rc, out = esegui(EN, "confronta", "bil-it.md", monca)
        finally:
            os.unlink(monca)
        self.assertEqual(rc, 1)
        self.assertIn("NON ALLINEATI", out)

    def test_servono_due_file(self):
        rc, _ = esegui(EN, "confronta", "bil-it.md")
        self.assertEqual(rc, 2)

    def test_mesi_inglesi_non_sono_nomi_diversi(self):
        _, out = esegui(EN, "confronta", "bil-it.md", "bil-en-ok.md")
        self.assertNotIn("June", out)


class Allineamento(unittest.TestCase):
    SCRIPT = os.path.join(RADICE, "inglese", "strumenti", "verifica_allineamento.py")

    def test_allineati(self):
        rc, out = esegui(self.SCRIPT, "bil-it.md", "bil-en-ok.md")
        self.assertEqual(rc, 0, out)

    def test_titoli_diversi(self):
        monca = file_temporaneo("# The Event\n\nOne section only.\n")
        try:
            rc, _ = esegui(self.SCRIPT, "bil-it.md", monca)
        finally:
            os.unlink(monca)
        self.assertEqual(rc, 1)


class Uso(unittest.TestCase):
    def test_lingua_sconosciuta(self):
        rc, _ = esegui(EN, "--lingua", "xx", "ritmo", "en-buono.md")
        self.assertEqual(rc, 2)

    def test_lingua_senza_valore(self):
        rc, _ = esegui(EN, "ritmo", "en-buono.md", "--lingua")
        self.assertEqual(rc, 2)

    def test_senza_comando(self):
        rc, _ = esegui(EN, "--lingua", "en")
        self.assertEqual(rc, 2)

    def test_lingua_ovunque_negli_argomenti(self):
        rc1, o1 = esegui(EN, "--lingua", "en", "tic", "en-llm.md")
        rc2, o2 = esegui(EN, "tic", "en-llm.md", "--lingua", "en")
        self.assertEqual((rc1, o1), (rc2, o2))


class InglesTic(unittest.TestCase):
    def test_testo_da_llm(self):
        rc, out = esegui(EN, "--lingua", "en", "tic", "en-llm.md")
        self.assertEqual(rc, 0)
        for etichetta in ("apertura o chiusura formulaica", "annuncio di rilevanza", "meta-annuncio", "perifrasi della copula",
                          "lessico da LLM", "corporate-speak", "ortografia britannica", "«not X, it's Y»",
                          "trattino spaziato, doppio", "[en] em dash"):
            self.assertIn(etichetta, out, etichetta)

    def test_not_x_its_y_trovato_due_volte(self):
        _, out = esegui(EN, "--lingua", "en", "tic", "en-llm.md")
        self.assertEqual(out.count("[«not X, it's Y»"), 2)

    def test_calchi_dall_italiano(self):
        _, out = esegui(EN, "--lingua", "en", "tic", "en-italianismi.md")
        for parte in ("depends from", "discussed about", "informations", "the people is", "From one side", "In the nineties",
                      "data in formato non americano", "ortografia britannica", "punto o virgola fuori dalle virgolette",
                      "virgola seriale"):
            self.assertIn(parte, out, parte)

    def test_testo_pulito_senza_tic_principali(self):
        _, out = esegui(EN, "--lingua", "en", "tic", "en-buono.md")
        for etichetta in ("lessico da LLM", "apertura o chiusura", "annuncio di rilevanza", "calco", "ortografia britannica",
                          "virgola seriale", "[en] em dash", "corporate-speak"):
            self.assertNotIn(etichetta, out, etichetta)

    def test_il_commento_html_non_e_prosa(self):
        _, out = esegui(EN, "--lingua", "en", "tic", "en-buono.md")
        self.assertNotIn("TESTO DI PROVA", out)

    def test_sull_italiano_non_scattano_le_regole_inglesi(self):
        _, out = esegui(IT, "tic", "en-llm.md")
        self.assertNotIn("lessico da LLM", out)
        _, out = esegui(IT, "tic", "en-segni-catalogo.md")
        for etichetta in ("grappolo", "attribuzione vaga", "segnaposto"):
            self.assertNotIn(etichetta, out, etichetta)

    def tic_su(self, testo, *, lingua="en"):
        t = file_temporaneo(testo)
        try:
            _, out = esegui(EN, "--lingua", lingua, "tic", t)
        finally:
            os.unlink(t)
        return out

    def test_titoli_incoerenti_nello_stesso_livello(self):
        out = self.tic_su("# Harbor ledger\n\n## Harbor Ledger Basics\n\nText here.\n\n## How the ledger works today\n\nMore text.\n")
        self.assertIn("titoli di livello 2 incoerenti", out)

    def test_titoli_coerenti_o_di_livelli_diversi_non_sono_segnalati(self):
        out = self.tic_su("# The Harbor Ledger Explained\n\n## How the ledger works today\n\nText.\n\n## Why the ledger matters here\n\nMore.\n")
        self.assertNotIn("incoerenti", out)

    def test_apostrofi_e_virgolette_miste(self):
        out = self.tic_su('It\'s the clerk’s ledger. He said "no" and then “yes”.\n')
        self.assertIn("apostrofi misti: 1 dritti e 1 ricurvi", out)
        self.assertIn("virgolette doppie miste: 2 dritte e 2 ricurve", out)

    def test_tipografia_coerente_e_codice_non_segnalati(self):
        out = self.tic_su("It’s the clerk’s ledger. Use `it's` or see [the page](https://example.org/it's-here) for details.\n")
        self.assertNotIn("misti", out)

    def test_us_ed_eg(self):
        out = self.tic_su("The U.S. office and the US office agree (e.g. on fees; i.e., on the rate).\n")
        self.assertIn("U.S. e US nello stesso testo (1 e 1)", out)
        self.assertIn("e.g. / i.e. senza la virgola dopo: 1 occorrenze", out)

    def test_contrazioni_e_forme_estese(self):
        out = self.tic_su("It's late. We don't know. They're gone. He did not call. She is not here. It does not matter.\n")
        self.assertIn("registro incoerente", out)
        out = self.tic_su("It's late. We don't know. They're gone. He called. She left.\n")
        self.assertNotIn("registro incoerente", out)

    def test_segni_del_catalogo(self):
        rc, out = esegui(EN, "--lingua", "en", "tic", "en-segni-catalogo.md")
        self.assertEqual(rc, 0)
        for etichetta in ("enfasi sul significato", "linguaggio da brochure", "attribuzione vaga", "formula delle sfide",
                          "associazione vaga", "avvertenza didattica", "parola ricercata", "residuo della chat",
                          "disclaimer sul sapere", "segnaposto", "emoji come formattazione", "elenco con etichetta in grassetto"):
            self.assertIn(etichetta, out, etichetta)

    def test_etichette_di_lavoro_e_link_non_sono_segnaposto(self):
        _, out = esegui(EN, "--lingua", "en", "tic", "en-segni-catalogo.md")
        segnaposto = [r for r in out.splitlines() if "[segnaposto]" in r]
        self.assertEqual(len(segnaposto), 1, segnaposto)
        self.assertIn("[Your Name]", segnaposto[0])
        _, out = esegui(EN, "--lingua", "en", "tic", "en-non-segni.md")
        self.assertNotIn("segnaposto", out)

    def test_grappolo_solo_con_indizi_vicini(self):
        _, out = esegui(EN, "--lingua", "en", "tic", "en-segni-catalogo.md")
        self.assertIn("grappolo: il capoverso 1", out)
        self.assertIn("grappolo: il capoverso 2", out)
        _, out = esegui(EN, "--lingua", "en", "tic", "en-non-segni.md")
        self.assertNotIn("grappolo", out)

    def test_testo_formale_e_corretto_non_ha_segni_nuovi(self):
        _, out = esegui(EN, "--lingua", "en", "tic", "en-non-segni.md")
        for etichetta in ("enfasi sul significato", "brochure", "attribuzione vaga", "residuo della chat", "emoji",
                          "avvertenza didattica", "disclaimer", "parola ricercata"):
            self.assertNotIn(etichetta, out, etichetta)

    def test_testo_pulito_senza_segni_nuovi(self):
        _, out = esegui(EN, "--lingua", "en", "tic", "en-buono.md")
        for etichetta in ("grappolo", "attribuzione vaga", "segnaposto", "residuo della chat", "emoji", "brochure"):
            self.assertNotIn(etichetta, out, etichetta)

    def test_grassetto_sparso_nel_corpo(self):
        t = file_temporaneo("The plan has **three** parts. The **first** covers **cost**, the **second** covers **time**, "
                            "and the **third** covers **risk**. Each part is short.\n")
        try:
            _, out = esegui(EN, "--lingua", "en", "tic", t)
        finally:
            os.unlink(t)
        self.assertIn("[en] grassetto: 7 passaggi", out)


class ItalianoSegni(unittest.TestCase):
    """Parità italiana con i segni del catalogo: famiglie, grappoli, non-segni, coerenza."""

    def tic_su(self, testo):
        t = file_temporaneo(testo)
        try:
            _, out = esegui(IT, "tic", t)
        finally:
            os.unlink(t)
        return out

    def test_segni_del_catalogo(self):
        rc, out = esegui(IT, "tic", "it-segni-catalogo.md")
        self.assertEqual(rc, 0)
        for etichetta in ("enfasi sul significato", "lessico da brochure", "attribuzione vaga", "formula delle sfide",
                          "associazione vaga", "avvertenza didattica", "residuo della chat", "disclaimer sul sapere",
                          "segnaposto", "emoji come formattazione", "elenco con etichetta in grassetto",
                          "titoli di livello 1 in Title Case"):
            self.assertIn(etichetta, out, etichetta)

    def test_etichette_di_lavoro_e_link_non_sono_segnaposto(self):
        _, out = esegui(IT, "tic", "it-segni-catalogo.md")
        segnaposto = [r for r in out.splitlines() if "[segnaposto]" in r]
        self.assertEqual(len(segnaposto), 1, segnaposto)
        self.assertIn("[Il tuo nome]", segnaposto[0])
        _, out = esegui(IT, "tic", "it-non-segni.md")
        self.assertNotIn("segnaposto", out)

    def test_grappolo_solo_con_indizi_vicini(self):
        _, out = esegui(IT, "tic", "it-segni-catalogo.md")
        self.assertIn("[it] grappolo: il capoverso 1", out)
        self.assertIn("[it] grappolo: il capoverso 2", out)
        _, out = esegui(IT, "tic", "it-non-segni.md")
        self.assertNotIn("grappolo", out)

    def test_testo_formale_e_corretto_non_ha_segni_nuovi(self):
        _, out = esegui(IT, "tic", "it-non-segni.md")
        for etichetta in ("enfasi sul significato", "brochure", "attribuzione vaga", "residuo della chat", "emoji",
                          "avvertenza didattica", "disclaimer", "Title Case", "misti"):
            self.assertNotIn(etichetta, out, etichetta)

    def test_testo_di_autore_senza_segni_nuovi(self):
        _, out = esegui(IT, "tic", "it-origine.md")
        for etichetta in ("grappolo", "attribuzione vaga", "segnaposto", "residuo della chat", "emoji", "Title Case", "misti"):
            self.assertNotIn(etichetta, out, etichetta)

    def test_apostrofi_misti_ma_non_le_virgolette(self):
        out = self.tic_su("L'uomo e l’anno. Disse «sì» e poi \"no\".\n")
        self.assertIn("apostrofi misti: 1 dritti e 1 ricurvi", out)
        self.assertNotIn("virgolette doppie miste", out)

    def test_titolo_in_frase_non_e_title_case(self):
        out = self.tic_su("# Il registro del porto\n\n## Come funziona il registro\n\nTesto.\n")
        self.assertNotIn("Title Case", out)

    def test_controlli_inglesi_non_scattano_in_italiano(self):
        out = self.tic_su("Gli U.S. e gli US; per es. e.g. qui. Non lo so. Non lo sapevo. Non lo saprò. Non lo sappiamo.\n")
        self.assertNotIn("U.S. e US", out)
        self.assertNotIn("e.g.", out)
        self.assertNotIn("registro incoerente", out)


class InglesRitmoEScorrevolezza(unittest.TestCase):
    def test_soglie_dichiarate_provvisorie(self):
        for comando in ("ritmo", "scorrevolezza"):
            _, out = esegui(EN, "--lingua", "en", comando, "en-buono.md")
            self.assertIn("provvisorie", out)

    def test_italiano_non_ha_il_banner(self):
        _, out = esegui(IT, "ritmo", "it-origine.md")
        self.assertNotIn("provvisorie", out)

    def test_frasi_con_abbreviazioni(self):
        t = file_temporaneo("Dr. Smith met the U.S. ambassador at 5 p.m. on Tuesday. He left. Mr. Lee stayed. "
                            'She said "Go." Then she left.\n')
        try:
            _, out = esegui(EN, "--lingua", "en", "ritmo", t)
        finally:
            os.unlink(t)
        self.assertIn("5 frasi", out)

    def test_soglie_italiane_non_valgono_in_inglese(self):
        _, out = esegui(EN, "--lingua", "en", "ritmo", "en-buono.md")
        self.assertIn("fino a 7:", out)
        self.assertIn("oltre 30:", out)
        _, out_it = esegui(IT, "ritmo", "it-origine.md")
        self.assertIn("fino a 8:", out_it)
        self.assertIn("oltre 35:", out_it)

    def test_segnala_vago_this_e_passivi(self):
        t = file_temporaneo("The report was written by a clerk and was filed in a drawer nobody opened. "
                            "This is a problem for everyone who reads the long list that was compiled last year.\n")
        try:
            _, out = esegui(EN, "--lingua", "en", "scorrevolezza", t)
        finally:
            os.unlink(t)
        self.assertIn("passivi ripetuti", out)
        self.assertIn("«This/That» come soggetto senza nome", out)
        self.assertIn("passivi: 2 frasi su 2", out)

    def test_testo_chiaro_non_segnalato(self):
        _, out = esegui(EN, "--lingua", "en", "scorrevolezza", "en-buono.md")
        self.assertIn("0 segnalate", out)


class InglesIntegrita(unittest.TestCase):
    def test_riscrittura_fedele(self):
        rc, out = esegui(EN, "--lingua", "en", "integrita", "en-origine.md", "en-rivisto-ok.md")
        self.assertEqual(rc, 0, out)
        self.assertIn("Numeri e nomi coincidono", out)
        self.assertNotIn("cautela", out)

    def test_riscrittura_infedele(self):
        rc, out = esegui(EN, "--lingua", "en", "integrita", "en-origine.md", "en-rivisto-guasto.md")
        self.assertEqual(rc, 1)
        self.assertIn("20000", out)
        self.assertIn("Popov", out)
        self.assertIn("cautela forse persa, «according to»", out)
        self.assertIn("cautela forse persa, «modali", out)
        self.assertIn("possibili omissioni", out)

    def test_numeri_in_formato_americano(self):
        a = file_temporaneo("The fund held 1,000,000 dollars and 3.5 percent of shares.\n")
        b = file_temporaneo("The fund held 1000000 dollars and 3.5 percent of shares.\n")
        try:
            rc, out = esegui(EN, "--lingua", "en", "integrita", a, b)
        finally:
            os.unlink(a)
            os.unlink(b)
        self.assertEqual(rc, 0, out)
        self.assertIn("Numeri e nomi coincidono", out)

    def test_maggio_non_e_una_cautela(self):
        a = file_temporaneo("In May the committee met. It may meet again.\n")
        b = file_temporaneo("The committee met in May. It may meet again.\n")
        try:
            _, out = esegui(EN, "--lingua", "en", "integrita", a, b)
        finally:
            os.unlink(a)
            os.unlink(b)
        self.assertNotIn("cautela", out)

    def test_struttura_titolo_cambiato(self):
        a = file_temporaneo("# Title one\n\nSome text.\n")
        b = file_temporaneo("# Title two\n\nSome text.\n")
        try:
            rc, out = esegui(EN, "--lingua", "en", "struttura", a, b)
        finally:
            os.unlink(a)
            os.unlink(b)
        self.assertEqual(rc, 1)
        self.assertIn("DIFFERENZA titoli", out)

    def test_struttura_senza_differenze(self):
        rc, out = esegui(EN, "--lingua", "en", "struttura", "en-origine.md", "en-origine.md")
        self.assertEqual(rc, 0, out)

    def test_sezione_notes_esclusa_dal_testo(self):
        a = file_temporaneo("A short text with 12 apples.\n\n---\n\n## Notes\n\nSource: 1999 survey of Boston.\n")
        b = file_temporaneo("A short text with 12 apples.\n\n---\n\n## Note\n\nFonte: indagine del 2001.\n")
        try:
            rc, out = esegui(EN, "--lingua", "en", "integrita", a, b)
        finally:
            os.unlink(a)
            os.unlink(b)
        self.assertEqual(rc, 0, out)
        self.assertNotIn("1999", out)


if __name__ == "__main__":
    unittest.main(verbosity=1)
