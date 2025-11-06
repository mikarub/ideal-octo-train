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
def spinner(stop_event,  message, style, color):
	spin = itertools.cycle(style)
	while not stop_event.is_set():
		sys.stdout.write('\r' + color + message + next(spin) + Style.RESET_ALL)
		sys.stdout.flush()
		time.sleep(0.1)
	sys.stdout.write('\r' + ' ' * (len(message)+2) + '\r') # clear line


# --- Animated text output ---
def animated_text(text, color=Fore.WHITE, speed=0.03):
	for c in text:
		sys.stdout.write(color + c + Style.RESET_ALL)
		sys.stdout.flush()
		time.sleep(speed)
	print() # new line after text

# --- Animated sparkle effect for success/warning/info ---
def animated_effect(text, effect_type="success"):
	symbols = ["✦", "✧", "★", "☆", "✪", "✫"]
	color = {"succes": Fore.GREEN, "warning": Fore.YELLOW, "info": Fore.CYAN}.get(effect_type, Fore.WHITE)
	for char in text:
		sys.stdout.write(color + char + Style.RESET_ALL)
		sys.stdout.flush()
		time.sleep(0.03)
		if random.random() < 0.1:
			sys.stdout.write(color + random.choice(symbols) + Style.RESET_ALL)
			sys.stdout.flush()
			time.sleep(0.02)
	print()
	
# --- Reusable input with spinner ---
def spinner_input(prompt_text, theme):					
	animated_text(prompt_text, color=theme["prompt_color"])
	stop_event = threading.Event()
	style = random.choice(SPINNER_STYLES)
	color = random.choice(theme["spinner_colors"])
	t = threading.Thread(target=spinner, args=(stop_event, "Waiting for input...", style, color))
	t.start()
	user_input = input()
	stop_event.set()
	t.join()
	return user_input.strip().lower()

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
	animated_text(" Welcome to the Interactive Wizard! ", color=random.choice(theme["spinner_colors"]))
	time.sleep(0.5) 
	animated_text("Your choices will shape the story.\n", color=theme["accent"])
	
# --- Animated outro ---
def animated_outro(theme):
	animated_text("\nClosing Wizard...", color=random.choice(theme["spinner_colors"]))
	time.sleep(0.5)
	animated_text("Goodbye!\n", color=theme["accent"])

# --- Main wizard loop ---
def run_wizard(theme):
	animated_intro(theme)
	print(theme["text_color"] + "(Type 'exit' anytime to quit)\n")
	
	while True:
		name = spinner_input(" What is your name? ", theme)
		if name.lower() == "exit": break
		
		choice1 = spinner_input(f"Hello {name}! Choose a path: [forest/city] ", theme)
		if choice1 == "forest":
			animated_effect("You venture info a mysterious forest...", "info")
			choice2 = spinner_input("You see a glowing tree. Do you approach it? [yes/no] ", theme)
			if choice2 == "yes":
				animated_effect("Magic sparkles surround you! You've unlocked a secret!", "success")
			else:
				animated_effect("You walk past safely, but feel something missed.", "warning")
		elif choice1 == "city":
			animated_effect("You enter a bustling cyberpunk city...", "info")
			choice2 = spinner_input("A hacker offers you a deal. Accept? [yes/no] ", theme)
			if choice2 == "yes":
				animated_effect("You gain secret hacking skills! ", "success")
			else:
				animated_effect("You walk away, blending into the crowd.", "warning")
		else:
			animated_effect("Invalid path, the story pauses.", "warning")
			
		cont = spinner_input("Do you want to play another story? [yes/no] ", theme)
		if cont != "yes": break
		
	animated_outro(theme)

# --- Run program ---
if __name__ == "__main__":
	chosen_theme = select_theme()
	run_wizard(chosen_theme)
