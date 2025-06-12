from __future__ import annotations

from typing import Dict

from .formula_base import Formula

class FormulaSolver:
    """Simple wrapper around Formula providing a consistent interface."""

    def __init__(self, formula: Formula) -> None:
        self.formula = formula

    def solve(self, values: Dict[str, float]) -> float:
        """Solve formula for the unknown variable using provided values."""
        return self.formula.solve(**values)
