# engine/engine_core.py
import time
import threading
import random

# Attempt to re-use an existing timed_challenge if present in your codebase
try:
    # if you already have a timed_challenge in some module, adapt the import target as needed
    from engine.combine import timed_challenge as _external_timed_challenge  # optional existing
except Exception:
    _external_timed_challenge = None

# fallback spinner & key detection
try:
    import msvcrt
    def key_pressed():
        return msvcrt.kbhit()
    def read_key():
        return msvcrt.getwch()
except Exception:
    import sys, select, tty, termios
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

def timed_challenge(prompt, required_key, timeout=5, allow_skip=False, poll_delay=0.01):
    """
    A small portable timed_challenge fallback used by handlers.
    Returns True on success (correct key pressed within timeout), False otherwise.
    If an external timed_challenge exists, it will be used.
    """
    if _external_timed_challenge:
        # Attempt to call external signature; adapt if necessary.
        try:
            return _external_timed_challenge(prompt, required_key, timeout=timeout)
        except Exception:
            # if signature doesn't match, fall back
            pass

    # Fallback UI (very minimal) - prints prompt and listens for key.
    print(prompt)
    start = time.time()
    while time.time() - start < timeout:
        if key_pressed():
            ch = read_key()
            if isinstance(ch, str) and ch.lower() == required_key.lower():
                return True
            if allow_skip and ch in ("\r", "\n"):
                return False
        time.sleep(poll_delay)
    return False
