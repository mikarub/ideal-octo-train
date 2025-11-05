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
	speed = 0.1
	fading = False
	
	while not stop_event.is_set():
		if not pause_event.is_set():
			sys.stdout.write('\rWaiting for input... ' + next(spinner_cycle))
			sys.stdout.flush()
			time.sleep(speed)
		else:
			if not fading:
				fading = True
				for delay in [0.15, 0.25, 0.35, 0.45, 0.55]:
					if stop_event.is_set():
						break
					sys.stdout.write('\rWaiting for input... ' + next(spinner_cycle))
					sys.stdout.flush()
					time.sleep(delay)
			break
	sys.stdout.write('\r' + ' ' * 40 + '\r') # clear line
					
	
stop_event = threading.Event()
pause_event = threading.Event()
spinner_thread = threading.Thread(target=spinner, args=(stop_event, pause_event))
spinner_thread.start()

sys.stdout.write("Please type something: ")
sys.stdout.flush()

# Watch for user typing
while True:
	if key_pressed():
		pause_event.set() # Triggers fade-out
		break
	time.sleep(0.05)

# Then actually get input normally
user_input = input() # Standard input

# Stop the spinner
stop_event.set()
spinner_thread.join()

print(f"You typed: {user_input}")


