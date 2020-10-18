"""Miscellanous utilities"""

import importlib
from string import ascii_lowercase as alphabet

from utils.storage import store_token
from utils.config import GREEN
from utils.log import display


def rotn(text, value):
    """Rotate string by value characters"""

    return "".join([alphabet[(alphabet.find(c) - value) % len(alphabet)] for c in text])


def level_tostr(level_number):
    """Convert integer <n> to 'level0<n>' string"""

    return "level{:02d}".format(level_number)


def parse_token(getflag_output):
    """Parse getflag command output and return token"""

    return getflag_output.decode().split(":")[-1].strip()


def prompt_for_level(level_number, password=None):
    """Prompt user before proceeding to next level and store password if provided"""

    if level_number < 15:
        if password is not None:
            store_token(level_number, password)

        answer = input(f"\nProceed to level {level_number} (Y/n) ? ").strip().lower()
        if answer in {"", "y", "yes", "true"}:
            # Import required level module
            importlib.import_module(
                f"{level_tostr(level_number)}.Ressources.{level_tostr(level_number)}"
            )
        else:
            display("OK then, see you next time!")
    else:
        display("This is the end, my friend! Congratulations :)", GREEN)
