from __future__ import annotations

import sympy  # type: ignore

from ..tools.formula_base import Formula

"""Collection of thermodynamic formula classes."""

# ----------------------------------------------------------------------------
# Thermodynamic Fundamentals
# ----------------------------------------------------------------------------


class IdealGasLaw(Formula):
    """p = ρ * R * T"""

    topic = "Theromdynamics"

    variables = ["p", "rho", "R", "T"]

    def __init__(self):
        p, rho, R, T = sympy.symbols("p rho R T")
        eq = sympy.Eq(p, rho * R * T)
        super().__init__(self.variables, eq)


class AdiabaticPressureVolume(Formula):
    """p * v^κ = C (constant)"""

    topic = "Theromdynamics"

    variables = ["p", "v", "kappa", "C"]

    def __init__(self):
        p, v, kappa, C = sympy.symbols("p v kappa C")
        eq = sympy.Eq(p * v**kappa, C)
        super().__init__(self.variables, eq)


class AdiabaticTemperatureVolume(Formula):
    """T * v^{κ−1} = C (constant)"""

    topic = "Theromdynamics"

    variables = ["T", "v", "kappa", "C"]

    def __init__(self):
        T, v, kappa, C = sympy.symbols("T v kappa C")
        eq = sympy.Eq(T * v ** (kappa - 1), C)
        super().__init__(self.variables, eq)


class AdiabaticTemperaturePressure(Formula):
    """T * p^{(1−κ)/κ} = C (constant)"""

    topic = "Theromdynamics"

    variables = ["T", "p", "kappa", "C"]

    def __init__(self):
        T, p, kappa, C = sympy.symbols("T p kappa C")
        exponent = (1 - kappa) / kappa
        eq = sympy.Eq(T * p**exponent, C)
        super().__init__(self.variables, eq)
