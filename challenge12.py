#!/usr/bin/env python3

import os
from challenge9 import pkcs7_padding, pkcs7_unpadding
from base64 import b64encode, b64decode
from Crypto.Cipher import AES

key = os.urandom(16)

append_str = b64decode(b'Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK')

def oracle(text):
	if isinstance(text, str):
		text = text.encode()
	aes = AES.new(key, AES.MODE_ECB)
	text += append_str
	text = pkcs7_padding(text, 16)
	return aes.encrypt(text)

def detect_ecb(oracle, blk_size):
	pad_blk = len(oracle('')) // blk_size
	cipher = oracle('A' * blk_size * pad_blk)
	ciphers = [cipher[i : i + blk_size] for i in range(0, len(cipher), blk_size)]
	diff = len(ciphers) - len(set(ciphers))
	return diff != 0

def block_size(oracle):
	len0 = len(oracle(''))
	i = 1
	while True:
		len1 = len(oracle('A' * i))
		if len1 != len0:
			return len1 - len0
		i += 1

def byte_at_a_time_ecb_decryption():
	blk_size = block_size(oracle)
	assert detect_ecb(oracle, blk_size)
	pad_str = b'A' * (blk_size - 1) # AAA...A?
	i = 0
	while True:
		cipher = oracle('A' * (blk_size - 1 - (i % blk_size)))
		cipher_blk_id = i // blk_size
		cipher_blk = cipher[cipher_blk_id * blk_size : (cipher_blk_id + 1) * blk_size]
		for j in range(0xff):
			guess_str = (pad_str + bytes([j]))[i : i + blk_size]
			guess_blk = oracle(guess_str)[0 : blk_size]
			if cipher_blk == guess_blk:
				pad_str += bytes([j])
				break
		else:
			break
		i += 1
	return pkcs7_unpadding(pad_str[blk_size - 1:])
		
if __name__ == '__main__':
	result = byte_at_a_time_ecb_decryption()
	print(result.decode())
