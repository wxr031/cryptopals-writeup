#!/usr/bin/env python3

def pkcs7_validation(text):
	if isinstance(text, str):
		text = text.encode()
	last = text[-1]
	return bytes([last]) * last == text[-last:]

if __name__ == '__main__':
	string = 'ICE ICE BABY\x04\x04\x04\x04\x04'
	print(pkcs7_validation(string))
