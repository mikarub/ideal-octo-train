# quests/hollowbridge_factory/workshop.py
from ui.animated_text import animated_text, animated_effect
from ui.spinner_input import spinner_input
from scenes.runner import register_scene, run_scene

@register_scene("factory_workshop")
def workshop_scene(stats, inventory, theme, save_state):
    animated_text("\nYou step into the workshop. Benches sag under broken instruments.", color=theme["text_color"])
    visited = save_state.setdefault("visited", {})

    if not visited.get("factory_workshop"):
        animated_effect("A broken toolbox rests in the corner.", "info")
        visited["factory_workshop"] = True

    while True:
        choice = spinner_input("[search toolbox / repair bench / back]: ", theme).strip().lower()
        if choice == "search toolbox":
            if "precision_screwdriver" not in inventory:
                animated_effect("You pries open a rusted case and find a precision screwdriver.", "info")
                inventory.append("precision_screwdriver")
            else:
                animated_effect("Nothing else of use remains in the box.", "info")
        elif choice == "repair bench":
            # small puzzle: need precision_screwdriver to fix gadget
            if "precision_screwdriver" in inventory:
                animated_effect("Using the screwdriver you repair an odd contraption that reveals a small key.", "success")
                if "small_key" not in inventory:
                    inventory.append("small_key")
            else:
                animated_effect("Your hands work, but without a fine tool you can only make noise.", "warning")
        elif choice in ("back", "b"):
            return run_scene("factory_hall", stats, inventory, theme, save_state)
        else:
            animated_effect("You fumble; nothing happens.", "warning")
