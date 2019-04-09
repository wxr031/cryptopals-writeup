#!/usr/bin/env python3

from base64 import b64encode

def hex_to_base64(string):
	text = bytes.fromhex(string)
	return b64encode(text).decode()

if __name__ == '__main__':
	string = input()
	print(hex_to_base64(string))
