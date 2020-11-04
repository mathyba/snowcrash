"""Exploit file with gdb

This script should be run within gdb intepreter"""

import gdb

gdb.execute("file level13")
gdb.execute("break *main +14")
gdb.execute("r")
gdb.execute("set $eax=4242")
gdb.execute("cont")
gdb.execute("quit")
