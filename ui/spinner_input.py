# ui/spinner_input.py
import threading
import itertools
import sys
import time
import random
from .animated_text import animated_text
from colorama import Fore, Style

SPINNER_STYLES = [
    ['|', '/', '-', '\\'],
    ['⠋','⠙','⠹','⠸','⠼','⠴','⠦','⠧','⠇','⠏'],
    ['◐','◓','◑','◒'],
    ['←','↖','↑','↗','→','↘','↓','↙'],
    ['▁','▃','▄','▅','▆','▇','▆','▅','▄','▃'],
    ['.  ', '.. ', '...', ' ..', '  .', '   ']
]

def spinner(stop_event, message, style, color):
    cycle = itertools.cycle(style)
    while not stop_event.is_set():
        sys.stdout.write('\r' + color + message + next(cycle) + Style.RESET_ALL)
        sys.stdout.flush()
        time.sleep(0.12)
    sys.stdout.write('\r' + ' ' * (len(message)+10) + '\r')

def spinner_input(prompt_text, theme):
    animated_text(prompt_text, color=theme.get("prompt_color"))
    stop_event = threading.Event()
    style = random.choice(SPINNER_STYLES)
    color = random.choice(theme.get("spinner_colors", [Fore.WHITE]))
    t = threading.Thread(target=spinner, args=(stop_event, "Waiting for input... ", style, color))
    t.daemon = True
    t.start()
    try:
        user_input = input()
    except KeyboardInterrupt:
        user_input = ""
    stop_event.set()
    t.join()
    return user_input.strip()
