# Developer Guide: Adding New Formulas

This project uses **SymPy** to define symbolic equations that can be solved and
visualised inside the GUI. Each formula is implemented as a subclass of
`lambda_explorer.tools.formula_base.Formula`. When a module defining new
formulas is imported, they automatically appear in the GUI because the GUI
recursively searches for subclasses of ``Formula``.

## Creating a Formula Class

1. **Choose a module** – Built‑in formulas reside in
   `lambda_explorer/tools/aero_formulas.py`. You can add your class there or
   create a new module under `lambda_explorer/tools`. Ensure the module is
   imported (for example from `gui_tools.py`) so that the class is registered.
2. **Define the variables** – Provide an ordered list of variable names in the
   class attribute `variables`.
3. **Implement `__init__`** – Inside `__init__` create `sympy` symbols and the
   equation using `sympy.Eq`. Then call
   `super().__init__(self.variables, equation)`.

A minimal example looks like this:

```python
from __future__ import annotations
import sympy
from .formula_base import Formula

class AspectRatio(Formula):
    """AR = b**2 / S"""
    variables = ["AR", "b", "S"]

    def __init__(self) -> None:
        AR, b, S = sympy.symbols("AR b S")
        eq = sympy.Eq(AR, b ** 2 / S)
        super().__init__(self.variables, eq)
```

After the module is imported, `AspectRatio` will appear in the formula overview
window and can be used like any other equation.

### Custom LaTeX Output

The base class can render the equation automatically using
`sympy.latex`. If you want to override the generated LaTeX string
you can pass an optional `latex` argument to `super().__init__`:

```python
eq = sympy.Eq(AR, b ** 2 / S)
super().__init__(self.variables, eq, latex=r"AR = \frac{b^2}{S}")
```

The GUI will display this string instead of auto‑generated LaTeX.

## Default Values

Default variable values used in the GUI are stored in
`lambda_explorer.tools.default_manager.default_values`. When a new formula class
is imported, `gui_tools` adds its variables to this mapping. You can load and
save defaults via the *Defaults* tab in each formula window or by editing
`defaults.yaml`.

## Testing Your Formula

Once added, start the GUI with `lambda-explorer` or by calling
`lambda_explorer.main()` and open your formula from the overview window. You can
use the *Calculation* tab for quick solving and the *Plot* tab to visualise how
the output changes with different inputs.
