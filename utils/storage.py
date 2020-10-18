"""Handle storage and retrieval of flag passwords and level tokens"""

import subprocess

import utils.config as config
from .config import GREEN
from .log import display


def _store_item(level, item, password):
    """If file storage does not exist, create a <item> file and store password"""
    level_str = "level{:02}".format(level)
    try:
        path = f"{config.remote_path}/{level_str}"
        if item != "flag":
            path += "/Ressources"
        path += f"/{item}"
        with open(path, "+w", encoding="utf-8") as myfile:
            display(f"--> storing {item} '{password}' for {level_str} in {path}", GREEN)
            myfile.write(password + "\n")
        subprocess.run(["chmod", "a+rw", path], check=True)
    except (FileExistsError, FileNotFoundError):
        # Overwrite file content if storage file already exists
        # Silently create file if it doesn't exist
        pass


def store_flag(level, flag):
    """Store flag"""

    _store_item(level, "flag", flag)


def store_token(level, token):
    """Store token"""

    _store_item(level, "token", token)


def get_token(level):
    """Retrieve token from token file in level Ressources directory"""

    with open(f"{config.remote_path}/{level}/Ressources/token", "r") as myfile:
        return myfile.read().rstrip()
