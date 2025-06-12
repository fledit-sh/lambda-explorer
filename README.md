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

`lambda-explorer` can also be used programmatically. Formula classes are
available in `lambda_explorer.tools.aero_formulas` and provide a convenient
`solve()` method. Exactly one variable must be omitted so that it can be
calculated:

```python
from lambda_explorer.tools.aero_formulas import ReynoldsNumber

eq = ReynoldsNumber()
# Solve for Re while providing the other values
re = eq.solve(rho=1.225, V=50.0, c=0.5, mu=1.8e-5)
print(re)
```

To launch the GUI from Python simply call `lambda_explorer.main()`:

```python
from lambda_explorer import main

main()
```

Default values used inside the GUI can be customised. Use the *Defaults* tab in
any formula window to load or save the `defaults.yaml` file directly, or choose
"Save As" to export the defaults to a custom YAML file. The defaults map
variable names to their stored string values.
