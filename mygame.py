#!/usr/bin/env python3
# filename: mygame.py
# author: miklenn
# date: oktober 2025 (mostly based on interaction with ChatGPT 4 and 5)

import sys
import threading
import itertools
import time
import random
from colorama import init, Fore, Style

init(autoreset=True)

# --- Cross-platform key detection ---
try:
	import msvcrt
	def key_pressed():
		return msvcrt.kbhit()
except ImportError:
	import select
	def key_pressed():	
		dr, dw, de = select.select([sys.stdin], [], [], 0)
		return bool(dr)

# --- Spinner styles ---
SPINNER_STYLES = [
    ['|', '/', '-', '\\'],                  # classic line
    ['⠋','⠙','⠹','⠸','⠼','⠴','⠦','⠧','⠇','⠏'],  # Braille dots
    ['◐','◓','◑','◒'],                    # quarter circles
    ['←','↖','↑','↗','→','↘','↓','↙'],     # arrow wheel
    ['▁','▃','▄','▅','▆','▇','▆','▅','▄','▃'],  # bounce bar
    ['.  ', '.. ', '...', ' ..', '  .', '   ']   # dot pulse
]

# --- Theme definitions ---
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

# --- Spinner thread function ---
def spinner(stop_event,  message, style, color, pause_event=None):
	spinner_cycle = itertools.cycle(style)
	
	while not stop_event.is_set():
		if pause_event and pause_event.is_set():
			time.sleep(0.05)
			continue
		sys.stdout.write('\r' + color + message + next(spinner_cycle) + Style.RESET_ALL)
		sys.stdout.flush()
		time.sleep(0.1)
	sys.stdout.write('\r' + ' ' * (len(message)+2) + '\r') # clear line

# --- Animated prompt typing ---
def animated_prompt(prompt_text, theme):
	style = random.choice(SPINNER_STYLES)
	color = random.choice(theme["spinner_colors"])
	stop_event = threading.Event()
	pause_event = threading.Event()
	
	spinner_thread = threading.Thread(target=spinner, args=(stop_event, "", style, color, pause_event))
	spinner_thread.start()
	
	typed = ""
	for char in prompt_text:
		typed += char
		pause_event.set() # Stop spinner while typing character
		sys.stdout.write(theme["prompt_color"] + typed + Style.RESET_ALL)
		sys.stdout.flush()
		time.sleep(0.05) # typing speed
		sys.stdout.write('\r')
	stop_event.set()
	spinner_thread.join()
	sys.stdout.write(theme["prompt_color"] + typed + Style.RESET_ALL)
	return typed

# --- Reusable input with spinner ---
def spinner_input(prompt_text, theme):					
	animated_prompt(prompt_text, theme)
	stop_event = threading.Event()
	pause_event = threading.Event()
	
	style = random.choice(SPINNER_STYLES)
	color = random.choice(theme["spinner_colors"])
	spinner_thread = threading.Thread(target=spinner, args=(stop_event, "Waiting for input... ", style, color))
	spinner_thread.start()

	# Pause spinner once user starts typing
	while True:
		if key_pressed():
			break
		time.sleep(0.05)

	# Then actually get input normally
	user_input = input() # Standard input

	# Stop the spinner
	stop_event.set()
	spinner_thread.join()
	return user_input

# --- Interactive theme selection ---
def select_theme():
	print("Choose a theme for your wizard:")
	for i, theme_name in enumerate(THEMES.keys(), start=1):
		print(f"  {i}. {theme_name.title()}")
		
	while True:
		choice = input("Enter the number of your theme: ").strip()
		if choice.isdigit() and 1 <= int(choice) <= len(THEMES):
			selected = list(THEMES.keys())[int(choice)-1]
			print(f"Selected theme: {selected.title()}\n")
			return THEMES[selected]
		else:
			print("Invalid choice. Please enter a number from the list.")
	
# --- Animated intro ---
def animated_intro(theme):
	message = " Welcome to the Wizard! "
	style = random.choice(SPINNER_STYLES)
	color = random.choice(theme["spinner_colors"])
	stop_event = threading.Event()
	thread = threading.Thread(target=spinner, args=(stop_event, message, style, color))
	thread.start()
	time.sleep(2) # Show animation for 2 seconds
	stop_event.set()
	thread.join()
	print(theme["accent"] + "\nLet's get started!\n" + Style.RESET_ALL)

# --- Animated outro ---
def animated_outro(theme):
	message = " Closing Wizard... "
	style = random.choice(SPINNER_STYLES)
	color = random.choice(theme["spinner_colors"])
	stop_event = threading.Event()
	thread = threading.Thread(target=spinner, args=(stop_event, message, style, color))
	thread.start()
	time.sleep(2) # Show animation for 2 seconds
	stop_event.set()
	thread.join()
	print(theme["accent"] + "\nGoodbye!\n" + Style.RESET_ALL)

# --- Main wizard loop ---
def run_wizard(theme):
	animated_intro(theme)
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
		
	animated_outro(theme)

# --- Run program ---
if __name__ == "__main__":
	chosen_theme = select_theme()
	run_wizard(chosen_theme)
