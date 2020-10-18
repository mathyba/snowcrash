"""LEVEL 14"""

from utils.level_wrapper import level_handler


@level_handler
def solve_level14(path, snow_crash):
    """Debug with gdb"""
    snow_crash.upload(f"{path}/debug.py", "/tmp/debug.py")
    output = (
        snow_crash["gdb -x /tmp/debug.py; rm -f /tmp/debug.py"].decode().split("\n")[-2]
    )
    return "flag", output.split()[-1]
