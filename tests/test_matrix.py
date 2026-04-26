# tests/test_matrix_coverage.py
"""Targeted tests for matrix.py lines not hit by test_matrix.py."""

from pathlib import Path
from unittest.mock import patch

from se_mapping_education.matrix import (
    build_coverage_matrix,
    collect_rows,
    run_matrix,
    sort_source_systems,
)


def _write_toml(path: Path, content: str) -> Path:
    path.write_text(content, encoding="utf-8")
    return path


# --- sort_source_systems: unknown systems fall through to alphabetical ---


def test_sort_source_systems_unknown_appended_alphabetically():
    result = sort_source_systems({"NAEP", "ZZFOO", "AAFOO"})
    naep_pos = result.index("NAEP")
    aa_pos = result.index("AAFOO")
    zz_pos = result.index("ZZFOO")
    assert naep_pos < aa_pos < zz_pos


def test_sort_source_systems_all_unknown():
    result = sort_source_systems({"ZZZ", "AAA", "MMM"})
    assert result == ["AAA", "MMM", "ZZZ"]


# --- collect_rows: skips entries missing required string fields ---


def test_collect_rows_skips_non_string_source_id(tmp_path: Path):
    _write_toml(
        tmp_path / "bad.toml",
        """
[[alignment]]
source_id = 42
target_id = "nor.math.g8.mean"
relation = "overlaps"
confidence = 0.80
method = "expert_review"
human_validated = false
""",
    )
    rows = collect_rows(tmp_path)
    assert rows == []


def test_collect_rows_skips_non_string_target_id(tmp_path: Path):
    _write_toml(
        tmp_path / "bad.toml",
        """
[[alignment]]
source_id = "NAEP.Math.G8.Foo"
target_id = 99
relation = "overlaps"
confidence = 0.80
method = "expert_review"
human_validated = false
""",
    )
    rows = collect_rows(tmp_path)
    assert rows == []


def test_collect_rows_skips_non_string_relation(tmp_path: Path):
    _write_toml(
        tmp_path / "bad.toml",
        """
[[alignment]]
source_id = "NAEP.Math.G8.Foo"
target_id = "nor.math.g8.mean"
relation = 0
confidence = 0.80
method = "expert_review"
human_validated = false
""",
    )
    rows = collect_rows(tmp_path)
    assert rows == []


# --- build_coverage_matrix and run_matrix ---


def test_build_coverage_matrix_writes_file(tmp_path: Path):
    mappings = tmp_path / "mappings"
    mappings.mkdir()
    _write_toml(
        mappings / "m.toml",
        """
[[alignment]]
source_id = "NAEP.Math.G8.Foo"
target_id = "nor.math.g8.mean"
relation = "overlaps"
confidence = 0.80
method = "expert_review"
human_validated = false
""",
    )
    output = tmp_path / "out" / "matrix.md"
    result = build_coverage_matrix(mappings_dir=mappings, output_path=output)
    assert result == output
    assert output.exists()
    content = output.read_text(encoding="utf-8")
    assert "nor.math.g8.mean" in content


def test_run_matrix_returns_zero(tmp_path: Path):
    mappings = tmp_path / "mappings"
    mappings.mkdir()
    _write_toml(
        mappings / "m.toml",
        """
[[alignment]]
source_id = "NAEP.Math.G8.Foo"
target_id = "nor.math.g8.mean"
relation = "overlaps"
confidence = 0.80
method = "expert_review"
human_validated = false
""",
    )
    output = tmp_path / "out" / "matrix.md"
    with (
        patch("se_mapping_education.matrix.MAPPINGS_DIR", mappings),
        patch("se_mapping_education.matrix.DOCS_MATRIX_PATH", output),
    ):
        result = run_matrix()
    assert result == 0
