# se-mapping-education

[![Docs Site](https://img.shields.io/badge/docs-site-blue?logo=github)](https://structural-explainability.github.io/se-mapping-education/)
[![Repo](https://img.shields.io/badge/repo-GitHub-black?logo=github)](https://github.com/structural-explainability/se-mapping-education)
[![Python 3.15+](https://img.shields.io/badge/python-3.15%2B-blue?logo=python)](./pyproject.toml)
[![License](https://img.shields.io/badge/license-MIT-yellow.svg)](./LICENSE)

[![CI](https://github.com/structural-explainability/se-mapping-education/actions/workflows/ci-python-zensical.yml/badge.svg?branch=main)](https://github.com/structural-explainability/se-mapping-education/actions/workflows/ci-python-zensical.yml)
[![Docs](https://github.com/structural-explainability/se-mapping-education/actions/workflows/deploy-zensical.yml/badge.svg?branch=main)](https://github.com/structural-explainability/se-mapping-education/actions/workflows/deploy-zensical.yml)
[![Links](https://github.com/structural-explainability/se-mapping-education/actions/workflows/links.yml/badge.svg?branch=main)](https://github.com/structural-explainability/se-mapping-education/actions/workflows/links.yml)

# Structural Explainability Mapping: Education

> Bounded education-domain conformance examples for Structural Explainability mapping rules.

Mapping example repositories include minimal `ctx` declarations sufficient for
self-contained validation and traceability.
These declarations identify external
systems and do not constitute full source registries.

## Owns

- education-domain mapping examples
- cross-system education reference contexts
- conformance examples for education standards alignment

## Includes

### Education contexts

- NAEP
- CCSS
- PISA
- selected national or jurisdictional education systems

### Mapping examples

- source-to-reference alignments
- cross-system comparison examples

### Validation support

- mapping schema checks
- relation checks
- context checks (not yet implemented)

## Does Not Include

- source registries
- dashboards
- analytics applications
- policy interpretation
- claims about educational quality

## Relationship to Implementations

This repository defines the education-domain boundary for mapping examples.

Concrete implementations live in downstream mapping repositories, including:

- [se-mapping-education-math](https://github.com/structural-explainability/se-mapping-education-math)
- [se-mapping-education-math-g8](https://github.com/structural-explainability/se-mapping-education-math-g8)

## Command Reference

<details>
<summary>Show command reference</summary>

### In a machine terminal

After you get a copy of this repo in your own GitHub account,
open a machine terminal in `Repos` or where you want the project:

```shell
# Replace username with YOUR GitHub username.
git clone https://github.com/username/se-mapping-education

cd se-mapping-education
code .
```

### In a VS Code terminal

```shell
uv self update
uv python pin 3.15
uv sync --extra dev --extra docs --upgrade

uvx pre-commit install

git add -A
uvx pre-commit run --all-files
# repeat if changes were made
git add -A
uvx pre-commit run --all-files

# run
uv run python -m se_mapping_education sort
uv run python -m se_mapping_education validate
uv run python -m se_mapping_education matrix

# child repos use the same commands with their own module name
# uv run python -m se_mapping_education_math validate
# uv run python -m se_mapping_education_math_g8 validate

# do chores
npx markdownlint-cli "**/*.md" --fix
uv run python -m ruff format .
uv run python -m ruff check . --fix
uv run python -m pyright
uv run python -m pytest
uv run python -m zensical build

# save progress
git add -A
git commit -m "update"
git push -u origin main
```

</details>

## Citation

[CITATION.cff](./CITATION.cff)

## License

[LICENSE](./LICENSE)

## Manifest

[SE_MANIFEST.toml](./SE_MANIFEST.toml)
