"""LEVEL 02"""

import subprocess

from utils.level_wrapper import level_handler


@level_handler
def solve_level02(path, snow_crash):
    """Follow a stream of packets to find the flag password"""

    snow_crash.download("level02.pcap", f"{path}/level02.pcap")
    # Follow and display stream 0's packet content in hex and ascii format
    output = (
        subprocess.run(
            ["tshark", "-r", f"{path}/level02.pcap", "-z", "follow,tcp,hex,0"],
            capture_output=True,
            check=True,
        )
        .stdout.decode("utf-8")
        .split("\n")
    )
    # Fine line with prompt for password
    matched_lines = [i for i, line in enumerate(output) if "Pass" in line]
    password = "".join(
        [l[-1] for l in output[matched_lines[0] + 1 :] if l.startswith("000000")]
    )[:-1]
    # Detect 3 delete symbols and remove them as well as deleted characters from input
    while "." in password:
        index = password.find(".")
        password = password[: index - 1] + password[index + 1 :]
    return "flag", password
