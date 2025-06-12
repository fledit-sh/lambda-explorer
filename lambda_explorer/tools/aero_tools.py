# tools/aero_tools.py
import sympy  # type: ignore
from typing import Callable, Dict, Optional, Type

# DearPyGui import
try:
    import dearpygui.dearpygui as dpg
except ImportError:
    raise ImportError("Please install dearpygui (pip install dearpygui)")

# Base class for symbolic equations
class Formula:
    """Base class for symbolic equations.

    Given a list of variable names and a ``sympy`` equation this class
    automatically generates numerical solvers for every variable. The
    :meth:`solve` method expects all but one variables as keyword arguments and
    returns the numeric solution for the missing one.
    """
    variables: list[str] = []

    def __init__(self, var_names: list[str], eq: sympy.Eq):
        self.vars: Dict[str, sympy.Basic] = {
            name: sympy.symbols(name) for name in var_names
        }
        self.eq = eq
        # store variables also on the class for inspection without instantiation
        self.__class__.variables = var_names
        self._solvers: Dict[str, Callable] = {}
        for target, symbol in self.vars.items():
            sols = sympy.solve(self.eq, symbol)
            if not sols:
                raise ValueError(f"No solution for {target}")
            args = [v for n, v in self.vars.items() if n != target]
            self._solvers[target] = sympy.lambdify(args, sols[0], "numpy")

    def solve(self, **knowns) -> float:
        """Return the value of the variable that was left unspecified.

        Parameters
        ----------
        **knowns : float
            Keyword arguments for all known variable values. Exactly one
            variable must be omitted so that it can be solved for.
        """
        total = set(self.vars.keys())
        given = set(knowns.keys())
        extras = given - total
        if extras:
            raise ValueError(
                f"Unknown variable(s) provided: {', '.join(sorted(extras))}"
            )
        expected = len(total) - 1
        if len(given) < expected:
            missing = sorted(total - given)
            raise ValueError(
                f"{len(missing)} variable(s) missing: {', '.join(missing)}"
            )
        if len(given) > expected:
            raise ValueError(
                f"Too many variables provided (expected {expected}, got {len(given)})"
            )
        target = (total - given).pop()
        args = [knowns[name] for name in self.vars if name != target]
        return float(self._solvers[target](*args))

# Example formulas
class IdealGasEquation(Formula):
    """P * V = n * R * T"""

    variables = ['P', 'V', 'n', 'R', 'T']

    def __init__(self):
        P, V, n, R, T = sympy.symbols("P V n R T")
        eq = sympy.Eq(P * V, n * R * T)
        super().__init__(self.variables, eq)

class CircleArea(Formula):
    """A = pi * r**2"""

    variables = ['A', 'r']

    def __init__(self):
        A, r = sympy.symbols("A r")
        eq = sympy.Eq(A, sympy.pi * r**2)
        super().__init__(self.variables, eq)

# Additional aerodynamic formulas
class L_eq(Formula):
    """L = 0.5 * rho * V**2 * S * Cl"""

    variables = ['L', 'rho', 'V', 'S', 'Cl']

    def __init__(self):
        L, rho, V, S, Cl = sympy.symbols("L rho V S Cl")
        eq = sympy.Eq(L, sympy.Rational(1, 2) * rho * V**2 * S * Cl)
        super().__init__(self.variables, eq)


class D_eq(Formula):
    """D = 0.5 * rho * V**2 * S * Cd"""

    variables = ['D', 'rho', 'V', 'S', 'Cd']

    def __init__(self):
        D, rho, V, S, Cd = sympy.symbols("D rho V S Cd")
        eq = sympy.Eq(D, sympy.Rational(1, 2) * rho * V**2 * S * Cd)
        super().__init__(self.variables, eq)


