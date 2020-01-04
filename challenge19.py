#!/usr/bin/env python3

import curses
import string
from base64 import b64decode
from challenge18 import aes_decryption_ctr

myprintable = string.digits + string.ascii_letters + string.punctuation + ' '

texts = [
'SSBoYXZlIG1ldCB0aGVtIGF0IGNsb3NlIG9mIGRheQ==',
'Q29taW5nIHdpdGggdml2aWQgZmFjZXM=',
'RnJvbSBjb3VudGVyIG9yIGRlc2sgYW1vbmcgZ3JleQ==',
'RWlnaHRlZW50aC1jZW50dXJ5IGhvdXNlcy4=',
'SSBoYXZlIHBhc3NlZCB3aXRoIGEgbm9kIG9mIHRoZSBoZWFk',
'T3IgcG9saXRlIG1lYW5pbmdsZXNzIHdvcmRzLA==',
'T3IgaGF2ZSBsaW5nZXJlZCBhd2hpbGUgYW5kIHNhaWQ=',
'UG9saXRlIG1lYW5pbmdsZXNzIHdvcmRzLA==',
'QW5kIHRob3VnaHQgYmVmb3JlIEkgaGFkIGRvbmU=',
'T2YgYSBtb2NraW5nIHRhbGUgb3IgYSBnaWJl',
'VG8gcGxlYXNlIGEgY29tcGFuaW9u',
'QXJvdW5kIHRoZSBmaXJlIGF0IHRoZSBjbHViLA==',
'QmVpbmcgY2VydGFpbiB0aGF0IHRoZXkgYW5kIEk=',
'QnV0IGxpdmVkIHdoZXJlIG1vdGxleSBpcyB3b3JuOg==',
'QWxsIGNoYW5nZWQsIGNoYW5nZWQgdXR0ZXJseTo=',
'QSB0ZXJyaWJsZSBiZWF1dHkgaXMgYm9ybi4=',
'VGhhdCB3b21hbidzIGRheXMgd2VyZSBzcGVudA==',
'SW4gaWdub3JhbnQgZ29vZCB3aWxsLA==',
'SGVyIG5pZ2h0cyBpbiBhcmd1bWVudA==',
'VW50aWwgaGVyIHZvaWNlIGdyZXcgc2hyaWxsLg==',
'V2hhdCB2b2ljZSBtb3JlIHN3ZWV0IHRoYW4gaGVycw==',
'V2hlbiB5b3VuZyBhbmQgYmVhdXRpZnVsLA==',
'U2hlIHJvZGUgdG8gaGFycmllcnM/',
'VGhpcyBtYW4gaGFkIGtlcHQgYSBzY2hvb2w=',
'QW5kIHJvZGUgb3VyIHdpbmdlZCBob3JzZS4=',
'VGhpcyBvdGhlciBoaXMgaGVscGVyIGFuZCBmcmllbmQ=',
'V2FzIGNvbWluZyBpbnRvIGhpcyBmb3JjZTs=',
'SGUgbWlnaHQgaGF2ZSB3b24gZmFtZSBpbiB0aGUgZW5kLA==',
'U28gc2Vuc2l0aXZlIGhpcyBuYXR1cmUgc2VlbWVkLA==',
'U28gZGFyaW5nIGFuZCBzd2VldCBoaXMgdGhvdWdodC4=',
'VGhpcyBvdGhlciBtYW4gSSBoYWQgZHJlYW1lZA==',
'QSBkcnVua2VuLCB2YWluLWdsb3Jpb3VzIGxvdXQu',
'SGUgaGFkIGRvbmUgbW9zdCBiaXR0ZXIgd3Jvbmc=',
'VG8gc29tZSB3aG8gYXJlIG5lYXIgbXkgaGVhcnQs',
'WWV0IEkgbnVtYmVyIGhpbSBpbiB0aGUgc29uZzs=',
'SGUsIHRvbywgaGFzIHJlc2lnbmVkIGhpcyBwYXJ0',
'SW4gdGhlIGNhc3VhbCBjb21lZHk7',
'SGUsIHRvbywgaGFzIGJlZW4gY2hhbmdlZCBpbiBoaXMgdHVybiw=',
'VHJhbnNmb3JtZWQgdXR0ZXJseTo=',
'QSB0ZXJyaWJsZSBiZWF1dHkgaXMgYm9ybi4='
]

def fixed_nonce_aes_ctr():
	ciphers = [aes_decryption_ctr(b64decode(b64text), 0).decode('latin1') for b64text in texts]
	guesses = ['·' * len(cipher) for cipher in ciphers]
	stream_len = max(map(len, ciphers))
	stream = bytearray(b'\0' * stream_len)

	stdscr = curses.initscr()

	maxy, maxx = stdscr.getmaxyx()

	curses.noecho()
	curses.cbreak()
	stdscr.keypad(True)

	for i in range(maxy):
		stdscr.addstr(i, 0, guesses[i][0 : maxx - 1])
	
	curr_word = 0
	curr_index = 0

	curr_show_word = 0
	curr_show_index = 0

	while True:
		stdscr.move(curr_word - curr_show_word, curr_index - curr_show_index)
		ch = stdscr.getkey()

		redraw = False

		if ch == 'KEY_UP':
			if curr_word > 0:
				curr_word -= 1
				if curr_word - curr_show_word < 0:
					redraw = True
					curr_show_word -= 1
				if curr_index >= len(guesses[curr_word]):
					curr_index = len(guesses[curr_word]) - 1
					if curr_index < curr_show_index:
						curr_show_index = curr_index
					
		elif ch == 'KEY_DOWN':
			if curr_word < len(guesses) - 1:
				curr_word += 1
				if curr_word - curr_show_word >= maxy:
					redraw = True
					curr_show_word += 1
				if curr_index >= len(guesses[curr_word]):
					curr_index = len(guesses[curr_word]) - 1
					if curr_index < curr_show_index:
						curr_show_index = curr_index

		elif ch == 'KEY_LEFT':
			if curr_index > 0:
				curr_index -= 1
				if curr_index - curr_show_index < 0:
					redraw = True
					curr_show_index -= 1

		elif ch == 'KEY_RIGHT':
			if curr_index < len(guesses[curr_word]) - 1:
				curr_index += 1
				if curr_index - curr_show_index >= maxx - 1:
					redraw = True
					curr_show_index += 1

		elif ch == 'KEY_BACKSPACE':
			redraw = True
			stream[curr_index] = 0
			for i in range(len(guesses)):
				if curr_index < len(guesses[i]):
					guesses[i] = guesses[i][: curr_index] + '·' + guesses[i][curr_index + 1 :]

		elif ch == chr(27):
			return
				
		elif ch in myprintable:
			redraw = True
			stream[curr_index] = ord(ch) ^ ord(ciphers[curr_word][curr_index])
			for i in range(len(guesses)):
				if curr_index < len(guesses[i]):
					gch = chr(stream[curr_index] ^ ord(ciphers[i][curr_index]))
					if gch not in myprintable:
						gch = '·'
					guesses[i] = guesses[i][: curr_index] + gch + guesses[i][curr_index + 1 :]

			
		if redraw:
			stdscr.clear()			
			for i in range(maxy):
				stdscr.addstr(i, 0, guesses[curr_show_word + i][curr_show_index : curr_show_index + maxx - 1])

	curses.endwin()

if __name__ == '__main__':
	fixed_nonce_aes_ctr()
