# ui/animated_text.py
# Provides animated_text and animated_effect used across the project.

import sys
import time
import random
from colorama import init, Fore, Style

init(autoreset=True)

# Simple color map (falls back to white)
COLOR_MAP = {
    "white": Fore.WHITE,
    "red": Fore.RED,
    "green": Fore.GREEN,
    "yellow": Fore.YELLOW,
    "cyan": Fore.CYAN,
    "magenta": Fore.MAGENTA,
    "blue": Fore.BLUE,
    None: Fore.WHITE
}

def animated_text(text, delay=0.00, speed=None, color=None, newline=True):
    """
    Print text optionally character-by-character.
    - text: string to print
    - delay: seconds between characters (0 for instant)
    - color: color name or Colorama code (optional)
    - newline: whether to append newline at end
    """
    assert isinstance(color, (str, type(None))), f"animated_text color broken: {color}"
    if speed is not None:
        delay = speed
    col = COLOR_MAP.get(color, color)  # allow passing a Colorama code or name
    if delay and delay > 0:
        for ch in text:
            sys.stdout.write(col + ch + Style.RESET_ALL)
            sys.stdout.flush()
            time.sleep(delay)
        if newline:
            print()
    else:
        # fast path
        sys.stdout.write(col + text + Style.RESET_ALL)
        if newline:
            sys.stdout.write("\n")
        sys.stdout.flush()

def animated_effect(text, effect_type="info", delay=0.02):
    """
    Display the text intact but animate small prefix/suffix symbols.
    Keeps the text body untouched (no symbols inserted inside words).
    - effect_type: "success", "warning", "info", or other
    - delay: timing for the small animation frames
    """
    # symbol pools and color selection
    SYMBOLS = {
        "success": ["✦", "✧", "★", "✪"],
        "warning": ["✖", "⚠", "◆", "✚"],
        "info": ["♦", "◈", "◍", "●"],
        "default": ["•", "*", "·", "#"]
    }
    COLOR = {
        "success": Fore.GREEN,
        "warning": Fore.YELLOW,
        "info": Fore.CYAN
    }.get(effect_type, Fore.WHITE)

    symbols = SYMBOLS.get(effect_type, SYMBOLS["default"])
    prefix = random.choice(symbols)
    suffix = random.choice(symbols)

    base = f"{prefix} {text} {suffix}"
    max_len = len(base)

    # small prefix pulse
    for _ in range(2):
        p = random.choice(symbols)
        display = f"{p} {text}"
        sys.stdout.write("\r" + COLOR + display + " " * (max_len - len(display)) + Style.RESET_ALL)
        sys.stdout.flush()
        time.sleep(delay)

    # stable prefix
    display = f"{prefix} {text}"
    sys.stdout.write("\r" + COLOR + display + " " * (max_len - len(display)) + Style.RESET_ALL)
    sys.stdout.flush()
    time.sleep(delay * 1.0)

    # suffix pulse
    for _ in range(2):
        s = random.choice(symbols)
        display = f"{prefix} {text} {s}"
        sys.stdout.write("\r" + COLOR + display + " " * (max_len - len(display)) + Style.RESET_ALL)
        sys.stdout.flush()
        time.sleep(delay * 1.0)

    # final stable line and newline
    display = f"{prefix} {text} {suffix}"
    sys.stdout.write("\r" + COLOR + display + " " * (max_len - len(display)) + Style.RESET_ALL + "\n")
    sys.stdout.flush()
