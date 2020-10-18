"""SSH related utility functions"""

from pwn import ssh
from paramiko import AuthenticationException

from .log import display, display_welcome
from .config import vm, port, RED
from .storage import store_flag
from .misc import flag_tostr, parse_token, prompt_for_level


def ssh_conn(user, pwd):
    """Open an SSH connection with Snowcrash VM

    Use in 'with' statement, to automatically close connection when leaving
    """

    display(f"Opening SSH connection with Snowcrash VM as {user}")
    conn = ssh(host=vm, user=user, password=pwd, port=int(port), timeout=2)
    display_welcome(user)
    return conn


def getflag(level_number, password):
    """Connect to Snowcrash VM as flag and run getflag to retrieve token"""

    try:
        with ssh_conn(flag_tostr(level_number), password) as snow_crash:
            token = parse_token(snow_crash["getflag"])
        store_flag(level_number, password)
        return token
    except AuthenticationException as err:
        display(
            f"""Exception raised: {err}
        This flag password is incorrect... Perhaps you should try this level again!""",
            RED,
        )
        prompt_for_level(level_number)
