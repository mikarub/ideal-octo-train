#!/usr/bin/env python3
# filename: mygame.py
# author: miklenn
# date: oktober 2025 (mostly based on interaction with ChatGPT 4 and 5)

import threading
import itertools
import time
import sys
import select, termios, tty

def key_pressed():
	dr, dw, de = select.select([sys.stdin], [], [], 0)
	return bool(dr)

def spinner(stop_event, pause_event, message="Waiting for input... "):
	"""
	This is the actual spinner function.
	"""
	spinner_cycle = itertools.cycle(['|', '/', '-', '\\'])
	fading = False
	
	while not stop_event.is_set():
		if not pause_event.is_set():
			sys.stdout.write('\r' + message + next(spinner_cycle))
			sys.stdout.flush()
			time.sleep(0.1)
		else:
			# Smooth fade-out
			if not fading:
				fading = True
				for delay in [0.15, 0.25, 0.35, 0.45, 0.55]:
					if stop_event.is_set(): break
					sys.stdout.write('\r' + message + next(spinner_cycle))
					sys.stdout.flush()
					time.sleep(delay)
			break
	sys.stdout.write('\r' + ' ' * (len(message) + 10) + '\r') # clear line

def spinner_input(prompt):
	"""
	Reusable input with spinner
	"""					
	stop_event = threading.Event()
	pause_event = threading.Event()
	spinner_thread = threading.Thread(target=spinner, args=(stop_event, pause_event))
	spinner_thread.start()

	sys.stdout.write(prompt)
	sys.stdout.flush()

	# Pause spinner once user starts typing
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
	return user_input

# Example interactive program
def run_wizard():
	print("=== Welcome to the Setup Wizard ===\n")
	
	name = spinner_input("What is your name? ")
	age = spinner_input("How old are you? ")
	hobby = spinner_input("What is your favourite hobby? ")
	fav_lang = spinner_input("Favourite programming language? ")
	
	print("\nProcessing your responses...\n")
	time.sleep(1)
	
	print(f"Pleased to meet you, {name}! You claim to be {age} years old while enjoying {hobby}.")
	print(f"Your favourite language is {fav_lang}.")
	print("Setup complete!")


if __name__ == "__main__":
	run_wizard()
	
	
	

