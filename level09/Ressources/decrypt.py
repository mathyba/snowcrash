"""Decryption algorithm

Apply to each character an inverse rotation of its index value
abcdefg -> aaaaaaa
"""
import sys

arg = sys.argv[1].encode(errors="surrogateescape")

print("".join([chr(l - i) for i, l in enumerate(arg) if l - i > 0]))
