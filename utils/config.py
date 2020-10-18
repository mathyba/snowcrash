"""Configuration file"""

import os
from pwnlib.log import getLogger

HOST = "HOST"
VM = "VM"
PORT = "PORT"
USER = "USER"
LEVEL_PATH = "LEVEL_PATH"
REMOTE_PATH = "REMOTE_PATH"
LOG_LEVEL = "LOG_LEVEL"
CONTAINER = "CONTAINER"

RED = "RED"
CYAN = "CYAN"
YELLOW = "YELLOW"
GREEN = "GREEN"

# Environment variables are set in the Dockerfile or via the docker-compose.yml
host = os.environ.get(HOST, "localhost")
vm = os.environ.get(VM, "localhost")
container = os.environ.get(CONTAINER, "localhost")
port = os.environ.get(PORT, 22)
user = os.environ.get(USER, "snowcrash")
local_level_path = os.environ.get(LEVEL_PATH, "/{user}")
remote_path = os.environ.get(REMOTE_PATH, "/")
log_level = os.environ.get(LOG_LEVEL, "info")

loggers = [
    logger.setLevel(log_level)
    for logger in [
        getLogger("pwnlib.tubes.ssh"),
        getLogger("paramiko.transport"),
        getLogger("pwnlib.elf.elf"),
        getLogger("pwnlib.asm"),
    ]
]
