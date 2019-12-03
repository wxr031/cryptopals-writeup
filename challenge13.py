#!/usr/bin/env python3

import os
from challenge9 import pkcs7_padding, pkcs7_unpadding
from challenge10 import aes_encrypt_ecb, aes_decrypt_ecb
from Crypto.Cipher import AES

key = os.urandom(16)

def parsing_routine(string):
	items = (item.split(b'=') for item in string.split(b'&'))
	return {key: value for key, value in items}

def profile_for(email):
	if isinstance(email, str):
		email = email.encode()
	email = email.replace(b'&', b'').replace(b'=', b'')
	profile = b'email=' + email + b'&uid=10&role=user'
	return aes_encrypt_ecb(pkcs7_padding(profile, AES.block_size), key)

def profile_decode(cipher):
	return pkcs7_unpadding(aes_decrypt_ecb(cipher, key))

def ecb_cut_and_paste(profile_for):
	# email=AAAAAAAAAA
	#       ^^^^^^^^^^
	# admin\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11
	# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
	# AAA&uid=10&role=
	# ^^^
	# user\x12\x12\x12\x12\x12\x12\x12\x12\x12\x12\x12\x12
	payload = ('A' * 10) + ('admin' + '\x0b' * 0xb) + ('A' * 3)
	cipher1 = profile_for(payload)

	# reorder the cipher block to: 
	# email=AAAAAAAAAA
	# AAA&uid=10&role=
	# admin\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11

	cipher2 = cipher1[0:16] + cipher1[32:48] + cipher1[16:32]
	return profile_decode(cipher2)

if __name__ == '__main__':
	profile = ecb_cut_and_paste(profile_for)
	print(profile)
