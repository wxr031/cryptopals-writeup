#!/usr/bin/env python3

w, n, m, r = 32, 624, 397, 31
a = 0x9908b0df
u, d = 11, 0xffffffff
s, b = 7, 0x9d2c5680
t, c = 15, 0xefc60000
l = 18
f = 1812433253

lower_mask = 0x7fffffff
upper_mask = 0x80000000

mt = [0 for i in range(n)]
index = n + 1

def seed_mt(seed = 0):
	global index
	index = n
	mt[0] = seed;
	for i in range(1, n):
		mt[i] = (f * (mt[i - 1] ^ (mt[i - 1] >> (w - 2))) + i) & d

def twist():
	global index
	for i in range(n):
		x = (mt[i] & upper_mask) + (mt[(i + 1) % n] & lower_mask)
		xA = x >> 1
		if x % 2 == 1:
			xA = xA ^ a
		mt[i] = mt[(i + m) % n] ^ xA

	index = 0

def extract_number():
	global index

	if index >= n:
		if index >= n + 1:
			seed_mt(5489)
		twist()
	
	y = mt[index]
	y = y ^ ((y >> u) & d)
	y = y ^ ((y << s) & b)
	y = y ^ ((y << t) & c)
	y = y ^ (y >> l)

	index += 1
	return y & d

if __name__ == '__main__':
	seed_mt()
	for i in range(16):
		print(extract_number())