class M_eq(Formula):
    """M = 0.5 * rho * V**2 * S * c * Cm"""

    variables = ['M', 'rho', 'V', 'S', 'c', 'Cm']

    def __init__(self):
        M, rho, V, S, c, Cm = sympy.symbols("M rho V S c Cm")
        eq = sympy.Eq(M, sympy.Rational(1, 2) * rho * V**2 * S * c * Cm)
        super().__init__(self.variables, eq)


class q_eq(Formula):
    """q = 0.5 * rho * V**2"""

    variables = ['q', 'rho', 'V']

    def __init__(self):
        q, rho, V = sympy.symbols("q rho V")
        eq = sympy.Eq(q, sympy.Rational(1, 2) * rho * V**2)
        super().__init__(self.variables, eq)


class Re_eq(Formula):
    """Re = rho * V * c / mu"""

    variables = ['Re', 'rho', 'V', 'c', 'mu']

    def __init__(self):
        Re, rho, V, c, mu = sympy.symbols("Re rho V c mu")
        eq = sympy.Eq(Re, rho * V * c / mu)
        super().__init__(self.variables, eq)


class Cf_lam(Formula):
    """Cf = 1.328 / sqrt(Re)"""

    variables = ['Cf', 'Re']

    def __init__(self):
        Cf, Re = sympy.symbols("Cf Re")
        eq = sympy.Eq(Cf, 1.328 / sympy.sqrt(Re))
        super().__init__(self.variables, eq)


class Cf_turb(Formula):
    """Cf = 0.455 / (log(Re)**2.58)"""

    variables = ['Cf', 'Re']

    def __init__(self):
        Cf, Re = sympy.symbols("Cf Re")
        eq = sympy.Eq(Cf, 0.455 / (sympy.log(Re) ** sympy.Float(2.58)))
        super().__init__(self.variables, eq)


class delta_lam(Formula):
    """delta = 5 * x / sqrt(Re)"""

    variables = ['delta', 'x', 'Re']

    def __init__(self):
        delta, x, Re = sympy.symbols("delta x Re")
        eq = sympy.Eq(delta, 5 * x / sympy.sqrt(Re))
        super().__init__(self.variables, eq)


class delta_star_lam(Formula):
    """delta_star = 1.72 * x / sqrt(Re)"""

    variables = ['delta_star', 'x', 'Re']

    def __init__(self):
        delta_star, x, Re = sympy.symbols("delta_star x Re")
        eq = sympy.Eq(delta_star, 1.72 * x / sympy.sqrt(Re))
        super().__init__(self.variables, eq)


class theta_lam(Formula):
    """theta = 0.664 * x / sqrt(Re)"""

    variables = ['theta', 'x', 'Re']

    def __init__(self):
        theta, x, Re = sympy.symbols("theta x Re")
        eq = sympy.Eq(theta, 0.664 * x / sympy.sqrt(Re))
        super().__init__(self.variables, eq)


class Cl_alpha(Formula):
    """Cl = 2 * pi * (alpha - alpha0)"""

    variables = ['Cl', 'alpha', 'alpha0']

    def __init__(self):
        Cl, alpha, alpha0 = sympy.symbols("Cl alpha alpha0")
        eq = sympy.Eq(Cl, 2 * sympy.pi * (alpha - alpha0))
        super().__init__(self.variables, eq)


class Cd_induced(Formula):
    """Cd_i = Cl**2 / (pi * AR * e)"""

    variables = ['Cd_i', 'Cl', 'AR', 'e']

    def __init__(self):
        Cd_i, Cl, AR, e = sympy.symbols("Cd_i Cl AR e")
        eq = sympy.Eq(Cd_i, Cl**2 / (sympy.pi * AR * e))
        super().__init__(self.variables, eq)


class Cd_total(Formula):
    """Cd = Cd0 + k * Cl**2"""

    variables = ['Cd', 'Cd0', 'k', 'Cl']

    def __init__(self):
        Cd, Cd0, k, Cl = sympy.symbols("Cd Cd0 k Cl")
        eq = sympy.Eq(Cd, Cd0 + k * Cl**2)
        super().__init__(self.variables, eq)


