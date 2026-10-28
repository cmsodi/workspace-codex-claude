#!/usr/bin/env python3
"""Genera gli entrypoint Codex dalle skill canoniche in .claude/skills."""

from __future__ import annotations

import argparse
import ast
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
CANONICAL_SKILLS = ROOT / ".claude" / "skills"
CODEX_SKILLS = ROOT / ".agents" / "skills"
GENERATOR_NAME = "genera-entrypoint-codex"
MARKER = "<!-- GENERATO DA genera-entrypoint-codex: NON MODIFICARE -->"
NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


class MetadataError(ValueError):
    """Metadati di una skill non utilizzabili per un entrypoint."""


def parse_scalar(value: str, field: str, source: Path) -> str:
    value = value.strip()
    if not value:
        raise MetadataError(f"{source}: valore {field!r} vuoto")
    if value[0] in {'"', "'"}:
        try:
            parsed = ast.literal_eval(value)
        except (SyntaxError, ValueError) as exc:
            raise MetadataError(
                f"{source}: valore {field!r} non valido"
            ) from exc
        if not isinstance(parsed, str):
            raise MetadataError(f"{source}: {field!r} deve essere testo")
        return parsed
    if value[0] in {"|", ">"}:
        raise MetadataError(
            f"{source}: {field!r} deve stare su una sola riga"
        )
    return value


def read_metadata(source: Path) -> tuple[str, str]:
    lines = source.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        raise MetadataError(f"{source}: frontmatter YAML mancante")
    try:
        end = next(
            index
            for index, line in enumerate(lines[1:], start=1)
            if line.strip() == "---"
        )
    except StopIteration as exc:
        raise MetadataError(f"{source}: frontmatter YAML non chiuso") from exc

    values: dict[str, str] = {}
    for line in lines[1:end]:
        if ":" not in line or line[:1].isspace():
            continue
        key, raw_value = line.split(":", 1)
        if key in {"name", "description"}:
            values[key] = parse_scalar(raw_value, key, source)

    missing = [field for field in ("name", "description") if field not in values]
    if missing:
        raise MetadataError(
            f"{source}: metadati mancanti: {', '.join(missing)}"
        )
    return values["name"], values["description"]


def render_entrypoint(name: str, description: str) -> str:
    quoted_description = json.dumps(description, ensure_ascii=False)
    canonical = f".claude/skills/{name}/SKILL.md"
    tick = chr(96)
    return (
        "---\n"
        f"name: {name}\n"
        f"description: {quoted_description}\n"
        "---\n\n"
        f"{MARKER}\n\n"
        "# Entrypoint Codex\n\n"
        f"Leggi integralmente {tick}{canonical}{tick} e applicane le istruzioni. "
        "Risolvi i percorsi relativi rispetto alla directory della skill "
        f"canonica sotto {tick}.claude/skills/{tick}.\n"
    )


def collect_expected() -> tuple[dict[str, str], list[str]]:
    expected: dict[str, str] = {}
    errors: list[str] = []
    if not CANONICAL_SKILLS.is_dir():
        return expected, [f"directory canonica mancante: {CANONICAL_SKILLS}"]

    for directory in sorted(CANONICAL_SKILLS.iterdir()):
        source = directory / "SKILL.md"
        if not directory.is_dir() or not source.is_file():
            continue
        try:
            name, description = read_metadata(source)
            if not NAME_PATTERN.fullmatch(name):
                raise MetadataError(f"{source}: nome skill non valido: {name!r}")
            if name != directory.name:
                raise MetadataError(
                    f"{source}: il nome {name!r} non coincide con "
                    f"la directory {directory.name!r}"
                )
            if name == GENERATOR_NAME:
                raise MetadataError(
                    f"{source}: il nome {GENERATOR_NAME!r} è riservato"
                )
            expected[name] = render_entrypoint(name, description)
        except (OSError, MetadataError) as exc:
            errors.append(str(exc))
    return expected, errors


def read_generated(path: Path) -> str | None:
    if not path.is_file():
        return None
    text = path.read_text(encoding="utf-8")
    return text if MARKER in text else None


def plan_changes(
    expected: dict[str, str],
) -> tuple[list[str], list[str], list[str], list[str]]:
    create: list[str] = []
    update: list[str] = []
    remove: list[str] = []
    errors: list[str] = []

    for name, content in expected.items():
        target = CODEX_SKILLS / name / "SKILL.md"
        if not target.exists():
            if target.parent.exists() and any(target.parent.iterdir()):
                errors.append(
                    "non sovrascrivo la directory non generata: "
                    f"{target.parent.relative_to(ROOT)}"
                )
            else:
                create.append(name)
            continue
        existing = read_generated(target)
        if existing is None:
            errors.append(
                f"non sovrascrivo l'entrypoint manuale: {target.relative_to(ROOT)}"
            )
        elif existing != content:
            update.append(name)

    if CODEX_SKILLS.is_dir():
        for directory in sorted(CODEX_SKILLS.iterdir()):
            if not directory.is_dir() or directory.name == GENERATOR_NAME:
                continue
            target = directory / "SKILL.md"
            if directory.name not in expected and read_generated(target) is not None:
                remove.append(directory.name)

    return create, update, remove, errors


def apply_changes(
    expected: dict[str, str],
    create: list[str],
    update: list[str],
    remove: list[str],
) -> None:
    for name in create + update:
        target = CODEX_SKILLS / name / "SKILL.md"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(expected[name], encoding="utf-8")

    for name in remove:
        directory = CODEX_SKILLS / name
        target = directory / "SKILL.md"
        target.unlink()
        try:
            directory.rmdir()
        except OSError:
            pass


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Allinea gli entrypoint Codex alle skill in .claude/skills."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="controlla senza modificare file",
    )
    args = parser.parse_args()

    if CODEX_SKILLS.is_symlink():
        print("Errore: .agents/skills deve essere una directory reale")
        return 1
    if not CODEX_SKILLS.is_dir():
        if args.check:
            print("Entrypoint Codex non allineati:")
            print("- directory .agents/skills mancante")
            return 1
        CODEX_SKILLS.mkdir(parents=True, exist_ok=True)

    expected, metadata_errors = collect_expected()
    create, update, remove, conflicts = plan_changes(expected)
    errors = metadata_errors + conflicts
    if errors:
        print("Generazione non eseguita:")
        for error in errors:
            print(f"- {error}")
        return 1

    if args.check:
        if create or update or remove:
            print("Entrypoint Codex non allineati:")
            for action, names in (
                ("da creare", create),
                ("da aggiornare", update),
                ("da rimuovere", remove),
            ):
                if names:
                    print(f"- {action}: {', '.join(names)}")
            return 1
        print(f"Entrypoint Codex allineati: {len(expected)}")
        return 0

    apply_changes(expected, create, update, remove)
    print(
        "Entrypoint Codex: "
        f"{len(create)} creati, {len(update)} aggiornati, "
        f"{len(remove)} rimossi, {len(expected)} totali"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
