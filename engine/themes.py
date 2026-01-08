# ================================
# utils/themes.py
# Stores color themes for the UI
# ===============================

from colorama import Fore, Style

# ------------------
# Theme definitions
# ----------------- 
THEMES = {
	"victorian": {
		"text_color": Fore.LIGHTWHITE_EX,
		"accent": Fore.CYAN,
		"prompt_color": Fore.CYAN,
		"warning": Fore.LIGHTYELLOW_EX,
		"danger": Fore.LIGHTRED_EX,
		"reset": Style.RESET_ALL
	}
}

def color_text(text, color):
	""" Simple wrapper that applies color and resets afterwards. """
	return f"{color}{text}{Style.RESET_ALL}"
