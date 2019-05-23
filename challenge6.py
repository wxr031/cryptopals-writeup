#!/usr/bin/env python3

from base64 import b64decode
from binascii import hexlify
from challenge3 import single_byte_xor, freq_corr


def hamming_distance(word0, word1):
	word0, word1 = word0.encode(), word1.encode()
	xor_word = bytes([bit0 ^ bit1 for bit0, bit1 in zip(word0, word1)])
	xor_word_bin = format(int.from_bytes(xor_word, byteorder = 'big'), 'b')
	return xor_word_bin.count('1')

def break_repeating_xor(cipher, poss_keynum = 3):
	poss_keysize = {}
	for keysize in range(2, 40):
		blocksize = len(cipher) // keysize
		blocks = [cipher[i:i + keysize] for i in range(0, len(cipher), keysize)]
		dist = sum([hamming_distance(blocks[i], blocks[i + 1]) for i in range(blocksize - 1)])
		avg_dist = dist / blocksize / keysize
		poss_keysize[avg_dist] = keysize

	poss_keysize = sorted(poss_keysize.items(), key = lambda pair: pair[0])[:poss_keynum]
	poss_plaintext = []
	for dist, keysize in poss_keysize:
		solved_parts = []
		for i in range(keysize):
			part = ''.join([cipher[j] for j in range(i, len(cipher), keysize)])
			solved_part = single_byte_xor(hexlify(part.encode()).decode())
			solved_parts.append(solved_part)

		plaintext = ''.join([''.join(i) for i in zip(*solved_parts)])
		if len(plaintext) != 0:
			poss_plaintext.append(plaintext)

	return sorted(poss_plaintext, key = freq_corr)[0]
	
		
if __name__ == '__main__':
	with open('6.txt') as f:
		global cipher
		cipher = f.read()
	cipher = b64decode(cipher.encode()).decode('latin1')
	result = break_repeating_xor(cipher)
	print(result)
