from __future__ import annotations

import os
import dearpygui.dearpygui as dpg

LAYOUT_FILE = "layout.ini"


def load_layout(path: str = LAYOUT_FILE) -> None:
    """Load window layout from an ini file if it exists."""
    if os.path.exists(path):
        try:
            dpg.load_init_file(path)
        except Exception:
            pass


def save_layout(path: str = LAYOUT_FILE) -> None:
    """Save current window layout to an ini file."""
    try:
        dpg.save_init_file(path)
    except Exception:
        pass
