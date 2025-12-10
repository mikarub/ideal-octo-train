# quests/hollowbridge_factory/storage.py
from ui.animated_text import animated_text, animated_effect
from ui.spinner_input import spinner_input
from scenes.runner import register_scene, run_scene

@register_scene("factory_storage")
def storage_scene(stats, inventory, theme, save_state):
    animated_text("\nThe storage room smells of oil and old cloth.", color=theme["text_color"])
    visited = save_state.setdefault("visited", {})

    if not visited.get("factory_storage"):
        animated_effect("Crates line the walls. One lid is ajar.", "info")
        visited["factory_storage"] = True

    while True:
        choice = spinner_input("[open crate / inspect crates / back]: ", theme).strip().lower()
        if choice == "open crate":
            if "oil_can" not in inventory:
                animated_effect("You open the crate and find an Oil Can—very handy.", "info")
                inventory.append("oil_can")
            else:
                animated_effect("The crate is empty now.", "info")
        elif choice == "inspect crates":
            animated_text("You notice a crate marked 'fragile - engineering parts'.", color=theme["text_color"])
            if "brass_gear" not in inventory and stats.get("Luck", 0) > 1:
                animated_effect("Tucked between packing straw: a spare brass gear.", "info")
                inventory.append("brass_gear")
        elif choice in ("back", "b"):
            return run_scene("factory_hall", stats, inventory, theme, save_state)
        else:
            animated_effect("Your hands search blindly through dust.", "warning")
