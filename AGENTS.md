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

