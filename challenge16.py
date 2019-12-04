#!/usr/bin/env python3

import os
from Crypto.Cipher import AES
from challenge6 import xor_bytes
from challenge9 import pkcs7_padding, pkcs7_unpadding
from challenge15 import pkcs7_validation

BLK_SIZE = 16
key = os.urandom(16)

def parsing_routine(string):
	items = [item.split(b'=') for item in string.split(b';')]
	return {key: value for key, value in items}

def aes_encrypt_cbc(text, key, iv):
	aes = AES.new(key, AES.MODE_CBC, iv)
	return aes.encrypt(text)

def aes_decrypt_cbc(cipher, key, iv):
	aes = AES.new(key, AES.MODE_CBC, iv)
	return aes.decrypt(cipher)

def pending(text):
	if isinstance(text, str):
		text = text.encode()
	text = text.replace(b';', b'%3B').replace(b'=', b'%3D')
	text = b'comment1=cooking%20MCs;userdata=' + text + b';comment2=%20like%20a%20pound%20of%20bacon'
	text = pkcs7_padding(text, BLK_SIZE)
	iv = os.urandom(BLK_SIZE)
	cipher = aes_encrypt_cbc(text, key, iv)
	return cipher, iv

def check_admin(cipher, iv):
	if isinstance(cipher, str):
		cipher = cipher.encode()
	if isinstance(iv, str):
		iv = iv.encode()
	text = aes_decrypt_cbc(cipher, key, iv)
	if not pkcs7_validation(text):
		return False
	text = pkcs7_unpadding(text)
	parsed = parsing_routine(text)
	return parsed[b'admin'] == b'true'

def cbc_bitflipping_attack(pending):
	payload = b'AAAAABadminBtrue'
	payload2 = b'AAAAA;admin=true'
	cipher, iv = pending(payload)
	change_blk = cipher[BLK_SIZE : 2 * BLK_SIZE]
	flip_bits = xor_bytes(payload, payload2)
	flipped_blk = xor_bytes(change_blk, flip_bits)
	cipher = cipher[0 : BLK_SIZE] + flipped_blk + cipher[2 * BLK_SIZE :]
	return check_admin(cipher, iv)


if __name__ == '__main__':
	result = cbc_bitflipping_attack(pending)
	print(result)
