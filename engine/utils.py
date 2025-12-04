# engine/utils.py
import threading
import random
import time
from ui.animated_text import animated_text, animated_effect
from ui.spinner_input import spinner_input, spinner

# --------------------------
# Timed Challenge Primitive
# --------------------------
def timed_challenge(prompt, required_key, theme, stats, inventory, timeout=5, effects=None, reward_item=None, allow_skip=False):
    """
    Shows prompt, runs a spinner while waiting for a specific key press within timeout.
    effects: dict like {"success": {"Agility":10}, "failure": {"Health":-2}}
    reward_item: item name to append on success
    Returns True if succeeded, False if failed or timed out.
    """
    animated_text(prompt, color=theme["accent"])
    stop_event = threading.Event()
    style = random.choice(["dots", "line", "bounce"])  # example spinner styles
    color = random.choice(theme["spinner_colors"])
    t = threading.Thread(target=spinner, args=(stop_event, "React now! ", style, color))
    t.start()

    start_time = time.time()
    success = False
    try:
        while time.time() - start_time < timeout:
            ch = spinner_input("Press key: ", theme)
            if ch:
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
