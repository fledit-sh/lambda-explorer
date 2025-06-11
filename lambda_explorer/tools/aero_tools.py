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
    def __init__(self, var_names: list[str], eq: sympy.Eq):
        self.vars: Dict[str, sympy.Basic] = {name: sympy.symbols(name) for name in var_names}
        self.eq = eq
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
    def __init__(self):
        P, V, n, R, T = sympy.symbols("P V n R T")
        eq = sympy.Eq(P * V, n * R * T)
        super().__init__(['P', 'V', 'n', 'R', 'T'], eq)

class CircleArea(Formula):
    """A = pi * r**2"""
    def __init__(self):
        A, r = sympy.symbols("A r")
        eq = sympy.Eq(A, sympy.pi * r**2)
        super().__init__(['A', 'r'], eq)

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
