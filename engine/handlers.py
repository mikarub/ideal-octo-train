# engine/handlers.py
from scenes.runner import register_special_handler
from engine.engine_core import timed_challenge
from ui.animated_text import animated_text, animated_effect

def engine_repair_panel(stats, inventory, theme, save_state):
    """
    A multi-step mini-game to repair the engine panel.
    Requirements: presence of 'insulated_wire' and 'precision_screwdriver' gives bonus.
    Rewards: 'repaired_panel' and possibly 'Silenced Core Fragment'.
    """
    animated_text("\nYou kneel before the engine's service panel.", color=theme["text_color"])

    # Check components
    has_wire = "insulated_wire" in inventory
    has_screw = "precision_screwdriver" in inventory

    if not (has_wire and has_screw):
        animated_effect("You are missing some components to attempt a proper repair.", "warning")
        # small chance to attempt amateur fix anyway
        choice = input("Attempt a makeshift repair? (y/n): ").strip().lower()
        if choice != "y":
            return False

    # Step sequence (3 quick key presses). The player must press the printed key within a short timeout.
    seq = []
    for _ in range(3):
        seq.append(random.choice(list("rhteuk")))

    # display sequence as hints one by one; require correct presses
    successes = 0
    timeout_base = 4
    if has_wire and has_screw:
        timeout_base += 1  # small bonus for having the right tools

    for idx, key in enumerate(seq, start=1):
        prompt = f"Action {idx}: press '{key}' now!"
        ok = timed_challenge(prompt, key, timeout=timeout_base - min(2, idx))
        if ok:
            animated_effect(f"Action {idx} successful.", "success")
            successes += 1
        else:
            animated_effect(f"Action {idx} failed.", "warning")

    if successes >= 2:
        animated_effect("The panel locks into place with a soft click. Repair successful.", "success")
        if "repaired_panel" not in inventory:
            inventory.append("repaired_panel")
        # reward possibility
        if random.random() < 0.6:
            inventory.append("Silenced Core Fragment")
            animated_effect("You pry a humming fragment loose and slip it into your pack.", "info")
        # record visited state
        save_state["visited"]["engine_panel_repaired"] = True
        return True
    else:
        animated_effect("The makeshift repair fails; sparks singe your gloves.", "warning")
        stats["Health"] = max(0, stats.get("Health", 0) - 2)
        return False

# register handler under a friendly name
register_special_handler("engine_repair_panel", engine_repair_panel)
