# tests/test_sort.py

from pathlib import Path

import se_mapping_education.sort


def _write_toml(path: Path, content: str) -> Path:
    path.write_text(content, encoding="utf-8")
    return path


def test_sort_acu_already_sorted_returns_false():
    data = {"acu": [{"id": "acu.a"}, {"id": "acu.b"}]}
    assert se_mapping_education.sort.sort_acu(data) is False


def test_sort_acu_unsorted_returns_true_and_sorts():
    data = {"acu": [{"id": "acu.z"}, {"id": "acu.a"}]}
    changed = se_mapping_education.sort.sort_acu(data)
    assert changed is True
    assert data["acu"][0]["id"] == "acu.a"
    assert data["acu"][1]["id"] == "acu.z"


def test_sort_acu_no_acu_key_returns_false():
    data: dict[str, list[dict[str, str]]] = {}
    assert se_mapping_education.sort.sort_acu(data) is False


def test_sort_acu_not_list_returns_false():
    data = {"acu": "not a list"}
    assert se_mapping_education.sort.sort_acu(data) is False


def test_sort_file_unsorted_writes_sorted(tmp_path: Path):
    f = _write_toml(
        tmp_path / "acus.toml",
        """
[[acu]]
id = "acu.z"

[[acu]]
id = "acu.a"
""",
    )
    changed = se_mapping_education.sort.sort_file(f)
    assert changed is True
    content = f.read_text(encoding="utf-8")
    assert content.index("acu.a") < content.index("acu.z")


def test_sort_file_already_sorted_not_rewritten(tmp_path: Path):
    f = _write_toml(
        tmp_path / "acus.toml",
        """
[[acu]]
id = "acu.a"

[[acu]]
id = "acu.z"
""",
    )
    changed = se_mapping_education.sort.sort_file(f)
    assert changed is False


def test_sort_file_invalid_toml_returns_false(tmp_path: Path):
    f = _write_toml(tmp_path / "broken.toml", "[[acu]\n")
    assert se_mapping_education.sort.sort_file(f) is False


def test_sort_file_no_acu_section_returns_false(tmp_path: Path):
    f = _write_toml(tmp_path / "no_acu.toml", '[mapping]\nid = "x"\n')
    assert se_mapping_education.sort.sort_file(f) is False
