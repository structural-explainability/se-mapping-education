"""validate.py - Shared validation utilities for SE education mapping repositories."""

from pathlib import Path
import sys
import tomllib
from typing import Any, cast

from se_mapping_education.constants import ALLOWED_METHODS, ALLOWED_RELATIONS

PROJECT_ROOT = Path.cwd()
DATA_DIR = PROJECT_ROOT / "data"
MAPPINGS_DIR = DATA_DIR / "mappings"

REQUIRED_ALIGNMENT_FIELDS = [
    "source_id",
    "target_id",
    "relation",
    "confidence",
    "method",
    "human_validated",
]


def load_toml(path: Path) -> dict[str, Any]:
    """Load a TOML file."""
    with path.open("rb") as file:
        return tomllib.load(file)


def validate_alignment(path: Path, index: int, alignment: object) -> list[str]:
    """Validate one [[alignment]] item."""
    if not isinstance(alignment, dict):
        return [f"{path}: alignment #{index} must be a table."]

    errors: list[str] = []
    alignment_dict = cast(dict[str, object], alignment)

    for field in REQUIRED_ALIGNMENT_FIELDS:
        if field not in alignment_dict:
            errors.append(f"{path}: alignment #{index} missing {field!r}.")

    source_id = alignment_dict.get("source_id")
    if "source_id" in alignment_dict and not isinstance(source_id, str):
        errors.append(f"{path}: alignment #{index} source_id must be a string.")
    elif isinstance(source_id, str) and not source_id.strip():
        errors.append(f"{path}: alignment #{index} source_id must not be empty.")

    target_id = alignment_dict.get("target_id")
    if "target_id" in alignment_dict and not isinstance(target_id, str):
        errors.append(f"{path}: alignment #{index} target_id must be a string.")
    elif isinstance(target_id, str) and not target_id.strip():
        errors.append(f"{path}: alignment #{index} target_id must not be empty.")

    relation = alignment_dict.get("relation")
    if "relation" in alignment_dict and not isinstance(relation, str):
        errors.append(f"{path}: alignment #{index} relation must be a string.")
    elif isinstance(relation, str) and relation not in ALLOWED_RELATIONS:
        allowed = ", ".join(sorted(ALLOWED_RELATIONS))
        errors.append(
            f"{path}: alignment #{index} relation {relation!r} is invalid; "
            f"allowed: {allowed}."
        )

    confidence = alignment_dict.get("confidence")
    if "confidence" in alignment_dict and not isinstance(confidence, int | float):
        errors.append(f"{path}: alignment #{index} confidence must be numeric.")
    elif isinstance(confidence, int | float) and not 0 <= float(confidence) <= 1:
        errors.append(f"{path}: alignment #{index} confidence must be between 0 and 1.")

    method = alignment_dict.get("method")
    if "method" in alignment_dict and not isinstance(method, str):
        errors.append(f"{path}: alignment #{index} method must be a string.")
    elif isinstance(method, str) and method not in ALLOWED_METHODS:
        allowed = ", ".join(sorted(ALLOWED_METHODS))
        errors.append(
            f"{path}: alignment #{index} method {method!r} is invalid; "
            f"allowed: {allowed}."
        )

    human_validated = alignment_dict.get("human_validated")
    if "human_validated" in alignment_dict and not isinstance(human_validated, bool):
        errors.append(f"{path}: alignment #{index} human_validated must be a boolean.")

    return errors


def validate_mapping_file(path: Path) -> list[str]:
    """Validate one mapping TOML file."""
    try:
        data = load_toml(path)
    except tomllib.TOMLDecodeError as exc:
        return [f"{path}: invalid TOML: {exc}"]
    except OSError as exc:
        return [f"{path}: could not read file: {exc}"]

    alignments = data.get("alignment")
    if alignments is None:
        return [f"{path}: missing [[alignment]] entries."]

    if not isinstance(alignments, list):
        return [f"{path}: alignment must be an array of tables."]

    errors: list[str] = []

    if not alignments:
        errors.append(f"{path}: alignment list must not be empty.")

    for index, raw in enumerate(cast(list[object], alignments), start=1):
        errors.extend(validate_alignment(path, index, raw))

    return errors


def validate_acu_order(path: Path, data: dict[str, Any]) -> list[str]:
    """Validate ordering and uniqueness of ACU identifiers."""
    errors: list[str] = []

    raw_acus = data.get("acu")
    if not isinstance(raw_acus, list):
        return errors

    acus = cast(list[object], raw_acus)
    ids: list[str] = []

    for item in acus:
        if isinstance(item, dict):
            acu_id = cast(dict[str, object], item).get("id")
            if isinstance(acu_id, str):
                ids.append(acu_id)

    if ids != sorted(ids):
        errors.append(f"{path}: ACU ids must be sorted alphabetically.")

    if len(ids) != len(set(ids)):
        errors.append(f"{path}: duplicate ACU ids detected.")

    return errors


def validate_nor_file(path: Path) -> list[str]:
    """Validate one NOR TOML file."""
    try:
        data = load_toml(path)
    except tomllib.TOMLDecodeError as exc:
        return [f"{path}: invalid TOML: {exc}"]
    except OSError as exc:
        return [f"{path}: could not read file: {exc}"]

    return validate_acu_order(path, data)


def validate_all(project_root: Path | None = None) -> list[str]:
    """Validate mapping and NOR TOML files in a repository."""
    root = project_root or PROJECT_ROOT
    data_dir = root / "data"
    mappings_dir = data_dir / "mappings"
    nor_dir = data_dir / "nor"

    errors: list[str] = []

    if mappings_dir.exists():
        for path in sorted(mappings_dir.rglob("*.toml")):
            errors.extend(validate_mapping_file(path))

    if nor_dir.exists():
        for path in sorted(nor_dir.rglob("*.toml")):
            errors.extend(validate_nor_file(path))

    if not mappings_dir.exists() and not nor_dir.exists():
        errors.append(f"{data_dir}: no mappings or NOR directory found.")

    return errors


def run_validate() -> int:
    """Run validation and return a process exit code."""
    errors = validate_all()

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("Mapping validation passed.")
    return 0
