#!/usr/bin/env python3
"""Controlla in sola lettura il workspace condiviso fra Codex e Claude."""

from __future__ import annotations

import os
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
CORE_FILES = (
    "AGENTS.md",
    "CLAUDE.md",
    "PROJECT_GUIDE.md",
    ".agents/README.md",
    ".agents/skills/chiudi-fase/SKILL.md",
    ".agents/skills/verifica-workspace/SKILL.md",
    "input/README.md",
    "lavorazione/README.md",
    "output/README.md",
    "legacy/README.md",
    "test/README.md",
)
CORE_DIRECTORIES = ("input", "lavorazione", "output", "legacy", "test")
WRITING_SKILLS = (
    "italiano-scrittore",
    "italiano-verificatore",
    "italiano-stilista",
    "inglese-scrittore",
    "inglese-verificatore",
    "inglese-stilista",
    "inglese-confronto",
)


def main() -> int:
    problems: list[str] = []
    warnings: list[str] = []
    notes: list[str] = []

    for relative in CORE_FILES:
        if not (ROOT / relative).is_file():
            problems.append(f"file essenziale mancante: {relative}")

    for relative in CORE_DIRECTORIES:
        if not (ROOT / relative).is_dir():
            problems.append(f"directory essenziale mancante: {relative}/")

    link = ROOT / ".claude"
    if not link.is_symlink():
        problems.append(".claude non è un collegamento simbolico")
    elif os.readlink(link) != ".agents":
        problems.append(
            f".claude punta a {os.readlink(link)!r}, non al percorso relativo '.agents'"
        )
    else:
        notes.append("collegamento .claude -> .agents valido")

    guide = ROOT / "PROJECT_GUIDE.md"
    if guide.is_file():
        text = guide.read_text(encoding="utf-8")
        if "[NOME DEL PROGETTO]" in text:
            warnings.append("PROJECT_GUIDE.md contiene ancora i segnaposto del modello")

    optional = ROOT / "moduli-opzionali" / "scrittura"
    if optional.exists():
        expected = (
            optional / "README.md",
            optional / "scrittura-plugins",
            optional / "skills",
        )
        missing = [str(path.relative_to(ROOT)) for path in expected if not path.exists()]
        if missing:
            problems.append(
                "modulo di scrittura opzionale incompleto: " + ", ".join(missing)
            )
        else:
            notes.append("modulo di scrittura disponibile ma opzionale")
    else:
        notes.append("modulo di scrittura non incluso, condizione ammessa")

    active_plugins = ROOT / ".agents" / "scrittura-plugins"
    if active_plugins.exists():
        missing_skills = [
            name
            for name in WRITING_SKILLS
            if not (ROOT / ".agents" / "skills" / name / "SKILL.md").is_file()
        ]
        if missing_skills:
            problems.append(
                "attivazione del modulo di scrittura incompleta; skill mancanti: "
                + ", ".join(missing_skills)
            )
        else:
            notes.append("modulo di scrittura attivato")
    else:
        notes.append("modulo di scrittura non attivato")

    if problems:
        print("Verifica workspace fallita:")
        for problem in problems:
            print(f"- {problem}")
    else:
        print("Nucleo del workspace valido")

    for note in notes:
        print(f"- {note}")

    if warnings:
        print("Avvisi:")
        for warning in warnings:
            print(f"- {warning}")

    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
