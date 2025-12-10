# quests/hollowbridge_factory/catwalk.py
from ui.animated_text import animated_text, animated_effect
from ui.spinner_input import spinner_input
from scenes.runner import register_scene, run_scene

@register_scene("factory_catwalk")
def catwalk_scene(stats, inventory, theme, save_state):
    animated_text("\nYou cross a rickety catwalk high above the factory floor.", color=theme["text_color"])
    visited = save_state.setdefault("visited", {})

    if not visited.get("factory_catwalk_first"):
        animated_effect("Below, cogs turn like sleeping teeth. A faint hum drifts from the engine room.", "info")
        visited["factory_catwalk_first"] = True

    # Offer inspect, jump, or approach engine choices
    while True:
        choice = spinner_input("[inspect / approach engine / jump down / back]: ", theme).strip().lower()
        if choice == "inspect":
            if "oil_can" in inventory:
                animated_effect("You oil a squeaky joint and notice a hidden panel with wiring diagrams.", "info")
                # give hint in notes
                save_state.setdefault("notes", "")
                save_state["notes"] += "Found wiring hint on catwalk.\n"
            else:
                animated_effect("You peer over the edge but the hum feels distant. Maybe some oil would steady your gaze.", "info")
        elif choice == "approach engine":
            return run_scene("factory_engine_room", stats, inventory, theme, save_state)
        elif choice == "jump down":
            animated_effect("You leap — it's a long drop. You survive but are shaken (-2 Health).", "warning")
            stats["Health"] = max(0, stats.get("Health", 0) - 2)
            return run_scene("factory_hall", stats, inventory, theme, save_state)
        elif choice in ("back", "b"):
            return run_scene("factory_hall", stats, inventory, theme, save_state)
        else:
            animated_effect("The catwalk creaks; choose carefully.", "warning")
