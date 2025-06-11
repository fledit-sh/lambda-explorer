# Lambda Explorer

A small GUI application for interacting with symbolic formulas and plotting them using [Dear PyGui](https://github.com/hoffstadt/dearpygui).

## Installation

```bash
pip install lambda-explorer
```

To install from source:

```bash
pip install -r requirements.txt
pip install -e .
```

## Usage

After installation you can launch the application with the command:

```bash
lambda-explorer
```

This will open the formula browser where you can calculate and visualize formulas.

## Library Usage

`lambda-explorer` can also be used programmatically. All formula classes are
available in `lambda_explorer.tools.aero_tools` and provide a convenient
`solve()` method. Exactly one variable must be omitted so that it can be
calculated:

```python
from lambda_explorer.tools.aero_tools import IdealeGasGleichung

eq = IdealeGasGleichung()
# Solve for n while providing the other values
mol = eq.solve(P=101325, V=1.0, R=8.314, T=300)
print(mol)
```

To launch the GUI from Python simply call `lambda_explorer.aero.main()`:

```python
from lambda_explorer.aero import main

main()
```

Default values used inside the GUI can be customised. Export the current
defaults from the settings window or create a `defaults.json` file in the
working directory with a mapping from variable names to their default string
value.