class Cd_polar(Formula):
    """Cd = Cd0 + (Cl**2 / (pi * AR * e))"""

    variables = ['Cd', 'Cd0', 'Cl', 'AR', 'e']

    def __init__(self):
        Cd, Cd0, Cl, AR, e = sympy.symbols("Cd Cd0 Cl AR e")
        eq = sympy.Eq(Cd, Cd0 + (Cl**2 / (sympy.pi * AR * e)))
        super().__init__(self.variables, eq)


class Cl_min_drag(Formula):
    """Cl_md = sqrt(Cd0 * pi * AR * e)"""

    variables = ['Cl_md', 'Cd0', 'AR', 'e']

    def __init__(self):
        Cl_md, Cd0, AR, e = sympy.symbols("Cl_md Cd0 AR e")
        eq = sympy.Eq(Cl_md, sympy.sqrt(Cd0 * sympy.pi * AR * e))
        super().__init__(self.variables, eq)


class Cp(Formula):
    """Cp = 1 - (V/V_inf)**2"""

    variables = ['Cp', 'V', 'V_inf']

    def __init__(self):
        Cp_sym, V, V_inf = sympy.symbols("Cp V V_inf")
        eq = sympy.Eq(Cp_sym, 1 - (V / V_inf) ** 2)
        super().__init__(self.variables, eq)


class V_ratio(Formula):
    """V_ratio = sqrt(1 - Cp)"""

    variables = ['V_ratio', 'Cp']

    def __init__(self):
        V_ratio_sym, Cp = sympy.symbols("V_ratio Cp")
        eq = sympy.Eq(V_ratio_sym, sympy.sqrt(1 - Cp))
        super().__init__(self.variables, eq)

# Additional aerodynamic formulas
class L_eq(Formula):
    """L = 0.5 * rho * V**2 * S * Cl"""

    def __init__(self):
        L, rho, V, S, Cl = sympy.symbols("L rho V S Cl")
        eq = sympy.Eq(L, sympy.Rational(1, 2) * rho * V**2 * S * Cl)
        super().__init__(['L', 'rho', 'V', 'S', 'Cl'], eq)


class D_eq(Formula):
    """D = 0.5 * rho * V**2 * S * Cd"""

    def __init__(self):
        D, rho, V, S, Cd = sympy.symbols("D rho V S Cd")
        eq = sympy.Eq(D, sympy.Rational(1, 2) * rho * V**2 * S * Cd)
        super().__init__(['D', 'rho', 'V', 'S', 'Cd'], eq)


class M_eq(Formula):
    """M = 0.5 * rho * V**2 * S * c * Cm"""

    def __init__(self):
        M, rho, V, S, c, Cm = sympy.symbols("M rho V S c Cm")
        eq = sympy.Eq(M, sympy.Rational(1, 2) * rho * V**2 * S * c * Cm)
        super().__init__(['M', 'rho', 'V', 'S', 'c', 'Cm'], eq)


class q_eq(Formula):
    """q = 0.5 * rho * V**2"""

    def __init__(self):
        q, rho, V = sympy.symbols("q rho V")
        eq = sympy.Eq(q, sympy.Rational(1, 2) * rho * V**2)
        super().__init__(['q', 'rho', 'V'], eq)


class Re_eq(Formula):
    """Re = rho * V * c / mu"""

    def __init__(self):
        Re, rho, V, c, mu = sympy.symbols("Re rho V c mu")
        eq = sympy.Eq(Re, rho * V * c / mu)
        super().__init__(['Re', 'rho', 'V', 'c', 'mu'], eq)


class Cf_lam(Formula):
    """Cf = 1.328 / sqrt(Re)"""

    def __init__(self):
        Cf, Re = sympy.symbols("Cf Re")
        eq = sympy.Eq(Cf, 1.328 / sympy.sqrt(Re))
        super().__init__(['Cf', 'Re'], eq)


