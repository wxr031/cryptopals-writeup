#!/usr/bin/env python3

def pkcs7_padding(message, length):
	if isinstance(message, str):
		message = message.encode()
	pl = length - (len(message) % length)
	return message + bytes([pl]) * pl

def pkcs7_unpadding(message):
	if isinstance(message, str):
		message = message.encode()
	return message[0 : len(message) - message[-1]]

if __name__ == '__main__':
	message = input()
	length = int(input())
	result = pkcs7_padding(message, length)
	print(result)
