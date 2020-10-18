"""LEVEL 00"""

from utils.level_wrapper import level_handler
import utils as u


@level_handler
def solve_level00(_, snow_crash):
    """Find file owned by flag00 and decode its content to obtain the flag password"""

    # u.storage.store_token(0, "level00")
    output = snow_crash[r"find /usr -group flag00 -exec cat {} \; 2>/dev/null"]
    password = u.misc.rotn(output.decode(), 15)
    return "flag", password
