#!/usr/bin/env python3

from operator import itemgetter

def detect_ecb(ciphers):
	different = {}
	for cipher in ciphers:
		chunks = [cipher[i:i + 32] for i in range(0, len(cipher), 32)]
		different[cipher] = len(chunks) - len(set(chunks))
	return sorted([(cipher, diff) for cipher, diff in different.items()], key = itemgetter(1), reverse = True)[0][0]


if __name__ == '__main__':
	with open('8.txt') as f:
		global ciphers
		ciphers = f.read().split()
	
	cipher = detect_ecb(ciphers)
	print(cipher)
	
