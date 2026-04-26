# tests/test_sort_coverage.py
"""Targeted tests for sort.py lines not hit by test_sort.py."""

from pathlib import Path
from unittest.mock import patch

from se_mapping_education.sort import run_sort


def _write_toml(path: Path, content: str) -> Path:
    path.write_text(content, encoding="utf-8")
    return path


def test_run_sort_no_changes(tmp_path: Path):
    _write_toml(
        tmp_path / "sorted.toml",
        """
[[acu]]
id = "acu.a"

[[acu]]
id = "acu.b"
""",
    )
    with patch("se_mapping_education.sort.DATA_DIR", tmp_path):
        result = run_sort()
    assert result == 0


def test_run_sort_with_changes(tmp_path: Path):
    _write_toml(
        tmp_path / "unsorted.toml",
        """
[[acu]]
id = "acu.z"

[[acu]]
id = "acu.a"
""",
    )
    with patch("se_mapping_education.sort.DATA_DIR", tmp_path):
        result = run_sort()
    assert result == 0
    content = (tmp_path / "unsorted.toml").read_text(encoding="utf-8")
    assert content.index("acu.a") < content.index("acu.z")


def test_run_sort_skips_invalid_toml(tmp_path: Path):
    _write_toml(tmp_path / "broken.toml", "[[acu]\n")
    with patch("se_mapping_education.sort.DATA_DIR", tmp_path):
        result = run_sort()
    assert result == 0
