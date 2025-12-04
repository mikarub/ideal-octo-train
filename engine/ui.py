# ============================================
# utils/animation.py
# Handles animated text, spinner prompts etc.
# ============================================

import time
import itertools
import threading
import sys
from colorama import Fore, Style

# -------------------------------------------
# Animated printing (per-character printing)
# -------------------------------------------
def animated_text(text, delay=0.015, color=Fore.WHITE):
	"""
	Smooth, readable animated printing.
	Does NOT scramble text.
	"""
	sys.stdout.write(color)
	for char in text:
		sys.stdout.write(char)
		sys.stdout.flush()
		time.sleep(delay)
	sys.stdout.write(Style.RESET_ALL)
	
# -----------------------------------------------------
# Clean animated effect with open/close symbol "burst"
# -----------------------------------------------------
def animated_effect(message, effect_type="info", delay=0.01):
	"""
	Animated message with a decorative prefix/suffix burst.
	Keeps the message itself clean.
	No scrambled words.
	"""
	burst = {
		"info":  ("≼≼≼ ", " ≽≽≽"),
        "warning": ("✦✦✦ ", " ✦✦✦"),
        "danger": ("✖✖✖ ", " ✖✖✖"),
        "success": ("➤➤➤ ", " ➤➤➤"),
        "magic": ("⌬⌬⌬ ", " ⌬⌬⌬"),
    }
    prefix, suffix = bursts.get(effect_type, ("≼ ", " ≽"))
    
    full_msg = f"{prefix}{message}{suffix}"
    
    for char in full_msg:
		sys.stdout.write(char)
		sys.stdout.flush()
		time.sleep(delay)
	print() # newline
	
# --------------------------------------------
# Spinner input for atmospheric input prompts
# --------------------------------------------
def spinner_input(prompt, theme):
	"""
	Displays a spinner while waiting for user input.
	"""
	spinner_chars = itertools.cycle(["-", "\\", "|", "/"])
	stop_flag = False
	user_input = ""
	
	def spinner():
		while not stop_flag:
			sys.stdout.write(f"\r{prompt}{next(spinner_chars)} ")
			sys.stdout.flush()
			time.sleep(0.07)
			
	thread = threading.Thread(target=spinner)
	thread.start()
	
	try:
		user_input = input(f"\r{prompt}")
	finally:
		stop_flag = True
		thread.join()
		print("\r" + " " * (len(prompt) + 4) + "\r", end="")
		
	return user_input
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
			
			
			
			
			
			
			
			








    
    
    
    
