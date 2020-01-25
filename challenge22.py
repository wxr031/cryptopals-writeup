#!/usr/bin/env python3

import time
import random

from challenge21 import seed_mt, extract_number

def get_nonce():
	current = int(time.time())
	wait0 = random.randint(40, 60)
	time.sleep(wait0)

	seed = current + wait0
	seed_mt(seed)
	nonce = extract_number()

	wait1 = random.randint(40, 60)
	time.sleep(wait1)
	
	return nonce

if __name__ == '__main__':
	nonce = get_nonce()
	output_time = int(time.time())
	for i in range(40, 60):
		output_time_test = output_time - i
		seed_mt(output_time_test)
		if extract_number() == nonce:
			print(output_time_test)
			break
