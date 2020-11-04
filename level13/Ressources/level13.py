"""LEVEL 13"""

from utils.level_wrapper import level_handler


@level_handler
def solve_level13(path, snow_crash):
    """Debug with gdb"""

    snow_crash.upload(f"{path}/debug.py", "/tmp/debug.py")
    output = snow_crash["gdb -x /tmp/debug.py; rm -f /tmp/debug.py"].decode()
    return "token", output.split("\n")[-2].split()[-1]
