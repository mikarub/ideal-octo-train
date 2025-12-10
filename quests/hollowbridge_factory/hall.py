from ui.animated_text import animated_text, animated_effect
from ui.spinner_input import spinner_input
from scenes.runner import register_scene, run_scene

@register_scene("factory_hall")
def hall_scene(stats, inventory, theme, save_state):
    animated_text("\nThe main hall is a cathedral of rust and belts.", color=theme["text_color"])
    animated_text("A network of walkways and stairs branch off in every direction.", color=theme["text_color"])

    visited = save_state.setdefault("visited", {})

    if not visited.get("factory_hall_first"):
        animated_effect("A faded signage points: WORKSHOP ←  STAIR →  CATWALK ↑  STORAGE ↓", "info")
        visited["factory_hall_first"] = True
        # small starter item possibility
        if "brass_gear" not in inventory and stats.get("Luck", 0) > 2:
            animated_effect("A loose Brass Gear glints by the wall — you pocket it.", "info")
            inventory.append("brass_gear")

    # present clear hub choices
    while True:
        choice = spinner_input("[workshop / stairs / storage / catwalk / engine / exit]: ", theme).strip().lower()
        if choice == "workshop":
            return run_scene("factory_workshop", stats, inventory, theme, save_state)
        elif choice == "stairs":
            return run_scene("factory_stairs", stats, inventory, theme, save_state)
        elif choice == "storage":
            return run_scene("factory_storage", stats, inventory, theme, save_state)
        elif choice == "catwalk":
            return run_scene("factory_catwalk", stats, inventory, theme, save_state)
        elif choice == "engine":
            # engine is deeper — approaching may require items/choices
            return run_scene("factory_engine_room", stats, inventory, theme, save_state)
        elif choice in ("exit", "leave"):
            animated_text("You slip back out into the night.", color=theme["text_color"])
            return
        else:
            animated_effect("You stand uncertain in the echoing hall.", "warning")
