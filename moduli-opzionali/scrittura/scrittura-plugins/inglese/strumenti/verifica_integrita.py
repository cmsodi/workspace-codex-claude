#!/usr/bin/env python3
"""Verifica che una versione rivista di un file Markdown non abbia alterato formattazione e caratteri speciali.

Uso: python3 -I verifica_integrita.py ORIGINALE RIVISTO [--righe A-B] [--max N]

Confronta riga per riga (le due versioni devono avere lo stesso numero di righe,
ignorando le righe vuote finali):
- le righe "protette" devono essere identiche: frontespizio YAML, blocchi di codice,
  righe di tabella, titoli, commenti HTML, linee orizzontali, righe vuote e, sotto un
  titolo "Note/Notes/References/Bibliografia", le note numerate;
- nelle righe di prosa modificate devono restare uguali: link e URL, richiami `[[...]]`,
  note `[^n]`, codice in linea, tag HTML, entità, escape con barra rovesciata, marcatori di
  enfasi (`*`, `**`, `_`, `__`, `~~`), parentesi quadre, caratteri non ASCII che non sono
  lettere (©, ¹, «», virgolette tipografiche, trattini lunghi, spazi non separabili),
  a capo con due spazi e prefisso della riga (rientro, elenco, citazione).
I numeri che cambiano in una riga di prosa sono solo un avviso.

--righe A-B confronta le righe A-B (1-based) dell'ORIGINALE con tutto il RIVISTO: serve
per un pezzo singolo.

Codice di uscita: 0 integro (anche con avvisi), 1 differenze, 2 errore d'uso.
"""
import re
import sys
import unicodedata
from collections import Counter

NOTE_TITOLO = re.compile(r"^#{1,6}\s+(notes?|note|references?|bibliograph\w*|bibliografia|riferimenti)\s*$", re.I)


def leggi(path):
    with open(path, encoding="utf-8", newline="") as f:
        t = f.read()
    righe = t.replace("\r\n", "\n").split("\n")
    while righe and righe[-1] == "":
        righe.pop()
    return righe


def protette(righe):
    """Lista di booleani: True se la riga va lasciata identica."""
    out = []
    in_yaml = in_code = False
    in_note = False
    for i, r in enumerate(righe):
        prot = False
        if i == 0 and r.strip() == "---":
            in_yaml = True
            prot = True
        elif in_yaml:
            prot = True
            if r.strip() == "---":
                in_yaml = False
        elif r.strip().startswith("```"):
            in_code = not in_code
            prot = True
        elif in_code:
            prot = True
        elif r.strip() == "":
            prot = True
        elif r.lstrip().startswith("|"):
            prot = True
        elif re.match(r"#{1,6}\s", r):
            prot = True
            in_note = bool(NOTE_TITOLO.match(r))
        elif r.lstrip().startswith("<!--"):
            prot = True
        elif re.match(r"(-{3,}|\*{3,}|_{3,})\s*$", r.strip()):
            prot = True
        elif in_note and re.match(r"\d+[.)]\s", r):
            prot = True
        out.append(prot)
    return out


def impronta(s):
    c = Counter()
    t = s
    for pat, nome in [
        (r"\]\([^)]*\)", "link"),
        (r"\[\[[^\]]*\]\]", "richiamo [[...]]"),
        (r"`[^`]*`", "codice in linea"),
        (r"\[\^[^\]]+\]", "nota [^n]"),
        (r"<[^>\n]+>", "tag HTML"),
        (r"&#?\w+;", "entità HTML"),
        (r"\\.", "escape"),
        (r"https?://[^\s)>\]]+", "URL"),
    ]:
        for m in re.findall(pat, t):
            c[f"{nome} {m}"] += 1
        t = re.sub(pat, " ", t)
    for m in re.findall(r"\*\*|__|~~|\*|_", t):
        c[f"marcatore {m}"] += 1
    c["[ "] = t.count("[")
    c["] "] = t.count("]")
    for ch in s:
        if ord(ch) > 127 and not ch.isalpha():
            c[f"carattere U+{ord(ch):04X} {unicodedata.name(ch, '?')}"] += 1
    if s.endswith("  "):
        c["a capo con due spazi"] += 1
    c["prefisso " + repr(re.match(r"^[\s>]*(?:[-*+]\s+|\d+[.)]\s+)?", s).group(0))] += 1
    return +c


