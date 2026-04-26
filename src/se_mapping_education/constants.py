"""constants.py - Shared constants for SE education mapping repositories.

Keep aligned with
se-mapspec/data/alignment/alignment-schema.toml.
"""

ALLOWED_RELATIONS: frozenset[str] = frozenset(
    {
        "equivalent",
        "narrower",
        "broader",
        "overlaps",
        "none",
    }
)

ALLOWED_METHODS: frozenset[str] = frozenset(
    {
        "manual",
        "expert_review",
        "llm_assisted",
        "rule_based",
        "imported",
    }
)

DEFAULT_DATA_DIR = "data"
DEFAULT_MAPPINGS_DIR = "data/mappings"
DEFAULT_MATRIX_OUTPUT = "docs/en/coverage-matrix.md"
