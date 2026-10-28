#!/usr/bin/env python3
"""Verifica la struttura essenziale del workspace condiviso."""

from __future__ import annotations

import os
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = (
    "AGENTS.md",
    "CLAUDE.md",
    "PROJECT_GUIDE.md",
    ".agents/README.md",
    ".agents/skills/chiudi-fase/SKILL.md",
)
REQUIRED_DIRECTORIES = (
    "input",
    "lavorazione",
    "output",
    "legacy",
    "test",
    "moduli-opzionali/scrittura",
)


def main() -> int:
    problems: list[str] = []

    for relative in REQUIRED_FILES:
        if not (ROOT / relative).is_file():
            problems.append(f"file mancante: {relative}")

    for relative in REQUIRED_DIRECTORIES:
        if not (ROOT / relative).is_dir():
            problems.append(f"directory mancante: {relative}")

    link = ROOT / ".claude"
    if not link.is_symlink():
        problems.append(".claude non è un collegamento simbolico")
    elif os.readlink(link) != ".agents":
        problems.append(f".claude punta a {os.readlink(link)!r}, non a '.agents'")

    if problems:
        print("Verifica fallita:")
        for problem in problems:
            print(f"- {problem}")
        return 1

    print("Struttura valida: workspace condiviso pronto")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
