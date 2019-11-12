#!/usr/bin/env python3

from challenge9 import pkcs7_padding
from base64 import b64decode
from Crypto.Cipher import AES

def xor_byte(bytes0, bytes1):
	if isinstance(bytes0, str):
		bytes0 = bytes0.encode()
	if isinstance(bytes1, str):
		bytes1 = bytes1.encode()
	return bytes([ch1 ^ ch2 for ch1, ch2 in zip(bytes0, bytes1)])

def aes_encrypt_ecb(text, key):
	aes = AES.new(key, AES.MODE_ECB)
	return aes.encrypt(text).decode('latin1')

def aes_decrypt_ecb(cipher, key):
	aes = AES.new(key, AES.MODE_ECB)
	return aes.decrypt(cipher).decode('latin1')

def aes_encrypt_cbc(text, key, iv):
	padded_text = pkcs7_padding(text, (len(text) + 15) // 16 * 16)
	block_num = len(padded_text) // 16
	blocks = [padded_text[i : i + 16] for i in range(0, len(padded_text), 16)]
	aes = AES.new(key, AES.MODE_ECB)
	prev_cipher = iv
	cipher = b''
	for block in blocks:
		prev_cipher = aes.encrypt(xor_byte(block, prev_cipher))
		cipher += prev_cipher
	return cipher

def aes_encrypt_cbc2(text, key, iv):
	padded_text = pkcs7_padding(text).decode()
	iv = iv.decode()
	aes = AES.new(key, AES,MODE_CBC, iv)
	return aes.encrypt(text).decode('latin1')

def aes_decrypt_cbc(cipher, key, iv):
	block_num = len(cipher) // 16
	blocks = [cipher[i : i + 16] for i in range(0, len(cipher), 16)]
	aes = AES.new(key, AES.MODE_ECB)
	prev_text = iv
	text = b''
	for block in blocks:
		text += xor_byte(aes.decrypt(block), prev_text)
		prev_text = block
	
	if text[-text[-1]:] == bytes([text[-1]]) * text[-1]:
		return text[0 : len(text) - text[-1]]
	return text

def aes_decrypt_cbc2(cipher, key, iv):
	aes = AES.new(key, AES.MODE_CBC, iv)
	return aes.decrypt(cipher)

if __name__ == '__main__':
	with open('10.txt') as f:
		cipher = f.read()
	cipher = b64decode(cipher)
	key = 'YELLOW SUBMARINE'
	iv = '\0' * 16
	result = aes_decrypt_cbc(cipher, key, iv).decode()
	print(result)

