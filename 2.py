#!/usr/bin/env python3

from string import hexdigits

string1 = input()
string2 = input()

assert len(string1) == len(string2)
assert all(c in hexdigits for c in string1)
assert all(c in hexdigits for c in string2)

xor = lambda ct: format(int(ct[0], 16) ^ int(ct[1], 16), 'x')
result = ''.join(map(xor, (ct for ct in zip(string1, string2))))

print(result)
