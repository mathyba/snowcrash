"""LEVEL 01"""

import subprocess

from utils.level_wrapper import level_handler


@level_handler
def solve_level01(path, snow_crash):
    """Crack the hashed password in /etc/passwd to obtain the flag password"""

    snow_crash.download("/etc/passwd", f"{path}/passwd")
    # John only cracks the password if run once without --show option
    subprocess.run(
        ["/usr/sbin/john", f"{path}/passwd"], capture_output=True, check=True
    )
    # Call again with --show to parse the answer
    output = subprocess.run(
        ["/usr/sbin/john", "--show", f"{path}/passwd"], capture_output=True, check=True
    ).stdout
    password = output.split(b":")[1].decode()
    return "flag", password
