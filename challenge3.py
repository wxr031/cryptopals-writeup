#!/usr/bin/env python3

from string import hexdigits, printable, ascii_letters
from numpy import corrcoef

def freq_corr(cipher):
	if isinstance(cipher, bytes):
		cipher = cipher.decode()
	# frequency of letter A-Z in English
	letter_freq_en = [
		0.08167, 0.01492, 0.02782, 0.04253, 0.012702, 0.02228, 0.02015, 0.06094, 0.06966, 0.00153, 0.00772, 0.04025, 0.02406, 0.06749, 0.07507, 0.01929, 0.00095, 0.05987, 0.06327, 0.09056, 0.02758, 0.00978, 0.02360, 0.00150, 0.01974, 0.00074
	]
	freq = [0] * 26
	for c in cipher:
		if c in ascii_letters:
			freq[ord(c.lower()) - ord('a')] += 1
	freq = list(map(lambda x: x / len(cipher), freq))
	return corrcoef(letter_freq_en, freq)[0][1]

def single_byte_xor(string):
	if isinstance(string, bytes):
		string = string.decode()
	assert len(string) > 1 and len(string) % 2 == 0
	assert all(c in hexdigits for c in string)

	cipher = bytes.fromhex(string)
	max_r = -1
	result = ''
	for k in range(0x0, 0x100):
		xor = lambda c: bytes([k ^ c]).decode('latin1')
		text = ''.join(map(xor, (c for c in cipher)))
		if all(c in printable for c in text):
			r = freq_corr(text)
			if r > max_r:
				max_r, result = r, text
	
	return result

if __name__ == '__main__':
	string = input()
	print(single_byte_xor(string))
