#!/usr/bin/env python3
# filename: mygame.py
# author: miklenn
# date: oktober 2025 (mostly based on interaction with ChatGPT 4 and 5)

import threading
import itertools
import time
import sys

def spinner(stop_event):
	spinner_cycle = itertools.cycle(['|', '/', '-', '\\'])
	while not stop_event.is_set():
		sys.stdout.write('\rWaiting for input...' + next(spinner_cycle))
		sys.stdout.flush()
		time.sleep(0.1)
	sys.stdout.write('\r') # clear line when done
	
# Create a stop event for the spinner
stop_event = threading.Event()
spinner_thread = threading.Thread(target=spinner, args=(stop_event,))

# Start the spinner
spinner_thread.start()

# Wait for user input
user_input = input(" Please type something: ")

# Stop the spinner
stop_event.set()
spinner_thread.join()

print(f"You typed: {user_input}")