class Cf_turb(Formula):
    """Cf = 0.455 / (log(Re)**2.58)"""

    def __init__(self):
        Cf, Re = sympy.symbols("Cf Re")
        eq = sympy.Eq(Cf, 0.455 / (sympy.log(Re) ** sympy.Float(2.58)))
        super().__init__(['Cf', 'Re'], eq)


class delta_lam(Formula):
    """delta = 5 * x / sqrt(Re)"""

    def __init__(self):
        delta, x, Re = sympy.symbols("delta x Re")
        eq = sympy.Eq(delta, 5 * x / sympy.sqrt(Re))
        super().__init__(['delta', 'x', 'Re'], eq)


class delta_star_lam(Formula):
    """delta_star = 1.72 * x / sqrt(Re)"""

    def __init__(self):
        delta_star, x, Re = sympy.symbols("delta_star x Re")
        eq = sympy.Eq(delta_star, 1.72 * x / sympy.sqrt(Re))
        super().__init__(['delta_star', 'x', 'Re'], eq)


class theta_lam(Formula):
    """theta = 0.664 * x / sqrt(Re)"""

    def __init__(self):
        theta, x, Re = sympy.symbols("theta x Re")
        eq = sympy.Eq(theta, 0.664 * x / sympy.sqrt(Re))
        super().__init__(['theta', 'x', 'Re'], eq)


class Cl_alpha(Formula):
    """Cl = 2 * pi * (alpha - alpha0)"""

    def __init__(self):
        Cl, alpha, alpha0 = sympy.symbols("Cl alpha alpha0")
        eq = sympy.Eq(Cl, 2 * sympy.pi * (alpha - alpha0))
        super().__init__(['Cl', 'alpha', 'alpha0'], eq)


class Cd_induced(Formula):
    """Cd_i = Cl**2 / (pi * AR * e)"""

    def __init__(self):
        Cd_i, Cl, AR, e = sympy.symbols("Cd_i Cl AR e")
        eq = sympy.Eq(Cd_i, Cl**2 / (sympy.pi * AR * e))
        super().__init__(['Cd_i', 'Cl', 'AR', 'e'], eq)


class Cd_total(Formula):
    """Cd = Cd0 + k * Cl**2"""

    def __init__(self):
        Cd, Cd0, k, Cl = sympy.symbols("Cd Cd0 k Cl")
        eq = sympy.Eq(Cd, Cd0 + k * Cl**2)
        super().__init__(['Cd', 'Cd0', 'k', 'Cl'], eq)


class Cd_polar(Formula):
    """Cd = Cd0 + (Cl**2 / (pi * AR * e))"""

    def __init__(self):
        Cd, Cd0, Cl, AR, e = sympy.symbols("Cd Cd0 Cl AR e")
        eq = sympy.Eq(Cd, Cd0 + (Cl**2 / (sympy.pi * AR * e)))
        super().__init__(['Cd', 'Cd0', 'Cl', 'AR', 'e'], eq)


class Cl_min_drag(Formula):
    """Cl_md = sqrt(Cd0 * pi * AR * e)"""

    def __init__(self):
        Cl_md, Cd0, AR, e = sympy.symbols("Cl_md Cd0 AR e")
        eq = sympy.Eq(Cl_md, sympy.sqrt(Cd0 * sympy.pi * AR * e))
        super().__init__(['Cl_md', 'Cd0', 'AR', 'e'], eq)


class Cp(Formula):
    """Cp = 1 - (V/V_inf)**2"""

    def __init__(self):
        Cp_sym, V, V_inf = sympy.symbols("Cp V V_inf")
        eq = sympy.Eq(Cp_sym, 1 - (V / V_inf) ** 2)
        super().__init__(['Cp', 'V', 'V_inf'], eq)


