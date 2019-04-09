#!/usr/bin/env python3

from string import hexdigits

def fixed_xor(string1, string2):
	assert len(string1) == len(string2)
	assert all(c in hexdigits for c in string1)
	assert all(c in hexdigits for c in string2)

	xor = lambda ct: format(int(ct[0], 16) ^ int(ct[1], 16), 'x')
	return ''.join(map(xor, (ct for ct in zip(string1, string2))))

if __name__ == '__main__':
	string1 = input()
	string2 = input()
	print(fixed_xor(string1, string2))
