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

# SPINNER_COLORS = [Fore.CYAN, Fore.MAGENTA, Fore.YELLOW, Fore.GREEN, Fore.BLUE, Fore.WHITE]

THEMES = {
    "cyberpunk": {
        "spinner_colors": [Fore.MAGENTA, Fore.CYAN, Fore.YELLOW],
        "prompt_color": Fore.CYAN,
        "text_color": Fore.WHITE,
        "accent": Fore.MAGENTA
    },
    "nature": {
        "spinner_colors": [Fore.GREEN, Fore.YELLOW, Fore.WHITE],
        "prompt_color": Fore.GREEN,
        "text_color": Fore.WHITE,
        "accent": Fore.YELLOW
    },
    "matrix": {
        "spinner_colors": [Fore.GREEN],
        "prompt_color": Fore.GREEN,
        "text_color": Fore.LIGHTBLACK_EX,
        "accent": Fore.LIGHTGREEN_EX
    },
    "classic": {
        "spinner_colors": [Fore.WHITE],
        "prompt_color": Fore.WHITE,
        "text_color": Fore.WHITE,
        "accent": Fore.CYAN
    }
}

def key_pressed():
	dr, dw, de = select.select([sys.stdin], [], [], 0)
	return bool(dr)

def spinner(stop_event, pause_event, message="Waiting for input... ", style=None, color=Fore.CYAN):
	"""
	This is the actual spinner thread function.
	"""
	spinner_cycle = itertools.cycle(style)
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

def spinner_input(prompt, theme):
	"""
	Reusable input with spinner
	"""					
	stop_event = threading.Event()
	pause_event = threading.Event()
	
	style = random.choice(SPINNER_STYLES)
	color = random.choice(theme["spinner_colors"])
	spinner_thread = threading.Thread(target=spinner, args=(stop_event, pause_event, "Waiting for input ", style, color))
	spinner_thread.start()

	sys.stdout.write(theme["prompt_color"] + prompt + Style.RESET_ALL)
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
def run_wizard(theme_name="cyberpunk"):
	theme = THEMES.get(theme_name.lower(), THEMES["classic"])
	
	print(theme["accent"] + f"=== {theme_name.title()} Spinner Wizard ===" + Style.RESET_ALL)
	print(theme["text_color"] + "(Type 'exit' anytime to quit)\n")
	
	while True:
		name = spinner_input(" What is your name? ", theme)
		if name.lower() == "exit": break
		
		age = spinner_input(" How old are you? ", theme)
		if age.lower() == "exit": break
		
		hobby = spinner_input(" What is your favourite hobby? ", theme)
		if hobby.lower() == "exit": break
		
		fav_lang = spinner_input(" Favourite programming language? ", theme)
		if fav_lang.lower() == "exit": break
	
		print(theme["accent"] + "\nProcessing your responses...\n" + Style.RESET_ALL)
		time.sleep(1.2)
	
		print(theme["text_color"] + f"✅ Pleased to meet you, {name}! You claim to be {age} years old while enjoying {hobby}.")
		print(f"✨ Your favourite language is {fav_lang}." + Style.RESET_ALL)
		print(theme["accent"] + "\nLet's go again! (or type 'exit' to quit)\n" + Style.RESET_ALL)
		
	print(theme["accent"] + "\nGoodbye!" + Style.RESET_ALL)


if __name__ == "__main__":
	# Choose a theme here: "cyberpunk", "nature", "matrix" or "classic"
	run_wizard("classic")

