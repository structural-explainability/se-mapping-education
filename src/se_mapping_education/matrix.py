"""matrix.py - Shared coverage matrix utilities for SE education mapping repositories."""

from dataclasses import dataclass
from pathlib import Path
import tomllib
from typing import Any, cast

PROJECT_ROOT = Path.cwd()
MAPPINGS_DIR = PROJECT_ROOT / "data" / "mappings"
DOCS_MATRIX_PATH = PROJECT_ROOT / "docs" / "en" / "coverage-matrix.md"

SOURCE_ORDER = [
    "NAEP",
    "CCSS",
    "MN",
    "NY",
    "PISA",
    "SG",
    "FI",
    "NO",
    "NOR",
]


@dataclass(frozen=True)
class AlignmentRow:
    """One alignment row for matrix generation."""

    source_system: str
    target_id: str
    relation: str


def load_toml(path: Path) -> dict[str, Any]:
    """Load a TOML file."""
    with path.open("rb") as file:
        return tomllib.load(file)


def source_system_from_id(source_id: str) -> str:
    """Infer the source system from the first source_id segment."""
    return source_id.split(".", maxsplit=1)[0].upper()


def relation_label(relation: str) -> str:
    """Return display label for a relation."""
    labels = {
        "equivalent": "yes",
        "none": "-",
    }
    return labels.get(relation, relation)


def sort_source_systems(source_systems: set[str]) -> list[str]:
    """Sort source systems using preferred order, then alphabetical fallback."""
    preferred = [source for source in SOURCE_ORDER if source in source_systems]
    remaining = sorted(source_systems - set(SOURCE_ORDER))
    return preferred + remaining


def collect_rows(mappings_dir: Path = MAPPINGS_DIR) -> list[AlignmentRow]:
    """Collect alignment rows from mapping TOML files."""
    rows: list[AlignmentRow] = []

    if not mappings_dir.exists():
        return rows

    for path in sorted(mappings_dir.rglob("*.toml")):
        data = load_toml(path)
        alignments = data.get("alignment", [])

        if not isinstance(alignments, list):
            continue

        for raw in cast(list[object], alignments):
            if not isinstance(raw, dict):
                continue

            alignment = cast(dict[str, object], raw)
            source_id = alignment.get("source_id")
            target_id = alignment.get("target_id")
            relation = alignment.get("relation")

            if not isinstance(source_id, str):
                continue
            if not isinstance(target_id, str):
                continue
            if not isinstance(relation, str):
                continue

            rows.append(
                AlignmentRow(
                    source_system=source_system_from_id(source_id),
                    target_id=target_id,
                    relation=relation,
                )
            )

    return rows


def build_matrix(rows: list[AlignmentRow]) -> dict[str, dict[str, str]]:
    """Build target_id by source-system coverage matrix."""
    target_ids = sorted({row.target_id for row in rows})
    source_systems = sort_source_systems({row.source_system for row in rows})

    return {
        target_id: {
            source_system: next(
                (
                    relation_label(row.relation)
                    for row in rows
                    if row.target_id == target_id and row.source_system == source_system
                ),
                "-",
            )
            for source_system in source_systems
        }
        for target_id in target_ids
    }


def render_markdown(matrix: dict[str, dict[str, str]]) -> str:
    """Render coverage matrix as Markdown."""
    if not matrix:
        return "# Coverage Matrix\n\nNo mappings found.\n"

    source_systems = list(next(iter(matrix.values())).keys())

    lines = [
        "# Coverage Matrix",
        "",
        "This matrix is a draft structural coverage artifact. "
        "It shows declared mapping relations between source systems and NOR targets. "
        "It does not evaluate curriculum quality, instructional effectiveness, or student performance.",
        "",
        "| NOR Target | " + " | ".join(source_systems) + " |",
        "|---|" + "|".join("---" for _ in source_systems) + "|",
    ]

    for target_id, coverage in sorted(matrix.items()):
        values = [coverage[source_system] for source_system in source_systems]
        lines.append("| " + target_id + " | " + " | ".join(values) + " |")

    lines.append("")
    return "\n".join(lines)


def build_coverage_matrix(
    mappings_dir: Path = MAPPINGS_DIR,
    output_path: Path = DOCS_MATRIX_PATH,
) -> Path:
    """Build and write the coverage matrix."""
    rows = collect_rows(mappings_dir)
    matrix = build_matrix(rows)
    markdown = render_markdown(matrix)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(markdown, encoding="utf-8")

    return output_path


def run_matrix() -> int:
    """Build matrix and return a process exit code."""
    output_path = build_coverage_matrix()
    print(f"Wrote coverage matrix: {output_path}")
    return 0
