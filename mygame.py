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
    "victorian": {
        "spinner_colors": [Fore.WHITE, Fore.LIGHTBLACK_EX],
        "prompt_color": Fore.LIGHTBLACK_EX,
        "text_color": Fore.WHITE,
        "accent": Fore.LIGHTRED_EX
    },
    # fallback themes if desired
    "classic": {
        "spinner_colors": [Fore.WHITE],
        "prompt_color": Fore.WHITE,
        "text_color": Fore.WHITE,
        "accent": Fore.CYAN
    }
}

# --- Spinner thread function ---
def spinner(stop_event,  message, style, color):
	cycle = itertools.cycle(style)
	while not stop_event.is_set():
		sys.stdout.write('\r' + color + message + next(cycle) + Style.RESET_ALL)
		sys.stdout.flush()
		time.sleep(0.12)
	sys.stdout.write('\r' + ' ' * (len(message)+10) + '\r') # clear line

# --- Animated text output ---
def animated_text(text, color=Fore.WHITE, speed=0.02, newline=True):
	for c in text:
		sys.stdout.write(color + c + Style.RESET_ALL)
		sys.stdout.flush()
		time.sleep(speed)
	if newline:
		print() # new line after text

# --- Animated sparkle effect for success/warning/info ---
def animated_effect(text, effect_type="success"):
	symbols = ["✦", "✧", "★", "☆", "✪", "✫"]
	color = {"success": Fore.GREEN, "warning": Fore.YELLOW, "info": Fore.CYAN}.get(effect_type, Fore.WHITE)
	for c in text:
		sys.stdout.write(color + c + Style.RESET_ALL)
		sys.stdout.flush()
		time.sleep(0.02)
		if random.random() < 0.08:
			sys.stdout.write(color + random.choice(symbols) + Style.RESET_ALL)
			sys.stdout.flush()
			time.sleep(0.01)
	print()
	
# ---------------------------- 
# Basic UI building blocks
# ----------------------------
def spinner_input(prompt_text, theme):	
	""" Show prompt (animated) and spinner until user types and presses Enter."""				
	animated_text(prompt_text, color=theme["prompt_color"])
	stop_event = threading.Event()
	style = random.choice(SPINNER_STYLES)
	color = random.choice(theme["spinner_colors"])
	t = threading.Thread(target=spinner, args=(stop_event, "Waiting for input...", style, color))
	t.start()
	try:
		user_input = input()
	except KeyboardInterrupt:
		user_input = ""
	stop_event.set()
	t.join()
	return user_input.strip()

# --- Display stats ---
def show_stats_inventory(stats, inventory, theme):
	stat_text = " | ".join([f"{k}: {v}" for k, v in stats.items()])
	inv_text = ", ".join(inventory) if inventory else "Empty"
	
	animated_text(f"Stats → {stat_text}", color=theme["text_color"])
	animated_text(f"Inventory → {inv_text}", color=theme["accent"])

# --------------------------
# Timed challenge primitive
# --------------------------
def timed_challenge(prompt, required_key, theme, stats, inventory, timeout=5, effects=None, reward_item=None, allow_skip=False):
	"""
	Shows prompt, runs a spinner while waiting for a specific key press within timeout.
	effects: dict like {"success": {"Agility":10, "failure": {"Health":-2}}
	reward_item: item name to append on success
	Returns True if succeeded, False if failed or timed out.
	"""
	animated_text(prompt, color=theme["accent"])
	stop_event = threading.Event()
	style = random.choice(SPINNER_STYLES)
	color = random.choice(theme["spinner_colors"])
	t = threading.Thread(target=spinner, args=(stop_event, "React now! ", style, color))
	t.start()
	
	start_time = time.time()
	success = False
	try:
		while time.time() - start_time < timeout:
			if key_pressed():
				ch = read_key()
				# normalise Windows return of \r or so; consider both lower/upper
				if isinstance(ch, str) and ch:
					if ch.lower() == required_key.lower():
						success = True
						break
				if allow_skip and ch in ("\r", "\n"):
					break
			time.sleep(0.01)
	finally:
		stop_event.set()
		t.join()

	if success:
		animated_effect("✅ Success! You completed the challenge!", "success")
		if effects and "success" in effects:
			for k, v in effects["success"].items():
				stats[k] = max(0, stats.get(k, 0) + v)
		if reward_item:
			inventory.append(reward_item)
			animated_effect(f"You obtained: {reward_item}", "info")
	else:
		animated_effect("❌ Challenge failed (time ran out or wrong key).", "warning")
		if effects and "failure" in effects:
			for k, v in effects["failure"].items():
				stats[k] = max(0, stats.get(k, 0) + v)
	return success		

