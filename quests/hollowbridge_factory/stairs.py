# quests/hollowbridge_factory/stairs.py
from ui.animated_text import animated_text, animated_effect
from ui.spinner_input import spinner_input
from scenes.runner import register_scene, run_scene

@register_scene("factory_stairs")
def stairs_scene(stats, inventory, theme, save_state):
    animated_text("\nYou ascend a flight of iron stairs. The air smells of oil and memory.", color=theme["text_color"])
    visited = save_state.setdefault("visited", {})

    # immediate hazard choice
    animated_text("A rung looks loose. You could try to hop it or test it.", color=theme["text_color"])
    while True:
        choice = spinner_input("[test / hop / back]: ", theme).strip().lower()
        if choice == "test":
            # simple Agility check
            agi = stats.get("Agility", 0)
            if agi >= 5:
                animated_effect("You test the rung — it's stable. You proceed carefully and gain confidence.", "info")
                stats["Agility"] = agi + 0  # no change, but narrative
            else:
                animated_effect("The rung cracks; you twist and shrug it off (-1 Health).", "warning")
                stats["Health"] = max(0, stats.get("Health", 0) - 1)
            # go to catwalk from here
            return run_scene("factory_catwalk", stats, inventory, theme, save_state)
        elif choice == "hop":
            if stats.get("Agility", 0) >= 6:
                animated_effect("You bound up the stairs with a flourish.", "success")
                return run_scene("factory_catwalk", stats, inventory, theme, save_state)
            else:
                animated_effect("You miss your footing and tumble — bruise (-1 Health).", "warning")
                stats["Health"] = max(0, stats.get("Health", 0) - 1)
                return run_scene("factory_hall", stats, inventory, theme, save_state)
        elif choice in ("back", "b"):
            return run_scene("factory_hall", stats, inventory, theme, save_state)
        else:
            animated_effect("Your movement stalls — choose an action.", "warning")
