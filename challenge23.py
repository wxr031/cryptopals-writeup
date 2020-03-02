#!/usr/bin/env python3

import z3

from challenge21 import seed_mt, extract_number

def untemper(y):
	y0 = z3.BitVec('y0', 32)
	y1 = z3.BitVec('y1', 32)
	y2 = z3.BitVec('y2', 32)
	y3 = z3.BitVec('y3', 32)

	equ = [
		y1 == y0 ^ ((z3.LShR(y0, 11)) & 0xffffffff),
		y2 == y1 ^ ((y1 << 7) & 0x9d2c5680),
		y3 == y2 ^ ((y2 << 15) & 0xefc60000),
		y == y3 ^ (z3.LShR(y3, 18))
	]

	solver = z3.Solver()
	solver.add(equ)
	assert solver.check() == z3.z3.CheckSatResult(z3.Z3_L_TRUE)
	return solver.model()[y0].as_long()

def solve(result):
	mt = [untemper(result[i]) for i in range(624)]
	print('mymt', mt)

	def gen_next(mt):
		index = 625
		def twist():
			nonlocal index
			for i in range(624):
				x = (mt[i] & 0x80000000) + (mt[(i + 1) % 624] & 0x7fffffff)
				xA = x >> 1
				if x % 2 == 1:
					xA = xA ^ 0x9908b0df
				mt[i] = mt[(i + 397) % 624] ^ xA
			index = 0
		
		def extract():
			nonlocal index
			if index >= 624:
				twist()
			y = mt[index]
			y = y ^ ((y >> 11) & 0xffffffff)
			y = y ^ ((y << 7) & 0x9d2c5680)
			y = y ^ ((y << 15) & 0xefc60000)
			y = y ^ (y >> 18)
			yield y

			index += 1

		return extract()
		
	return gen_next(mt)


if __name__ == '__main__':
	seed = 1024
	seed_mt(1024)
	result = [extract_number() for i in range(624)]
	gen = solve(result)
	
