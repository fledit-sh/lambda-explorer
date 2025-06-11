"""Entry point for lambda_explorer GUI."""

from .tools.gui_tools import build_context_menu


def main() -> None:
    """Launch the GUI."""
    build_context_menu(width=800, height=600)


if __name__ == "__main__":
    main()
