"""Wrapper function handling all levels"""

import utils.config as config
from .log import display
from .ssh import ssh_conn, prompt_for_level, getflag
from .storage import get_token, store_flag


def level_handler(func):
    """Level handler"""

    number = int(func.__name__[-2:])
    level = func.__name__.split("_")[-1]
    path = f"{config.remote_path}/{level}/Ressources"
    token = get_token(level) if number else "level00"

    def wrapper():
        """Wrapper to handle level"""

        flag_or_token = "", ""
        # Handles most timeout issues
        while flag_or_token not in {"flag", "token"}:
            # Initiate ssh connection to the Snowcrash vm at the required level
            with ssh_conn(level, token) as snow_crash:
                # Solve level and retrieve flag or token
                flag_or_token, password = func(path, snow_crash)

        # Run getflag if needed and store flag
        if flag_or_token == "flag":
            password = getflag(number, password)
        else:
            store_flag(number, "\n")

        prompt_for_level(number + 1, password)

    try:
        return wrapper()
    except FileNotFoundError:
        display(
            f"You have no token stored for {level}. You should try to solve previous levels.",
            config.RED,
        )
