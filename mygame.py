#!/usr/bin/env python3
# filename: mygame.py
# author: miklenn
# date: oktober 2025 (mostly based on interaction with ChatGPT 4 and 5)

import threading
import itertools
import time
import sys
import select, termios, tty
import random
from colorama import init, Fore, Style

SPINNER_STYLES = [
    ['|', '/', '-', '\\'],                  # classic line
    ['⠋','⠙','⠹','⠸','⠼','⠴','⠦','⠧','⠇','⠏'],  # Braille dots
    ['◐','◓','◑','◒'],                    # quarter circles
    ['←','↖','↑','↗','→','↘','↓','↙'],     # arrow wheel
    ['▁','▃','▄','▅','▆','▇','▆','▅','▄','▃'],  # bounce bar
    ['.  ', '.. ', '...', ' ..', '  .', '   ']   # dot pulse
]

SPINNER_COLORS = [Fore.CYAN, Fore.MAGENTA, Fore.YELLOW, Fore.GREEN, Fore.BLUE, Fore.WHITE]

def key_pressed():
	dr, dw, de = select.select([sys.stdin], [], [], 0)
	return bool(dr)

def spinner(stop_event, pause_event, message="Waiting for input... ", style=None, color=Fore.CYAN):
	"""
	This is the actual spinner function.
	"""
	spinner_cycle = itertools.cycle(style or SPINNER_STYLES[0])
	fading = False
	
	while not stop_event.is_set():
		if not pause_event.is_set():
			sys.stdout.write('\r' + color + message + next(spinner_cycle) + Style.RESET_ALL)
			sys.stdout.flush()
			time.sleep(0.1)
		else:
			# Smooth fade-out
			if not fading:
				fading = True
				for delay in [0.15, 0.25, 0.35, 0.45, 0.55]:
					if stop_event.is_set(): break
					sys.stdout.write('\r' + color + message + next(spinner_cycle) + Style.RESET_ALL)
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
	style = random.choice(SPINNER_STYLES)
	color = random.choice(SPINNER_COLORS)
	spinner_thread = threading.Thread(target=spinner, args=(stop_event, pause_event, "Waiting for input", style, color))
	spinner_thread.start()

	sys.stdout.write(Fore.CYAN + prompt + Style.RESET_ALL)
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

# Main interactive loop
def run_wizard():
	print(Fore.GREEN + "=== Dynamic Color Spinner Wizard ===" + Style.RESET_ALL)
	print(Fore.WHITE + "(Type 'exit' anytime to quit)\n")
	
	while True:
		name = spinner_input("What is your name? ")
		if name.lower() == "exit": break
		
		age = spinner_input("How old are you? ")
		if age.lower() == "exit": break
		
		hobby = spinner_input("What is your favourite hobby? ")
		if hobby.lower() == "exit": break
		
		fav_lang = spinner_input("Favourite programming language? ")
		if fav_lang.lower() == "exit": break
	
		print(Fore.YELLOW + "\nProcessing your responses...\n" + Style.RESET_ALL)
		time.sleep(1.2)
	
		print(Fore.GREEN + f"✅ Pleased to meet you, {name}! You claim to be {age} years old while enjoying {hobby}." + Style.RESET_ALL)
		print(Fore.CYAN + f"✨ Your favourite language is {fav_lang}.")
		print("n\👋Let's go again! (or type 'exit' to quit)\n")
		
	print("\nGoodbye!")


if __name__ == "__main__":
	run_wizard()
	
	
	

