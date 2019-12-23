#!/usr/bin/env python3

import base64
from Crypto.Cipher import AES

from challenge6 import xor_bytes

BLK_SIZE = 16
key = b'YELLOW SUBMARINE'


def aes_decryption_ctr(cipher, nonce):
	ciphers = [cipher[i : i + BLK_SIZE] for i in range(0, len(cipher), BLK_SIZE)]
	for i in range(len(ciphers)):
		aes = AES.new(key, AES.MODE_ECB)
		counter = nonce.to_bytes(BLK_SIZE // 2, byteorder = 'little')
		counter += i.to_bytes(BLK_SIZE // 2, byteorder = 'little')
		counter_enc = aes.encrypt(counter)
		ciphers[i] = xor_bytes(ciphers[i], counter_enc)
	return b''.join(ciphers)

if __name__ == '__main__':
	cipher_b64 = 'L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ=='
	cipher = base64.b64decode(cipher_b64)
	print(aes_decryption_ctr(cipher, 0))
