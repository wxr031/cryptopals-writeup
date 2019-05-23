#!/usr/bin/env python3

from challenge3 import single_byte_xor

with open('4.txt', 'r') as f:
	global ciphers
	ciphers = f.read().split()

count = 0
for cipher in ciphers:
	decode = single_byte_xor(cipher)
	if decode != '':
		print(count, decode)
		count += 1
