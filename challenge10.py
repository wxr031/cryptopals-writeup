#!/usr/bin/env python3

from challenge6 import xor_bytes
from challenge9 import pkcs7_padding
from base64 import b64decode
from Crypto.Cipher import AES

def aes_encrypt_ecb(text, key):
	aes = AES.new(key, AES.MODE_ECB)
	return aes.encrypt(text)

def aes_decrypt_ecb(cipher, key):
	aes = AES.new(key, AES.MODE_ECB)
	return aes.decrypt(cipher)

def aes_decrypt_cbc(cipher, key, iv):
	block_num = len(cipher) // 16
	blocks = [cipher[i : i + 16] for i in range(0, len(cipher), 16)]
	aes = AES.new(key, AES.MODE_ECB)
	prev_text = iv
	text = b''
	for block in blocks:
		text += xor_bytes(aes.decrypt(block), prev_text)
		prev_text = block
	
	if text[-text[-1]:] == bytes([text[-1]]) * text[-1]:
		return text[0 : len(text) - text[-1]]
	return text

if __name__ == '__main__':
	with open('10.txt') as f:
		cipher = f.read()
	cipher = b64decode(cipher)
	key = 'YELLOW SUBMARINE'
	iv = '\0' * 16
	result = aes_decrypt_cbc(cipher, key, iv).decode()
	print(result)

