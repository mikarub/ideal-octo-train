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

def skill_check(stats, skill_name, difficulty=5, critical_margin=3):
    """
    Performs a skill check based on player stats.

    Parameters
    ----------
    stats : dict
        Player stat dictionary, e.g. {"Strength": 4, "Agility": 6, ...}
    skill_name : str
        Name of the skill to test against.
    difficulty : int
        The target number to beat. Higher = harder.
    critical_margin : int
        How much above/below determines critical success/failure.

    Returns
    -------
    tuple (result, roll, total)
        result: "success", "failure", "critical_success", "critical_failure"
        roll: the raw d10 roll (1–10)
        total: roll + player skill value
    """

    # Retrieve skill level, default 0 if missing
    skill_value = stats.get(skill_name, 0)

    # Roll a d10
    roll = random.randint(1, 10)
    total = roll + skill_value

    # Narration
    animated_text(f"\n● Skill Check: {skill_name} (Difficulty {difficulty})")
    animated_text(f"  → Roll: {roll}   Skill: {skill_value}   Total: {total}")

    # Evaluate result
    target = difficulty

    if total >= target + critical_margin:
        animated_effect("Critical success!", "success")
        return "critical_success", roll, total

    if total >= target:
        animated_effect("Success.", "success")
        return "success", roll, total

    if total <= target - critical_margin:
        animated_effect("Critical failure!", "warning")
        return "critical_failure", roll, total

    animated_effect("Failure.", "warning")
    return "failure", roll, total
	
