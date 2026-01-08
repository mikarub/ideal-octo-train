# ui/spinner_input.py
import threading
import itertools
import sys
import time
import random
from ui.animated_text import animated_text
from colorama import Fore, Style

SPINNER_STYLES = [
    ['|', '/', '-', '\\'],
    ['⠋','⠙','⠹','⠸','⠼','⠴','⠦','⠧','⠇','⠏'],
    ['◐','◓','◑','◒'],
    ['←','↖','↑','↗','→','↘','↓','↙'],
    ['▁','▃','▄','▅','▆','▇','▆','▅','▄','▃'],
    ['.  ', '.. ', '...', ' ..', '  .', '   ']
]

def spinner(stop_event, theme):
    frames = ['⠋','⠙','⠹','⠸','⠼','⠴','⠦','⠧','⠇','⠏']
    accent = theme.get("accent", "")
    
    i = 0
    
    while not stop_event.is_set():
        sys.stdout.write("\r" + accent + frames[i % len(frames)] + " ")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
        
    # Clear spinner line on stop
    sys.stdout.write("\r    \r")
    sys.stdout.flush()

def spinner_input(prompt_text, theme):
    # 1) Print prompt normally
    animated_text(prompt_text, color=theme["prompt_color"]) # this works: theme["text_color"]
    
    # 2) Show spinner briefly
    stop_event = threading.Event()
    style = random.choice(SPINNER_STYLES)
    color = random.choice(theme.get("spinner_colors",[Fore.WHITE]))
    
    t = threading.Thread(
        target=spinner, 
        args=(stop_event, theme), 
        daemon=True)
    t.start()
    time.sleep(0.4)
    stop_event.set()
    t.join
    
    return input("> ").strip()
