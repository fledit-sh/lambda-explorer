from __future__ import annotations

from typing import Dict
import yaml
import os

# Global mapping of default values used across the GUI
default_values: Dict[str, str] = {}


def load_defaults_file(path: str = "defaults.yaml") -> None:
    """Load defaults from a YAML file into ``default_values``."""
    if not os.path.exists(path):
        return
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
    except OSError:
        return
    if isinstance(data, dict):
        for var, val in data.items():
            default_values[var] = str(val)


def save_defaults_file(path: str = "defaults.yaml") -> None:
    """Write ``default_values`` to a YAML file."""
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(default_values, f, sort_keys=False)