# ------------------------------
# Item combining (small helper)
# ------------------------------
def combine_items(inventory, theme):
	if len(inventory)<2:
		animated_effect("You need at least 2 items to combine.", "warning")
		return None
	animated_text("Choose two items to combine by name:", color=theme["prompt_color"])
	animated_text(f"Inventory: {', '.join(inventory)}", color=theme["accent"])
	i1=spinner_input("First item: ", theme).strip()
	i2=spinner_input("Second item: ", theme).strip()
	if i1 not in inventory or i2 not in inventory:
		animated_effect("One or both items not found in inventory.", "warning")
		return None
	# simple combination map (extend as needed)
	combos = {
		("Healing Herb","Lucky Coin"): "Elixir of Fortune",
		("Boots","Cloak"): "Stealth Gear",
		("Mystic Key", "Chest of Wonders"): "Celestial Relic"
	}
	key=(i1,i2)
	key_rev=(i2, i1)
	if key in combos or key_rev in combos:
		new = combos.get(key) or combos.get(key_rev)
		inventory.remove(i1)
		inventory.remove(i2)
		inventory.append(new)
		animated_effect(f"Combined items to create {new_item}!", "info")
		# trigger hidden evens if any (modular)
		trigger_item_combination_event(new, inventory, theme)
		return new
	else:
		animated_effect("The items do not combine into anything useful.", "warning")
		return None
# -----------------------------------	
# Hook for item-combination events (modular)
# -----------------------------------
def trigger_item_combination_event(new_item, inventory, theme):
	"""
	I certain special items are created, trigger secret events.
	Keep this modular - add cases as needed.
	"""
	if new_item == "Elixir of Fortune":
		animated_effect("A whispered fortune follows...you feel luckier.", "success")
		inventory.append("Golden Amulet")
	if new_item == "Stealth Gear":
		animated_effect("Shadows cling to you. A token slips into your pocket.", "info")
		inventory_append("Shadow Token")
	if new_item == "Celestial Relic":
		animated_effect("A distant hum answers the relic...the world shifts slightly.", "success")
		inventory_append("Phantom Amulet")

# -------------------------
# Random atmospheric scare
# -------------------------

def random_scatter_scary_lines(theme):
	# Occassionally called to drop atmospheric one-liners
	lines = [
		"A distant toot of a gear sighs-like a forgotten throat clearing.",
		"The steam seems to sigh with words you almost understand.",
		"A child's lullaby ghosts through the vents-a music box long dead.",
		"Something brushed past you, soft as moth-wings and colder than air."
	]
	animated_text(random.choice(lines), color=theme["text_color"])
	
