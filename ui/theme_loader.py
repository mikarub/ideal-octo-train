# ui/theme_loader.py
from colorama import Fore

THEMES = {
    "victorian": {
        "spinner_colors": [Fore.WHITE, Fore.LIGHTBLACK_EX],
        "prompt_color": Fore.LIGHTBLACK_EX,
        "text_color": Fore.WHITE,
        "accent": Fore.LIGHTRED_EX
    },
    "classic": {
        "spinner_colors": [Fore.WHITE],
        "prompt_color": Fore.WHITE,
        "text_color": Fore.WHITE,
        "accent": Fore.CYAN
    }
}

def get_theme(name="victorian"):
    return THEMES.get(name, THEMES["classic"])
