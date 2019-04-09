#!/usr/bin/env python3

from binascii import hexlify

def repeat_xor(string, key):
	key_len = len(key)
	str_len = len(string)

	key_b = bytearray(key, 'latin1')
	str_b = bytearray(string, 'latin1')
	for i in range(str_len):
		str_b[i] = (str_b[i] ^ key_b[i % key_len]) % 256
	return hexlify(str_b).decode()

if __name__ == '__main__':
	string = input()
	key = input()

	result = repeat_xor(string, key)
	print(result)
