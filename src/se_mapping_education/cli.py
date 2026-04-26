"""Command-line interface for SE mapping examples."""

import sys

from se_mapping_education.matrix import run_matrix
from se_mapping_education.sort import run_sort
from se_mapping_education.validate import run_validate


def main(argv: list[str] | None = None) -> int:
    """Entry point for CLI commands."""
    if argv is None:
        argv = sys.argv[1:]

    if not argv:
        print("Usage: python -m se_mapping_education <command>")
        print("Commands: validate, matrix, sort")
        return 1

    command = argv[0]

    if command == "matrix":
        return run_matrix()

    if command == "sort":
        return run_sort()

    if command == "validate":
        return run_validate()

    print(f"Unknown command: {command}")
    return 1
