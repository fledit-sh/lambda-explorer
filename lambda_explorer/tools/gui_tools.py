# gui_tools.py
import sympy  # type: ignore
from typing import Dict, Type, Optional, List
import dearpygui.dearpygui as dpg
from .aero_tools import Formula

# Discover all Formula subclasses
formula_classes = {cls.__name__: cls for cls in Formula.__subclasses__()}

# Default values storage
default_values: Dict[str, str] = {}
for cls in formula_classes.values():
    for var in cls().vars:
        default_values.setdefault(var, '')

# Callback: calculate just-cleared input and then full calculation
def calc_input_callback(sender, app_data, user_data):
    """Clear the input field and immediately recalculate the equation."""
    input_tag = user_data['input_tag']
    dpg.set_value(input_tag, '')
    calculate_callback(sender, app_data, user_data)

# Callback to set default into input
def set_default_callback(sender, app_data, user_data):
    """Insert the stored default value for the given variable."""
    input_tag, var = user_data
    default = default_values.get(var, '')
    dpg.set_value(input_tag, default)

# Callback to calculate formula from bottom button
def calculate_callback(sender, app_data, user_data):
    """Solve the equation with the values entered by the user."""
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

# Helper to update constant input fields for plotting
def update_plot_inputs(sender, app_data, user_data):
    """Refresh the constant value input fields when plot variables change."""
    eq: Formula = user_data['equation']
    x_var = dpg.get_value(user_data['x_var_tag'])
    y_var = dpg.get_value(user_data['y_var_tag'])
    group = user_data['const_group']
    dpg.delete_item(group, children_only=True)
    user_data['const_tags'].clear()
    for var in eq.vars:
        if var in (x_var, y_var):
            continue
        tag = f"{group}_{var}"
        default = default_values.get(var, '')
        dpg.add_input_text(parent=group, label=var, tag=tag, default_value=default)
        user_data['const_tags'][var] = tag

# Callback to compute and display plot data
def plot_callback(sender, app_data, user_data):
    """Calculate plot data for the selected x/y variables."""
    eq: Formula = user_data['equation']
    x_var = dpg.get_value(user_data['x_var_tag'])
    y_var = dpg.get_value(user_data['y_var_tag'])
    start = float(dpg.get_value(user_data['x_start']))
    end = float(dpg.get_value(user_data['x_end']))
    step = float(dpg.get_value(user_data['x_step']))
    consts = {}
    for var, tag in user_data['const_tags'].items():
        val = dpg.get_value(tag)
        try:
            consts[var] = float(val)
        except ValueError:
            return
    xs: List[float] = []
    ys: List[float] = []
    x = start
    while x <= end:
        knowns = consts.copy()
        knowns[x_var] = x
        try:
            y_val = eq.solve(**knowns)
        except Exception:
            break
        xs.append(x)
        ys.append(y_val)
        x += step
    dpg.set_value(user_data['series_tag'], [xs, ys])