class V_ratio(Formula):
    """V_ratio = sqrt(1 - Cp)"""

    def __init__(self):
        V_ratio_sym, Cp = sympy.symbols("V_ratio Cp")
        eq = sympy.Eq(V_ratio_sym, sympy.sqrt(1 - Cp))
        super().__init__(['V_ratio', 'Cp'], eq)

# Helper functions for GUI interactions
def clear_callback(sender, app_data, user_data):
    """Clear the value of the input field referenced by *user_data*."""
    dpg.set_value(user_data, "")


def default_callback(sender, app_data, user_data):
    """Set the default value for an input field.

    Parameters
    ----------
    sender, app_data : Any
        Passed through by DearPyGui and unused here.
    user_data : Tuple[str, str]
        Tuple of the widget tag and the default value to apply.
    """
    tag, default_val = user_data
    dpg.set_value(tag, default_val)


def calculate_callback(sender, app_data, user_data):
    """Calculate the missing variable of the selected equation."""
    eq: Formula = user_data['equation']
    vars_tags = user_data['vars_tags']
    error_tag = user_data['error_tag']
    dpg.set_value(error_tag, '')
    knowns: Dict[str, float] = {}
    missing = []
    for var, tag in vars_tags.items():
        val = dpg.get_value(tag)
        if not str(val).strip():
            missing.append(var)
        else:
            try:
                knowns[var] = float(val)
            except ValueError:
                dpg.set_value(error_tag, f"Invalid value for {var}: '{val}'")
                return
    if len(missing) != 1:
        dpg.set_value(error_tag, f"Please leave exactly one variable empty (currently {len(missing)})")
        return
    try:
        result = eq.solve(**knowns)
        dpg.set_value(vars_tags[missing[0]], str(result))
    except Exception as e:
        dpg.set_value(error_tag, str(e))

# GUI layout
def build_gui(width: int = 600, height: int = 400, defaults: Optional[Dict[str, str]] = None):
    """Start a simple formula calculator GUI.

    Parameters
    ----------
    width, height : int
        Size of the created DearPyGui window.
    defaults : dict[str, str] or None
        Optional mapping of variable names to default values shown in the
        input fields.
    """
    dpg.create_context()
    defaults = defaults or {}

    # Automatically discover all available formula subclasses
    klasses = Formula.__subclasses__()
    name_to_class: Dict[str, Type[Formula]] = {cls.__name__: cls for cls in klasses}
    formula_names = list(name_to_class.keys())

    def on_formula_change(sender, app_data):
        # Name of the selected class
        cls_name = app_data
        eq = name_to_class[cls_name]()
        # Clear previous inputs
        dpg.delete_item('child_inputs', children_only=True)
        vars_tags = {}
        for var in eq.vars:
            tag = f"input_{var}"
            default_val = defaults.get(var, '')
            with dpg.group(parent='child_inputs', horizontal=True):
                dpg.add_input_text(tag=tag, label=var, default_value=default_val)
                dpg.add_button(label='Clear', callback=clear_callback, user_data=tag)
                dpg.add_button(label='Default', callback=default_callback, user_data=(tag, default_val))
            vars_tags[var] = tag
        # Update calculate button
        dpg.configure_item('btn_calc', user_data={'equation': eq, 'vars_tags': vars_tags, 'error_tag': 'error_text'})

    with dpg.window(label='Formula Calculator', width=width, height=height):
        dpg.add_text('Choose a formula:')
        dpg.add_combo(formula_names, default_value=formula_names[0], callback=on_formula_change, tag='combo_formula')
        dpg.add_separator()
        with dpg.child_window(tag='child_inputs'):
            pass
        dpg.add_text(tag='error_text', default_value='', color=[255,0,0])
        dpg.add_button(label='Calculate', tag='btn_calc', callback=calculate_callback)

    # Initial display
    on_formula_change(None, formula_names[0])

    dpg.create_viewport(title='Formula Calculator', width=width+20, height=height+30)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()
