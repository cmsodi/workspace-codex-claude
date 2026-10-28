#!/usr/bin/env python3
"""Controlla che due file Markdown (due lingue dello stesso documento) abbiano la stessa struttura.

Uso: python3 -I verifica_allineamento.py FILE_A FILE_B

Confronta, in ordine: sequenza dei titoli (livelli), e per ogni sezione tra due titoli
il numero di righe di tabella, link, richiami a esponente, richiami [[...]], note
numerate, commenti HTML e blocchi di codice. Differenze su questi elementi bloccano.
Elenchi puntati e insiemi di URL diversi sono solo avvisi.

Codice di uscita: 0 allineati (anche con avvisi), 1 non allineati, 2 errore d'uso.
"""
import difflib
import re
import sys

SUP = "¹²³⁴⁵⁶⁷⁸⁹⁰"
BLOCCANTI = ["righe di tabella", "link", "richiami a esponente", "richiami [[...]]",
             "note numerate", "commenti HTML", "blocchi di codice"]


def leggi(path):
    with open(path, encoding="utf-8") as f:
        righe = f.read().split("\n")
    # salta il frontespizio YAML
    inizio = 0
    if righe and righe[0].strip() == "---":
        for i in range(1, len(righe)):
            if righe[i].strip() == "---":
                inizio = i + 1
                break
    return righe, inizio


def analizza(path):
    righe, inizio = leggi(path)
    titoli = []          # (livello, testo, numero riga)
    sezioni = [[]]       # righe di ogni sezione; la 0 è prima del primo titolo
    in_codice = False
    for n in range(inizio, len(righe)):
        r = righe[n]
        if r.strip().startswith("```"):
            in_codice = not in_codice
        m = None if in_codice else re.match(r"(#{1,6})\s+(.*)", r)
        if m:
            titoli.append((len(m.group(1)), m.group(2).strip(), n + 1))
            sezioni.append([])
        else:
            sezioni[-1].append(r)
    feats = []
    for s in sezioni:
        t = "\n".join(s)
        urls = re.findall(r"\]\((https?://[^)\s]+)", t)
        feats.append({
            "righe di tabella": sum(1 for r in s if r.lstrip().startswith("|")),
            "link": len(urls),
            "richiami a esponente": len(re.findall("[" + SUP + "]+", t)),
            "richiami [[...]]": len(re.findall(r"\[\[[^\]]*\]\]", t)),
            "note numerate": sum(1 for r in s if re.match(r"\d+\.\s", r)),
            "commenti HTML": len(re.findall(r"<!--", t)),
            "blocchi di codice": sum(1 for r in s if r.strip().startswith("```")) // 2,
            "elenchi puntati": sum(1 for r in s if re.match(r"\s*[-*•]\s", r)),
            "_urls": set(urls),
        })
    return titoli, feats


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    pa, pb = sys.argv[1], sys.argv[2]
    ta, fa = analizza(pa)
    tb, fb = analizza(pb)
    blocchi, avvisi = [], []

    la = [t[0] for t in ta]
    lb = [t[0] for t in tb]
    print(f"A: {pa}\n   {len(ta)} titoli")
    print(f"B: {pb}\n   {len(tb)} titoli")
    if la != lb:
        # I titoli non corrispondono: il confronto sezione per sezione non avrebbe senso.
        print("\nNON ALLINEATI: la sequenza dei titoli è diversa.")
        sm = difflib.SequenceMatcher(None, la, lb, autojunk=False)
        k = 0
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag == "equal":
                continue
            k += 1
            if k > 10:
                print("  ... altre differenze non mostrate")
                break
            qa = "; ".join(f"riga {t[2]} \"{t[1][:35]}\"" for t in ta[i1:i2]) or "nessuno"
            qb = "; ".join(f"riga {t[2]} \"{t[1][:35]}\"" for t in tb[j1:j2]) or "nessuno"
            print(f"  - {tag}: A ha {qa} | B ha {qb}")
        print("Sistema i titoli (o rendi le strutture uguali) e rilancia il controllo.")
        return 1

    n = min(len(fa), len(fb))
    for i in range(n):
        nome_a = f"riga {ta[i - 1][2]} \"{ta[i - 1][1][:40]}\"" if i > 0 else "prima del primo titolo"
        nome_b = f"riga {tb[i - 1][2]} \"{tb[i - 1][1][:40]}\"" if i > 0 else "prima del primo titolo"
        for k in BLOCCANTI:
            if fa[i][k] != fb[i][k]:
                blocchi.append(f"Sezione {i} ({nome_a} | {nome_b}): {k} {fa[i][k]} contro {fb[i][k]}.")
        if fa[i]["elenchi puntati"] != fb[i]["elenchi puntati"]:
            avvisi.append(f"Sezione {i} ({nome_a} | {nome_b}): elenchi puntati "
                          f"{fa[i]['elenchi puntati']} contro {fb[i]['elenchi puntati']}.")
        if fa[i]["_urls"] != fb[i]["_urls"] and fa[i]["link"] == fb[i]["link"]:
            avvisi.append(f"Sezione {i} ({nome_a} | {nome_b}): stesso numero di link ma URL diversi.")

    if avvisi:
        print(f"\nAvvisi ({len(avvisi)}), non bloccanti:")
        for a in avvisi[:20]:
            print("  -", a)
        if len(avvisi) > 20:
            print(f"  ... e altri {len(avvisi) - 20}")
    if blocchi:
        print(f"\nNON ALLINEATI: {len(blocchi)} differenze strutturali.")
        for b in blocchi[:40]:
            print("  -", b)
        if len(blocchi) > 40:
            print(f"  ... e altre {len(blocchi) - 40}")
        return 1
    print("\nALLINEATI: stessa sequenza di titoli e stessi elementi non prosa in ogni sezione.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