# Open per-formula window
def open_formula_window(sender, app_data, user_data):
    """Create or show a window for the selected formula."""
    cls_name = user_data
    eq = formula_classes[cls_name]()
    window_tag = f"win_{cls_name}"
    if dpg.does_item_exist(window_tag):
        dpg.show_item(window_tag)
        return
    vars_tags: Dict[str, str] = {}
    error_tag = f"{window_tag}_error"
    shared_data = {'equation': eq, 'vars_tags': vars_tags, 'error_tag': error_tag}

    plot_data = {
        'equation': eq,
        'const_tags': {},
    }

    with dpg.window(label=cls_name, tag=window_tag, width=450, height=400):
        dpg.add_text(f"Formula: {cls_name}")
        with dpg.tab_bar():
            with dpg.tab(label="Calculation"):
                for var in eq.vars:
                    input_tag = f"{window_tag}_input_{var}"
                    default = default_values.get(var, '')
                    with dpg.group(horizontal=True):
                        dpg.add_input_text(tag=input_tag, label=var, default_value=default)
                        shared_data['input_tag'] = input_tag
                        dpg.add_button(label="Calc", callback=calc_input_callback, user_data=shared_data.copy())
                        dpg.add_button(label="Default", callback=set_default_callback, user_data=(input_tag, var))
                    vars_tags[var] = input_tag
                dpg.add_text(tag=error_tag, default_value="", color=[255,0,0])
                dpg.add_button(label="Calculate", callback=calculate_callback, user_data=shared_data)

            with dpg.tab(label="Plot"):
                x_var_tag = f"{window_tag}_xvar"
                y_var_tag = f"{window_tag}_yvar"
                x_start_tag = f"{window_tag}_xstart"
                x_end_tag = f"{window_tag}_xend"
                x_step_tag = f"{window_tag}_xstep"
                const_group_tag = f"{window_tag}_const"
                plot_series_tag = f"{window_tag}_series"

                plot_data.update({
                    'x_var_tag': x_var_tag,
                    'y_var_tag': y_var_tag,
                    'x_start': x_start_tag,
                    'x_end': x_end_tag,
                    'x_step': x_step_tag,
                    'const_group': const_group_tag,
                    'series_tag': plot_series_tag,
                })

                var_names = list(eq.vars)
                dpg.add_combo(var_names, default_value=var_names[0], label="X", tag=x_var_tag, callback=update_plot_inputs, user_data=plot_data)
                dpg.add_combo(var_names, default_value=var_names[1] if len(var_names) > 1 else var_names[0], label="Y", tag=y_var_tag, callback=update_plot_inputs, user_data=plot_data)
                dpg.add_input_float(label="X Start", tag=x_start_tag, default_value=0.0)
                dpg.add_input_float(label="X End", tag=x_end_tag, default_value=10.0)
                dpg.add_input_float(label="Step", tag=x_step_tag, default_value=1.0)
                dpg.add_separator()
                with dpg.group(tag=const_group_tag):
                    pass
                dpg.add_button(label="Plot", callback=plot_callback, user_data=plot_data)
                with dpg.plot(label="Plot", height=200):
                    dpg.add_plot_axis(dpg.mvXAxis, label="X")
                    with dpg.plot_axis(dpg.mvYAxis, label="Y"):
                        dpg.add_line_series([], [], tag=plot_series_tag)

        # initial population of constant inputs
        update_plot_inputs(None, None, plot_data)

# Open defaults configuration window
def open_defaults_window(sender, app_data, user_data):
    """Open a window to configure default values for all variables."""
    # Reopen existing window
    if dpg.does_item_exist('win_defaults'):
        dpg.show_item('win_defaults')
        return
    default_tags: Dict[str, str] = {}
    with dpg.window(label="Configure default values", tag='win_defaults', width=400, height=500):
        dpg.add_text("Set default values for variables:")
        # Header row
        with dpg.group(horizontal=True):
            dpg.add_text("Variable")
            dpg.add_text("New value")
            dpg.add_text("Current value")
        # Input rows
        for var in sorted(default_values.keys()):
            input_tag = f"default_input_{var}"
            current_tag = f"current_text_{var}"
            default_tags[var] = input_tag
            with dpg.group(horizontal=True):
                dpg.add_text(var)
                dpg.add_input_text(tag=input_tag, default_value=default_values[var], width=150)
                dpg.add_text(default_values[var], tag=current_tag)
        dpg.add_separator()
        # Save all defaults
        def save_all(sender, app_data):
            for var, tag in default_tags.items():
                val = dpg.get_value(tag)
                default_values[var] = val
                dpg.set_value(f"current_text_{var}", val)
        dpg.add_button(label="Save all", callback=save_all)
        # Export to file
        def export_defaults(sender, app_data):
            import json
            with open('defaults.json', 'w', encoding='utf-8') as f:
                json.dump(default_values, f, ensure_ascii=False, indent=2)
        dpg.add_same_line()
        dpg.add_button(label="Export", callback=export_defaults)

# Build context menu overview
def build_context_menu(width=320, height=390):
    """Open the main window showing all available formulas."""
    dpg.create_context()
    with dpg.window(label="Formula Overview", width=300, height=350):
        dpg.add_text("Right-click formulas to open")
        for name in formula_classes:
            item_tag = f"item_{name}"
            dpg.add_text(name, tag=item_tag)
            with dpg.popup(item_tag, dpg.mvMouseButton_Right):
                dpg.add_menu_item(label="Open formula", callback=open_formula_window, user_data=name)
        dpg.add_separator()
        dpg.add_button(label="Default values...", callback=open_defaults_window)
    dpg.create_viewport(title="Formula Overview", width=320, height=390)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

if __name__ == "__main__":
    build_context_menu()