def numeri(s):
    s = re.sub(r"\]\([^)]*\)", " ", s)
    s = re.sub(r"https?://\S+", " ", s)
    return Counter(re.findall(r"\d+(?:[.,]\d+)*", s))


def main():
    a = sys.argv[1:]
    if len(a) < 2:
        print(__doc__)
        return 2
    orig_p, riv_p = a[0], a[1]
    rng, massimo = None, 40
    i = 2
    while i < len(a):
        if a[i] == "--righe" and i + 1 < len(a):
            m = re.match(r"(\d+)-(\d+)$", a[i + 1])
            if not m:
                print("--righe vuole un intervallo A-B")
                return 2
            rng = (int(m.group(1)), int(m.group(2)))
            i += 2
        elif a[i] == "--max" and i + 1 < len(a):
            massimo = int(a[i + 1])
            i += 2
        else:
            print(__doc__)
            return 2
    O = leggi(orig_p)
    R = leggi(riv_p)
    base = 1
    if rng:
        O = O[rng[0] - 1:rng[1]]
        base = rng[0]
        # il pezzo rivisto non ha righe vuote agli estremi: allinea togliendo quelle dell'originale
        while O and O[-1] == "":
            O.pop()
        while O and O[0] == "":
            O.pop(0)
            base += 1
    print(f"Originale: {orig_p}" + (f" (righe {rng[0]}-{rng[1]})" if rng else ""))
    print(f"Rivisto:   {riv_p}")
    if len(O) != len(R):
        print(f"\nDIFFERENZE: numero di righe diverso ({len(O)} nell'originale, {len(R)} nel rivisto).")
        print("Le versioni rivedute devono mantenere le righe allineate al sorgente.")
        return 1
    prot = protette(O)
    problemi, avvisi = [], []
    cambiate = 0
    for k, (x, y) in enumerate(zip(O, R)):
        n = base + k
        if x == y:
            continue
        cambiate += 1
        if prot[k]:
            problemi.append(f"riga {n}: riga protetta modificata. Prima: {x[:70]!r} Dopo: {y[:70]!r}")
            continue
        ix, iy = impronta(x), impronta(y)
        if ix != iy:
            d = []
            for key in sorted(set(ix) | set(iy)):
                if ix[key] != iy[key]:
                    d.append(f"{key.strip()[:60]}: {ix[key]} -> {iy[key]}")
            problemi.append(f"riga {n}: formattazione o caratteri speciali cambiati ({'; '.join(d[:4])})")
        nx, ny = numeri(x), numeri(y)
        if nx != ny:
            avvisi.append(f"riga {n}: numeri diversi ({dict(nx - ny)} -> {dict(ny - nx)})")
    print(f"Righe: {len(O)}; modificate: {cambiate}; protette identiche: "
          f"{sum(1 for k in range(len(O)) if prot[k] and O[k] == R[k])}")
    if avvisi:
        print(f"\nAvvisi ({len(avvisi)}, non bloccanti):")
        for v in avvisi[:massimo]:
            print("  -", v)
    if problemi:
        print(f"\nDIFFERENZE: {len(problemi)} righe con formattazione o caratteri alterati.")
        for v in problemi[:massimo]:
            print("  -", v)
        if len(problemi) > massimo:
            print(f"  ... e altre {len(problemi) - massimo}")
        return 1
    print("\nINTEGRO: righe protette identiche, marcatori e caratteri speciali invariati nelle righe di prosa modificate.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
