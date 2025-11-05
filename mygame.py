#!/usr/bin/env python3
# filename: mygame.py
# author: miklenn
# date: oktober 2025 (mostly based on interaction with ChatGPT 4 and 5)

import threading
import itertools
import time
import sys

# Detect keypresses cross-platform
try:
	import msvcrt # in case anyone on windows ever use this code
	def key_pressed():
		return msvcrt.kbhit()
except ImportError:
	import select, termios, tty # Unix
	import sys
	def key_pressed():
		dr, dw, de = select.select([sys.stdin], [], [], 0)
		return bool(dr)

def spinner(stop_event, pause_event):
	"""
	This is the actual spinner.
	"""
	spinner_cycle = itertools.cycle(['|', '/', '-', '\\'])
	while not stop_event.is_set():
		if not pause_event.is_set():
			sys.stdout.write('\rWaiting for input...' + next(spinner_cycle))
			sys.stdout.flush()
		time.sleep(0.1)
	sys.stdout.write('\r' + ' ' * 40 + '\r') # clear line
	
stop_event = threading.Event()
pause_event = threading.Event()
spinner_thread = threading.Thread(target=spinner, args=(stop_event, pause_event))

# Start the spinner
spinner_thread.start()

# Check for typing while waiting for input
user_input = ''
sys.stdout.write("Please type something: ")
sys.stdout.flush()

while True:
	if key_pressed():
		pause_event.set() # Pause spinner
	try:
		user_input = input() # Standard input
		break
	except KeyboardInterrupt:
		break

# Stop the spinner
stop_event.set()
spinner_thread.join()

print(f"You typed: {user_input}")


