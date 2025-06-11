# main.py
from tools.gui_tools import build_context_menu# IdealeGasGleichung nur, wenn du Defaults setzen willst

if __name__ == "__main__":
    # Optional: Default-Werte pro Variable
    defaults = {
        "R": "8.314",    # Beispiel: R automatisch vorbelegen
        # weitere Defaults…
    }

    # Starte die GUI mit Defaults (oder ohne Argumente für alle Leerfelder)
    build_context_menu(width=800, height=600)
