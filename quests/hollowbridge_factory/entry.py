from ui.animated_text import animated_text, animated_effect
from ui.spinner_input import spinner_input
from scenes.runner import register_scene, run_scene

@register_scene("enter_factory")
def enter_factory(stats, inventory, theme, save_state):
    animated_text("\nYou stand before the iron doors of the Hollowbridge Factory.", color=theme["text_color"])
    visited = save_state.setdefault("visited", {})

    if not visited.get("factory_arrival"):
        animated_effect("Smoke curls from the vents — the place has not fully slept.", "info")
        visited["factory_arrival"] = True
    else:
        animated_effect("The doors yawl open, familiar and terrible.", "info")

    # Entry always leads to the Hall (Hub)
    while True:
        choice = spinner_input("[enter hall / leave]: ", theme).strip().lower()
        if choice in ("enter", "hall", "enter hall"):
            return run_scene("factory_hall", stats, inventory, theme, save_state)
        elif choice == "leave":
            animated_text("You step back into the mist, for now.", color=theme["text_color"])
            return
        else:
            animated_effect("You hesitate — the doors are impatient.", "warning")
