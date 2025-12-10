from engine.utils import skill_check
from ui.animated_text import animated_text, animated_effect
from scenes.runner import register_special_handler

def engine_repair_panel(stats, inventory, theme, save_state):
    """
    A lightweight placeholder repair handler until the full puzzle is implemented.
    Returns True if repair succeeds.
    """
    animated_text("\nYou open the cracked maintenance panel…", color=theme["text_color"])

    # Optional: use item requirements
    required_items = {"brass_gear", "oil_can"}

    if not required_items.issubset(set(inventory)):
        animated_effect(
            "You lack the proper parts. The panel refuses to respond.",
            "warning"
        )
        return False

    # Skill or random check
    success = skill_check(stats.get("Engineering", 1), difficulty=5)

    if success:
        animated_effect("⚙ You repair the panel! The engine stabilizes.", "success")
        save_state["engine_repaired"] = True
        return True
    else:
        animated_effect("⚠ Your repair fails. Sparks flash dangerously.", "warning")
        return False

# Register immediately when the module loads
register_special_handler("engine_repair_panel", engine_repair_panel)
