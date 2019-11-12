#!/usr/bin/env python3

def pkcs7_padding(message, length):
	if isinstance(message, str):
		message = message.encode()
	pl = length - len(message)
	return message + bytes([pl]) * pl

if __name__ == '__main__':
	message = input()
	length = int(input())
	result = pkcs7_padding(message, length)
	print(repr(result))
