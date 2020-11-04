"""Run link switch and executable simultaneously"""

import os
from subprocess import Popen

Popen(["/bin/bash", "/tmp/create_link.sh"])

while True:
    Popen(["./level10", "/tmp/token", os.getenv("CONTAINER", "localhost")])
