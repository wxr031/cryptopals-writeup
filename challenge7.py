#!/usr/bin/env python3

from base64 import b64decode
from Crypto.Cipher import AES

def aes_decrypt_ecb(cipher, key):
	assert len(key) == 16 or len(key) == 24 or len(key) == 32
	assert len(cipher) % len(key) == 0

	aes = AES.new(key, AES.MODE_ECB)
	return aes.decrypt(cipher).decode('latin1')

if __name__ == '__main__':
	with open('7.txt') as f:
		global cipher
		cipher = f.read()
	cipher = b64decode(cipher)
	key = 'YELLOW SUBMARINE'

	result = aes_decrypt_ecb(cipher, key)
	print(result)