# --------------------------------
# The Lament Quest Implementation
# --------------------------------
def lament_of_hollowbridge_factory(stats, inventory, theme):
	"""
	Multi-stage Victorian-horror quest:
	- Assembly Hall (conveyor activates)
	- Mannequin Storage (mannequins shift when unseen)
	- Heart Engine (final chamber): destroy the engine, freeing consciousness fragments
	"""
	animated_effect("You arrive at Hollowbridge Factory - night and smoke cling to the brickwork.", "info")
	time.sleep(0.4)
	animated_text("Rumours say the place breathes. The gata is ajar.", color=theme["prompt_color"])
	time.sleep(0.3)
	
	# Stage: Assembly Hall
	animated_text("\n→ Assembly Hall", color=theme["accent"])
	animated_text("You step into the hall. Conveyor belts creak even though no hands feed them.", color=theme["text_color"])
	# time dodge or step aside: press 's' to step aside quickly
	dodge_ok = timed_challenge("Step aside! Press 's' to leap away.", "s", theme, stats, inventory,
								timeout=4,
								effects={"success": {"Agility": 1}, "failure": {"Health": -1}},
								reward_item=None)
	if not dodge_ok:
		animated_text("You stumble back, scraped by a rusted bracket. Your coat is torn.", color=theme["text_color"])
	random_scatter_scary_lines(theme)
	show_stats_inventory(stats, inventory, theme)
	time.sleep(0.5)
	
	# Stage: Clockwork Mannequin Storage
	animated_text("\n→ Clockwork Mannequin Storage", color=theme["accent"])
	animated_text("Rows upon rows of mannequins stand like sermon pews. Their glass eyes await.", color=theme["text_color"])
	time.sleep(0.4)
	animated_text("Each time you glance away, you sense a subtle shift in posture.", color=theme["text_color"])
	# investigation: the player can 'inspect' or 'listen'
	inspect_choice = spinner_input("Do you inspect a mannequin closely or move on? [inspect/move] ", theme).strip().lower()
	if inspect_choice == "inspect":
		animated_text("Leaning in, the mannequin's hand is warm - impossibly warm.", color=theme["text_color"])
		# small reveal item: hair ribbon, scrap of paper with a digit
		animated_effect("You find a scrap of paper tucked in its sleeve: '3' scribbled in hurried ink.", "info")
		inventory.append("Scrap: '3'")
	else:
		animated_text("You force your gaze forward; your eyes sting as if from long-held fear.", color=theme["text_color"])
	# mannequin movement scare: if player looks away repeatedly, we simulate by random chance
	if random.random() < 0.6:
		animated_text("When you turn back, a mannequin on the far row is now nearer than before.", color=theme["text_color"])
		# small timed encounter: press 't' to touch the mannequin (brave) - reveals clue
		brave = timed_challenge("Touch the mannequin? Press 't' to reach out.", "t", theme, stats, inventory,
								timeout=5,
								effects={"success": {"Luck": 1}, "failure": {"Health": -1}},
								reward_item=None)
		if brave:
			animated_effect("You feel a pulse - not of blood, but of memory. Words: 'Return to the Heart...'", "info")
			inventory.append("Whisper: 'Return to the Heart'")
	show_stats_inventory(stats, inventory, theme)
	time.sleep(0.5)
	
	# Encourage combinations / puzzle solving before entering final chamber
	animated_text("\nA groan echoes from deeper within - the Heart Engine stirs.", color=theme["text_color"])
	if "Mystic Key" in inventory and "Chest of Wonders" not in inventory:
		animated_effect("Your Mystic Key hums faintly; perhaps a chest lies ahead.", "info")
	
	# Allow player to try combining items before final showdown
	want_combine = spinner_input("Do you want to attempt any item combinations before proceeding? [yes/no] ", theme).strip().lower()
	if want_combine == "yes":
		combine_items(inventory, theme)
		show_stats_inventory(stats, inventory, theme)
		
	# Stage: The Heart Engine (Final Chamber)
	animated_text("\n→ The Heart Engine", color=theme["accent"])
	animated_text("You pass beneath a ring of gears. The air thickens; your breath tastes metallic.", color=theme["text_color"])
	time.sleep(0.5)
	animated_text("At the chamber's center a suspended sphere of interlocking brass gears: fragments cry out in half-remembered names.", color=theme["text_color"])
	time.sleep(0.6)
	
	# Reveal the truth: mannequins contain fragments; engine feeds on fear.
	animated_effect("As you step closer, a chorus of half-voices threads through the gears: fragments cry out in half-remembered names.", "info")
	animated_text("You realise with a sickening clarity: the mannequins hold stolen consciousness-this engine devours fear to keep them alive.", color=theme["text_color"])
	
	# Option: attempt to 'calm' the engine (riddle/puzzle) OR destroy it directly
	choice_final = spinner_input("Do you attempt to quiet the engine (clever puzzle) or destroy it outright (force)? [quiet/destroy] ", theme).strip().lower()
	
	if choice_final == "quiet":
		# A puzzle-based approach: use clues(e.g. Scrap: '3' and Whisper) to solve a riddle
		animated_text("You attempt to align the gears to a pattern that soothes the stolen echoes.", color=theme["text_color"])
		# Simple puzzle: player must type a word that includes 'heart' or 'calm' or use scrap
		puzzle_answer = spinner_input("Enter the calming phrase (hint: something of solace) or type 'fail' to abort: ", theme).strip().lower()
		if "calm" in puzzle_answer or "heart" in puzzle_answer or "solace" in puzzle_answer:
			animated_effect("The gears hesitate. For a breath, the world holds its breath. The engine falters.", "success")
			# if player successfully soothes, they can try to extract the core safely
			safe_extract = timed_challenge("Now quickly - press 'e' to extract the core while it slumbers!", "e", theme, stats, inventory,
											timeout=6,
											effects={"success": {"Luck": 2}, "failure": {"Health": -3}},
											reward_item="Silenced Core Fragment")
			if safe_extract:
				animated_effect("You wrench a humming piece from the engine. Its sound is a child's lullaby.", "info")
				inventory.append("Silenced Core Fragment")
				# consequence: engine weakened, mannequins slump but consciousness fragments remain bound
				animated_effect("The mannequins slump; the fragments still whisper, but their cries are muffled.", "info")
				show_stats_inventory(stats, inventory, theme)
			else:
				animated_effect("Extraction failed - the engine sluices fear outward in a violent burst.", "warning")
				# escalate to forced destroy path
				choice_final = "destroy"
		else:
			animated_effect("Your words tumble meaningless against the brass. The machine laughs - a grinding rasp.", "warning")
			# player loses a bit of Health
			stats["Health"] = max(0, stats.get("Health", 0) - 1)
			choice_final = "destroy"
				
	if choice_final == "destroy":
		# Final violent confrontation: timed sequence + possible inventory modifiers
		animated_text("You decide: the horror must end. Destroy the Hearth Engine.", color=theme["text_color"])
		# if player has special items, they may alter the outcome
		bonus = 0
		if "Shadow Token" in inventory or "Stealth Gear" in inventory:
			animated_effect("Your acquired items make the approach surer: you move like a ghost.", "info")
			bonus += 1
		if "Golden Amulet" in inventory or "Phantom Amulet" in inventory:
			animated_effect("A relic hums, lending you courage.", "info")
			bonus += 1
			
		# Multi-step attack: three rapid required key presses (simulate escalating difficulty)
		animated_text("You will need to perform three synchronised actions to rupture the core.", color=theme["text_color"])
		successes = 0
		# Step 1: sever a supporting gear (press 'r')
		if timed_challenge("Sever the outer gears! Press 'r' now!", "r", theme, stats, inventory, timeout=4 - min(2, bonus),
							effects={"success": {}, "failure": {"Health": -2}}):
			successes += 1
		# Step 2: smash the conduit (press 'h')
		if timed_challenge("Smash the conduit feeding the heart! Press 'h' now!", "h", theme, stats, inventory, timeout=4 - min(2, bonus),
							effects={"success": {}, "failure": {"Health": -2}}):
			successes += 1
		# Step 3: deliver the final blow (press 'k')
		if timed_challenge("Deliver the final blow to the core! Press 'k' now!", "k", theme, stats, inventory, timeout=3 - min(1, bonus),
							effects={"success": {}, "failure": {"Health": -4}}):
			successes += 1

		# Evaluate outcome
		if successes >= 2:
			# Player succeeds in destroying the engine
			animated_effect("\nThe gear-sphere cracks. A keening noise fills the chamber as ribbons of light and steam pour forth.", "success")
			# Freed consciousness fragments - add "Released Echoes" for narrative consequences
			inventory.append("Released Echoes")
			# reward: major stat change (also a narrative burden)
			stats["Luck"] = max(0, stats.get("Luck", 0) + 2)
			stats["Agility"] = max(0, stats.get("Agility", 0) + 1)
			animated_effect("You have destroyed the Heart Engine. The mannequins collapse, their bindings freed.", "info")
			animated_text("But in the rising steam, you feel the release of many voices-what you have set loose is unknown.", color=theme["text_color"])
			# Perhaps future quests are affected by Released Echoes (modular hook)
		else:
			animated_effect("\nThe engine resists. Your blows ring hollow and you are thrown back by a pulse of dread.", "warning")
			stats["Health"] = max(0, stats.get("Health", 0) - 5)
			animated_text("You barely escape the chamber as machinery smashes and the factory convulses.", color=theme["text_color"])
			# If player failed, possibly they flee with partial knowledge/item
			if random.random() < 0.5:
				animated_effect("You snatch a fragment as  you flee - it hums with trapped memory.", "info")
				inventory.append("Hollow Fragment")
	# Final aftermath
	time.sleep(0.6)
	animated_text("\nYou stumble out into the cold night. The factory behind you groans and then falls silent.", color=theme["text_color"])
	animated_text("In the hush that follows, the city seems unchanged - but something in the fog feels different.", color=theme["text_color"])
	show_stats_inventory(stats, inventory, theme)
	
	# Post-quest consequence hook (modular)
	if "Released Echoes" in inventory:
		animated_effect("News of strange dreams begins to ripple through the city. You have altered fate.", "info")
		
	animated_effect("Quest Complete: The Lament of Hollowbridge Factory", "success")

# ------------------------------------
# Main loop example to run this quest
# ------------------------------------
def main():
	theme = THEMES["victorian"]
	
	# Starting the player state
	stats = {"Health": 10, "Agility": 5, "Luck": 3}
	inventory = []
	
	animated_text("=== RPG: Hollowbridge Prologue ===\n", color=theme["accent"])
	animated_text("Type 'exit' at any prompt to quit the demo.\n", color=theme["text_color"])
	
	# Simple loop: allow player to run the quest, inspect inventory or quit
	while True:
		choice = spinner_input("\nChoose: [enter quest / inventory / exit] ", theme).strip().lower()
		if choice == "exit":
			animated_text("Farewell, wanderer.", color=theme["text_color"])
			break
		elif choice in ("inventory", "inv"):
			show_stats_inventory(stats, inventory, theme)
			continue
		elif choice in ("enter quest", "quest", "enter"):
			lament_of_hollowbridge_factory(stats, inventory, theme)
		else:
			animated_text("Command not recognised.", color=theme["text_color"])

# Run when executed
if __name__ == "__main__":
	main()
