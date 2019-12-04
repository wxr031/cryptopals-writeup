#!/usr/bin/env python3

import random
import os
from challenge9 import pkcs7_padding
from challenge10 import aes_encrypt_ecb, aes_encrypt_cbc

def encryption_oracle(text):
	if isinstance(text, str):
		text = text.encode()
	key = os.urandom(16)
	text = os.urandom(random.randint(5, 10)) + text + os.urandom(random.randint(5, 10))
	text = pkcs7_padding(text, (len(text) + 15) // 16 * 16)
	mode = random.randint(0, 1)
	if mode == 0:
		# Do ECB encryption
		return aes_encrypt_ecb(text, key)
	else:
		# Do CBC encryption
		return aes_encrypt_cbc(text, key, iv = os.urandom(16))
		
def detect_ecb_or_cbc(oracle):
	text = 'A' * (16 - 5 + 16 * 2)
	cipher = oracle(text)
	if cipher[17:32] == cipher[33:48]:
		return 'ECB'
	else:
		return 'CBC'

if __name__ == '__main__':
	result = detect_ecb_or_cbc(encryption_oracle)
	print(result)
