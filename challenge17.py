#!/usr/bin/env python3

from challenge9 import pkcs7_padding, pkcs7_unpadding, PaddingError
from challenge16 import aes_encrypt_cbc, aes_decrypt_cbc

import os
import base64
import random

BLK_SIZE = 16
key = os.urandom(BLK_SIZE)

def encrypt():
	strings = list(map(base64.b64decode, [
		'MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=',
		'MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=',
		'MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==',
		'MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==',
		'MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl',
		'MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==',
		'MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==',
		'MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=',
		'MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=',
		'MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93'
	]))
	random_string = random.choice(strings)
	text = pkcs7_padding(random_string, BLK_SIZE)
	iv = os.urandom(BLK_SIZE)
	cipher = aes_encrypt_cbc(text, key, iv)
	return cipher, iv

def check_padding(cipher, iv):
	if isinstance(cipher, str):
		cipher = cipher.encode()
	text = aes_decrypt_cbc(cipher, key, iv)

	try:
		pkcs7_unpadding(text)
		return True

	except PaddingError:
		return False

def padding_oracle(check_padding):
	cipher, iv = encrypt()
	ciphers = [cipher[i : i + BLK_SIZE] for i in range(0, len(cipher), BLK_SIZE)]
	#prev_blk = bytearray(iv)
	#for i in range(len(ciphers) - 1):
		#prev_blk_save = prev_blk[:]
		#text = b''
		#for j in range(BLK_SIZE - 1, -1, -1):
			#for ch in range(256):
				#prev_blk[j] = ch
				#if check_padding(ciphers[i], prev_blk):
					#break
			#text = text + bytes([(BLK_SIZE - j) ^ prev_blk[j] ^ prev_blk_save[j]])
			#for k in range(j, BLK_SIZE - 1):
				#prev_blk[k] = prev_blk[k] ^ (BLK_SIZE - j) ^ (BLK_SIZE - j + 1)
		#prev_blk = bytearray(cipher)
	prev_blk = bytearray(iv)
	text = b''
	for cipher in ciphers:
		prev_blk_save = prev_blk[:]
		for start in range(BLK_SIZE):
			prev_blk[start] = prev_blk[start] ^ 1
			if not check_padding(cipher, bytes(prev_blk)):
				break
			prev_blk[start] = prev_blk[start] ^ 1

		# no padding
		if start == 0:
			start = BLK_SIZE - 1

		# initial text
		text_blk = bytes([BLK_SIZE - start] * (BLK_SIZE - start - 1))
		for j in range(start, -1, -1):
			for ch in range(256):
				prev_blk[j] = ch
				if check_padding(cipher, bytes(prev_blk)):
					break
			text_blk = bytes([(BLK_SIZE - j) ^ prev_blk[j] ^ prev_blk_save[j]]) + text_blk
			for k in range(j, BLK_SIZE):
				prev_blk[k] = prev_blk[k] ^ (BLK_SIZE - j) ^ (BLK_SIZE - j + 1)

		text += text_blk
		prev_blk = bytearray(cipher)
	return pkcs7_unpadding(text)

if __name__ == '__main__':
	result = padding_oracle(check_padding).decode()
	print(result)
