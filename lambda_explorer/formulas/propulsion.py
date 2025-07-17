from __future__ import annotations

import sympy  # type: ignore

from ..tools.formula_base import Formula

class GeneralThrust(Formula):
    """F = m_dot * c_e = ∮ p dA_l"""

    topic = "Propulsion"
    variables = ["F", "m_dot", "c_e", "p", "A_l"]

    def __init__(self):
        F, m_dot, c_e, p, A_l = sympy.symbols("F m_dot c_e p A_l")
        eq = sympy.Eq(F, m_dot * c_e)
        super().__init__(self.variables, eq)

class ThrustExpanded(Formula):
    """F = m_dot * w_e + (p_e - p_a) * A_e = m_dot * c_e"""

    topic = "Propulsion"
    variables = ["F", "m_dot", "w_e", "p_e", "p_a", "A_e", "c_e"]

    def __init__(self):
        F, m_dot, w_e, p_e, p_a, A_e, c_e = sympy.symbols("F m_dot w_e p_e p_a A_e c_e")
        eq = sympy.Eq(F, m_dot * w_e + (p_e - p_a) * A_e)
        super().__init__(self.variables, eq)

class EffectiveExhaustVelocity(Formula):
    """c_e = F / m_dot = w_e + (p_e - p_a)*A_e/m_dot = c_star * c_f"""

    topic = "Propulsion"
    variables = ["c_e", "F", "m_dot", "w_e", "p_e", "p_a", "A_e", "c_star", "c_f"]

    def __init__(self):
        c_e, F, m_dot, w_e, p_e, p_a, A_e, c_star, c_f = sympy.symbols("c_e F m_dot w_e p_e p_a A_e c_star c_f")
        eq = sympy.Eq(c_e, F / m_dot)
        super().__init__(self.variables, eq)

class SpecificImpulse(Formula):
    """I_s = c_e / g0 = F / (m_dot * g0)"""

    topic = "Propulsion"
    variables = ["I_s", "c_e", "g0", "F", "m_dot"]

    def __init__(self):
        I_s, c_e, g0, F, m_dot = sympy.symbols("I_s c_e g0 F m_dot")
        eq = sympy.Eq(I_s, c_e / g0)
        super().__init__(self.variables, eq)

class ThrustCoefficient(Formula):
    """c_f = F / (p0 * A_t)"""

    topic = "Propulsion"
    variables = ["c_f", "F", "p0", "A_t"]

    def __init__(self):
        c_f, F, p0, A_t = sympy.symbols("c_f F p0 A_t")
        eq = sympy.Eq(c_f, F / (p0 * A_t))
        super().__init__(self.variables, eq)

class MassFlow(Formula):
    """m_dot = ρ * w * A = (p0 * A_t / sqrt(R*T0)) * Γ"""

    topic = "Propulsion"
    variables = ["m_dot", "rho", "w", "A", "p0", "A_t", "R", "T0", "Gamma"]

    def __init__(self):
        m_dot, rho, w, A, p0, A_t, R, T0, Gamma = sympy.symbols("m_dot rho w A p0 A_t R T0 Gamma")
        eq = sympy.Eq(m_dot, p0 * A_t / sympy.sqrt(R * T0) * Gamma)
        super().__init__(self.variables, eq)

class GammaFunction(Formula):
    """Γ = sqrt(κ * (2/(κ+1))^((κ+1)/(κ-1)))"""

    topic = "Propulsion"
    variables = ["Gamma", "kappa"]

    def __init__(self):
        Gamma, kappa = sympy.symbols("Gamma kappa")
        eq = sympy.Eq(Gamma, sympy.sqrt(kappa * (2/(kappa+1))**((kappa+1)/(kappa-1))))
        super().__init__(self.variables, eq)

class CharacteristicLength(Formula):
    """L_star = V0 / A_t"""

    topic = "Propulsion"
    variables = ["L_star", "V0", "A_t"]

    def __init__(self):
        L_star, V0, A_t = sympy.symbols("L_star V0 A_t")
        eq = sympy.Eq(L_star, V0 / A_t)
        super().__init__(self.variables, eq)

class CharacteristicVelocity(Formula):
    """c_star = p0 * A_t / m_dot = sqrt(R*T0 / Gamma)"""

    topic = "Propulsion"
    variables = ["c_star", "p0", "A_t", "m_dot", "R", "T0", "Gamma"]

    def __init__(self):
        c_star, p0, A_t, m_dot, R, T0, Gamma = sympy.symbols("c_star p0 A_t m_dot R T0 Gamma")
        eq = sympy.Eq(c_star, sympy.sqrt(R * T0 / Gamma))
        super().__init__(self.variables, eq)
