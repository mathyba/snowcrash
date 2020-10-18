"""Utilities to display information about exercice resolution"""

from utils.config import GREEN, RED, CYAN, YELLOW


def color_print(color, color_msg, *argv):
    """kwargs are for string to be appended without color for bi-color line output"""

    colors = {
        GREEN: "\033[32m",
        RED: "\033[31m",
        CYAN: "\033[36m",
        YELLOW: "\033[33m",
    }
    print(f"{colors[color]} {color_msg} \033[39m {''.join(argv)}")


def display(text, color=YELLOW):
    """Display colored text (defaults to yellow)"""

    color_print(color, f"\n{text}\n")


def display_welcome(level):
    """Displays generic title upon starting level script"""

    display(f"*** SOLVING {level.upper()} ***", CYAN)
