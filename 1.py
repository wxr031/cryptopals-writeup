#!/usr/bin/env python3

from base64 import b64encode
string = input()
text = bytes.fromhex(string)
print(b64encode(text).decode())
