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
	def read_key():
		return msvcrt.kbhit()
except ImportError:
	import select, tty, termios
	def key_pressed():	
		dr, dw, de = select.select([sys.stdin], [], [], 0)
		return bool(dr)
	def read_key():
		fd = sys.stdin.fileno()
		old = termios.tcgetattr(fd)
		try:
			tty.setraw(fd)
			ch = sys.stdin.read(1)
		finally:
			termios.tcsetattr(fd, termios.TCSADRAIN, old)
		return ch

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
	color = {"success": Fore.GREEN, "warning": Fore.YELLOW, "info": Fore.CYAN}.get(effect_type, Fore.WHITE)
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

# --- Timed mini challenge ---
def timed_challenge(prompt, key, theme, stats, inventory, timeout=5, effects=None, reward_item=None):
	animated_text(prompt, color=theme["accent"])
	stop_event = threading.Event()
	style = random.choice(SPINNER_STYLES)
	color = random.choice(theme["spinner_colors"])
	t = threading.Thread(target=spinner, args=(stop_event, "React now! ", style, color))
	t.start()
	
	start_time = time.time()
	success = False
	while time.time() - start_time < timeout:
		if key_pressed():
			pressed = read_key()
			if pressed.lower() == key.lower():
				success = True
				break
	stop_event.set()
	t.join()
	
	if success:
		animated_effect("✅ Success! You completed the challenge!", "success")
		if effects and "success" in effects:
			for k, v in effects["success"].items():
				stats[k] = max(0, stats.get(k, 0) + v)
		if reward_item:
			inventory.append(reward_item)
			animated_effect(f"You found an item: {reward_item}", "info")
	else:
		animated_effect("❌ Failed! Time ran out.", "warning")
		if effects and "failure" in effects:
			for k, v in effects["failure"].items():
				stats[k] = max(0, stats.get(k, 0) + v)
	

# --- Display stats ---
def show_stats_inventory(stats, inventory, theme):
	stat_text = " | ".join([f"{k}: {v}" for k, v in stats.items()])
	inv_text = ", ".join(inventory) if inventory else "Empty"
	
	animated_text(f"Stats → {stat_text}", color=theme["text_color"])
	animated_text(f"Inventory → {inv_text}", color=theme["accent"])

# --- Combine items collected ---
def combine_items(inventory, theme):
	if len(inventory)<2:
		animated_effect("You need at least 2 items to combine.", "warning")
		return None
	animated_text("Choose two items to combine by name:", color=theme["prompt_color"])
	item1=spinner_input("First item: ", theme)
	item2=spinner_input("Second item: ", theme)
	if item1 in inventory and item2 in inventory:
		# Define some special combinations
		combinations={
			("healing herb","lucky coin"):"Elixir of Fortune",
			("boots","cloak"):"Stealth Gear"
		}
		key=(item1.lower(),item2.lower())
		key_rev=(item2.lower(), item1.lower())
		if key in combinations or key_rev in combinations:
			new_item=combinations.get(key, combinations.get(key_rev))
			inventory.remove(item1); inventory.remove(item2); inventory.append(new_item)
			animated_effect(f"Combined items to create {new_item}!", "info")
		else:
			animated_effect("❌ Nothing happened. Items cannot be combined.", "warning")
	else:
		animated_effect("❌ One or both items not in inventory.", "warning")
	
# --- Interactive theme selection ---
def select_theme():
	print("Choose a theme for your wizard:")
	for i, name in enumerate(THEMES.keys(), 1):
		print(f"  {i}. {name.title()}")
		
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
	animated_text(" Welcome to the RPG Wizard with Item Combinations! ", color=random.choice(theme["spinner_colors"]))
	time.sleep(0.5) 
	animated_text("Your stats will influence the adventure\n", color=theme["accent"])
	
# --- Animated outro ---
def animated_outro(theme):
	animated_text("\nEnding Adventure...", color=random.choice(theme["spinner_colors"]))
	time.sleep(0.5)
	animated_text("Thanks for playing!\n", color=theme["accent"])

# --- Main wizard loop ---
def run_wizard(theme):
	animated_intro(theme)
	stats = {"Health": 10, "Agility": 5, "Luck": 3}
	inventory = []
	
	while True:
		name = spinner_input(" Enter your character name? ", theme)
		if name == "exit": break
		
		choice = spinner_input(f"Hello {name}! Choose a path: [forest/city] ", theme)
		if choice == "forest":
			animated_effect("Entering a forest...", "info")
			timed_challenge(
			"A wild boar charges! Press 'd' to dodge!",
			"d", theme, stats, inventory,
			effects={"success":{"Agility":1}, "failure":{"Health":-3}},
			reward_item="Healing herb"
			)
		elif choice == "city":
			animated_effect("Entering the city...", "info")
			timed_challenge(
			"A thief attacks! Press 'p' to parry!",
			"p", theme, stats, inventory,
			effects={"success":{"Luck":1}, "failure":{"Health":-2}},
			reward_item="Lucky Coin"
			)
		else:
			animated_effect("⚠️ Invalid path.", "warning")
		
		show_stats_inventory(stats, inventory, theme)	
		
		combine=spinner_input("Do you want to try combining items [yes/no] ", theme)
		if combine=="yes":
			combine_items(inventory, theme)
		
		cont = spinner_input("Do you want another adventure? [yes/no] ", theme)
		if cont != "yes": break
		
	animated_outro(theme)

# --- Run program ---
if __name__ == "__main__":
	chosen_theme = select_theme()
	run_wizard(chosen_theme)
