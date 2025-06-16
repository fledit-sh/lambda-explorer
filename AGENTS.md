# AGENTS Instructions for Lambda Explorer

This repository contains `lambda-explorer`, a GUI and CLI for solving and visualising symbolic formulas with SymPy and Dear PyGui.

## General Guidelines

* Use **Python 3.8+** features such as type hints and data classes where helpful.
* Follow **PEP 8** style with an 88 character line limit. Indent using 4 spaces.
* Document public functions, classes and formulas using docstrings. Include a short
  description and explain each parameter.
* Keep imports ordered (standard library, third party, local). Avoid unused
  imports and variables.
* Do not commit files under `build/` or `lambda_explorer.egg-info/`.

## Repository Structure

* `lambda_explorer/` – Package source code, including CLI entry points and GUI tools.
* `docs/` – Documentation such as the developer guide for creating new formulas.
* `defaults.yaml` – Default values used by the GUI.
* `layout.ini` – Window layout saved between runs.

## Development Workflow

1. Install the project in editable mode:

   ```bash
   pip install -e .
   ```

2. Run the application to ensure it launches correctly. It will open the GUI;
   you can close it immediately once you see the log output:

   ```bash
   lambda-explorer
   ```

3. If a `tests/` folder exists, run the test suite with `pytest`.

## Formula Implementation

When adding new formulas, subclass
`lambda_explorer.tools.formula_base.Formula` as described in
`docs/developer_guide.md`. Ensure that each formula class defines
`variables` and initialises the symbolic equation in `__init__`.

## Commit Messages

Use concise commit messages in the present tense (e.g. "Add new formula" or
"Fix GUI crash"). Group related changes into a single commit when possible.

## Pull Request Notes

When opening a pull request, summarise the changes and mention any tests that
were run. If you add new dependencies, explain why they are required.

## Semantic Versioning Policy (MAJOR.MINOR.PATCH)
The file lambda_explorer/__version__.py defines the current version.
Every change to the codebase must be reflected by incrementing one part of the version number according to the following rules:

### MAJOR (X.0.0)
Increment if:
- Incompatible API changes are made
- Public interfaces or formulas are removed or renamed
- Existing results or GUI behavior change in backward-incompatible ways

### MINOR (0.X.0)
Increment if:
- New features or formulas are added in a backward-compatible way
- New CLI commands, GUI tools, or plotting features are introduced

### PATCH (0.0.X)
Increment if:
- Bugs are fixed
- Documentation is updated
- Internal improvements or refactorings are made with no functional change
- GUI layout or styling is adjusted without changing behavior

### Codex Rule (Auto-Applied)
Every commit or pull request must be accompanied by one of the following version tags in the commit message:

- [version:major]
- [version:minor]
- [version:patch]

Codex or CI scripts must automatically bump the version accordingly in __version__.py.