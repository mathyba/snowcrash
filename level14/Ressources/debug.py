"""Exploit file with gdb

This script should be run within gdb intepreter
"""
import gdb

gdb.execute("file getflag")
gdb.execute("break *main +72")
gdb.execute("break *main +452")
gdb.execute("r")
gdb.execute("set $eax=0")
gdb.execute("cont")
gdb.execute("set $eax=3014")
gdb.execute("cont")
gdb.execute("quit")
