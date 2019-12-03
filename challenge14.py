#!/usr/bin/env python3

import os, random
from base64 import b64decode
from itertools import takewhile

from challenge9 import pkcs7_padding, pkcs7_unpadding
from challenge10 import aes_encrypt_ecb, aes_decrypt_ecb

BLK_SIZE = 16

key = os.urandom(16)
prefix = os.urandom(random.randint(0, 255))
target = b64decode(b'Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK')


def oracle(text):
	if isinstance(text, str):
		text = text.encode()
	padded = pkcs7_padding(prefix + text + target, BLK_SIZE)
	return aes_encrypt_ecb(padded, key)

def match_prefix(str1, str2):
	return sum(1 for _ in takewhile(lambda pair: pair[0] == pair[1], zip(str1, str2)))

def byte_at_a_time_ecb_decryption(oracle):

	# find prefix length
	text1 = b'1'
	text2 = b'2'
	prepend_len = 0
	prefix_block = match_prefix(oracle(text1), oracle(text2)) // BLK_SIZE
	match_block = prefix_block
	
	while match_block <= prefix_block:
		prepend_len += 1
		text1 = b'0' + text1
		text2 = b'0' + text2
		cipher1 = oracle(text1)
		cipher2 = oracle(text2)
		match_block = match_prefix(cipher1, cipher2) // BLK_SIZE
	
	# find padding length
	prefix_len = match_block * BLK_SIZE - prepend_len
	pad_len = BLK_SIZE - (prefix_len) % BLK_SIZE

	# the rest is similar to challenge 12
	pad_str = b'A' * (pad_len + BLK_SIZE - 1)

	i = 0
	while True:
		cipher = oracle(b'A' * (pad_len + BLK_SIZE - 1 - (i % 16)))
		blk_id = match_block + (i // 16)
		target_blk = cipher[blk_id * BLK_SIZE : (blk_id + 1) * BLK_SIZE]
		for j in range(256):
			guess_str = b'A' * pad_len + pad_str[pad_len + i : pad_len + i + BLK_SIZE - 1] + bytes([j])
			guess_blk = oracle(guess_str)[match_block * BLK_SIZE : (match_block + 1) * BLK_SIZE]
			if target_blk == guess_blk:
				pad_str += bytes([j])
				break
		
		else:
			break
		i += 1
	return pkcs7_unpadding(pad_str[pad_len + BLK_SIZE - 1:])

if __name__ == '__main__':
	result = byte_at_a_time_ecb_decryption(oracle)
	print(result.decode())

