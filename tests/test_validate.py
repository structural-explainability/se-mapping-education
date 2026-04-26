# tests/test_validate_coverage.py
"""Targeted tests for validate.py lines not hit by test_validate.py."""

from pathlib import Path
from unittest.mock import patch

from se_mapping_education.validate import (
    run_validate,
    validate_acu_order,
    validate_alignment,
    validate_all,
)

VALID_ALIGNMENT = {
    "source_id": "NAEP.Math.G8.Statistics.DescribeData",
    "target_id": "nor.math.g8.compute_mean",
    "relation": "overlaps",
    "confidence": 0.80,
    "method": "expert_review",
    "human_validated": False,
}


def _write_toml(path: Path, content: str) -> Path:
    path.write_text(content, encoding="utf-8")
    return path


# --- field type errors (non-string values for string fields) ---


def test_source_id_not_string():
    alignment = {**VALID_ALIGNMENT, "source_id": 42}
    errors = validate_alignment(Path("t.toml"), 1, alignment)
    assert any("source_id" in e and "string" in e for e in errors)


def test_target_id_not_string():
    alignment = {**VALID_ALIGNMENT, "target_id": 99}
    errors = validate_alignment(Path("t.toml"), 1, alignment)
    assert any("target_id" in e and "string" in e for e in errors)


def test_empty_target_id():
    alignment = {**VALID_ALIGNMENT, "target_id": "  "}
    errors = validate_alignment(Path("t.toml"), 1, alignment)
    assert any("target_id" in e for e in errors)


def test_relation_not_string():
    alignment = {**VALID_ALIGNMENT, "relation": 0}
    errors = validate_alignment(Path("t.toml"), 1, alignment)
    assert any("relation" in e and "string" in e for e in errors)


def test_confidence_not_numeric():
    alignment = {**VALID_ALIGNMENT, "confidence": "high"}
    errors = validate_alignment(Path("t.toml"), 1, alignment)
    assert any("confidence" in e and "numeric" in e for e in errors)


def test_method_not_string():
    alignment = {**VALID_ALIGNMENT, "method": True}
    errors = validate_alignment(Path("t.toml"), 1, alignment)
    assert any("method" in e and "string" in e for e in errors)


# --- validate_acu_order ---


def test_acu_order_valid(tmp_path: Path):
    f = _write_toml(
        tmp_path / "ok.toml",
        """
[[acu]]
id = "acu.alpha"

[[acu]]
id = "acu.beta"
""",
    )
    import tomllib

    with f.open("rb") as fh:
        data = tomllib.load(fh)
    errors = validate_acu_order(f, data)
    assert errors == []


def test_acu_order_unsorted(tmp_path: Path):
    f = _write_toml(
        tmp_path / "unsorted.toml",
        """
[[acu]]
id = "acu.z"

[[acu]]
id = "acu.a"
""",
    )
    import tomllib

    with f.open("rb") as fh:
        data = tomllib.load(fh)
    errors = validate_acu_order(f, data)
    assert any("sorted" in e for e in errors)


def test_acu_order_duplicates(tmp_path: Path):
    f = _write_toml(
        tmp_path / "dupe.toml",
        """
[[acu]]
id = "acu.a"

[[acu]]
id = "acu.a"
""",
    )
    import tomllib

    with f.open("rb") as fh:
        data = tomllib.load(fh)
    errors = validate_acu_order(f, data)
    assert any("duplicate" in e for e in errors)


def test_acu_order_no_acu_key(tmp_path: Path):
    f = _write_toml(tmp_path / "no_acu.toml", '[mapping]\nid = "x"\n')
    import tomllib

    with f.open("rb") as fh:
        data = tomllib.load(fh)
    errors = validate_acu_order(f, data)
    assert errors == []


# --- validate_all ---


def test_validate_all_missing_directory():
    errors = validate_all(Path("/nonexistent/path"))
    assert any("does not exist" in e or "no mappings" in e for e in errors)


def test_validate_all_empty_directory(tmp_path: Path):
    errors = validate_all(tmp_path)
    assert any("no mappings" in e for e in errors)


def test_validate_all_valid_file(tmp_path: Path):
    mappings = tmp_path / "data" / "mappings"
    mappings.mkdir(parents=True)
    _write_toml(
        mappings / "good.toml",
        """
[[alignment]]
source_id = "NAEP.Math.G8.Algebra.Alg4"
target_id = "nor.math.g8.linear_equations"
relation = "equivalent"
confidence = 0.90
method = "expert_review"
human_validated = false
""",
    )
    errors = validate_all(tmp_path)
    assert errors == []


def test_validate_all_invalid_file_included(tmp_path: Path):
    _write_toml(tmp_path / "bad.toml", '[mapping]\nid = "x"\n')
    errors = validate_all(tmp_path)
    assert len(errors) > 0


# --- run_validate ---


def test_run_validate_passes(tmp_path: Path):
    mappings = tmp_path / "data" / "mappings"
    mappings.mkdir(parents=True)
    _write_toml(
        mappings / "good.toml",
        """
[[alignment]]
source_id = "NAEP.Math.G8.Algebra.Alg4"
target_id = "nor.math.g8.linear_equations"
relation = "equivalent"
confidence = 0.90
method = "expert_review"
human_validated = false
""",
    )
    with patch("se_mapping_education.validate.PROJECT_ROOT", tmp_path):
        result = run_validate()
    assert result == 0
