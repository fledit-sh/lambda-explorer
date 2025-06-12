from __future__ import annotations

import sympy  # type: ignore

from .formula_base import Formula


class ReynoldsNumber(Formula):
    """Re = rho * V * c / mu"""

    variables = ["Re", "rho", "V", "c", "mu"]

    def __init__(self) -> None:
        Re, rho, V, c, mu = sympy.symbols("Re rho V c mu")
        eq = sympy.Eq(Re, rho * V * c / mu)
        super().__init__(self.variables, eq)


class DynamicViscosity(Formula):
    """mu = rho * V * c / Re"""

    variables = ["mu", "rho", "V", "c", "Re"]

    def __init__(self) -> None:
        mu, rho, V, c, Re = sympy.symbols("mu rho V c Re")
        eq = sympy.Eq(mu, rho * V * c / Re)
        super().__init__(self.variables, eq)


class KinematicViscosity(Formula):
    """nu = mu / rho"""

    variables = ["nu", "mu", "rho"]

    def __init__(self) -> None:
        nu, mu, rho = sympy.symbols("nu mu rho")
        eq = sympy.Eq(nu, mu / rho)
        super().__init__(self.variables, eq)
