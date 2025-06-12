from __future__ import annotations

from typing import Callable, Dict
import sympy  # type: ignore

class Formula:
    """Base class for symbolic equations providing cached solvers."""

    variables: list[str] = []

    def __init__(self, var_names: list[str], eq: sympy.Eq):
        cls = self.__class__
        if not hasattr(cls, "_vars"):
            cls._vars = {name: sympy.symbols(name) for name in var_names}
            cls.eq = eq
            cls.variables = var_names
            cls._solvers = {}
            for target, symbol in cls._vars.items():
                sols = sympy.solve(eq, symbol)
                if not sols:
                    raise ValueError(f"No solution for {target}")
                args = [v for n, v in cls._vars.items() if n != target]
                cls._solvers[target] = sympy.lambdify(args, sols[0], "numpy")
        self.vars = cls._vars
        self.eq = cls.eq
        self._solvers = cls._solvers

    def solve(self, **knowns) -> float:
        total = set(self.vars.keys())
        given = set(knowns.keys())
        extras = given - total
        if extras:
            raise ValueError(f"Unknown variable(s) provided: {', '.join(sorted(extras))}")
        expected = len(total) - 1
        if len(given) < expected:
            missing = sorted(total - given)
            raise ValueError(f"{len(missing)} variable(s) missing: {', '.join(missing)}")
        if len(given) > expected:
            raise ValueError(f"Too many variables provided (expected {expected}, got {len(given)})")
        target = (total - given).pop()
        args = [knowns[name] for name in self.vars if name != target]
        return float(self._solvers[target](*args))
