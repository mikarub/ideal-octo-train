from ui.spinner_input import spinner_input
from ui.animated_text import animated_text
from ui.animated_text import animated_effect
from scenes.runner import run_scene, register_scene

def enter_factory(stats, inventory, theme, save_state):
    animated_text("\nYou push open the metal doors...", color=theme["text_color"])

    while True:
        action = spinner_input(
            "[hall / stairs / workshop / storage / catwalk / engine / leave]: ", 
            theme
        ).strip().lower()

        if action == "hall":
            run_scene("factory_hall", stats, inventory, theme, save_state)
        elif action == "stairs":
            run_scene("factory_stairs", stats, inventory, theme, save_state)
        elif action == "workshop":
            run_scene("factory_workshop", stats, inventory, theme, save_state)
        elif action == "storage":
            run_scene("factory_storage", stats, inventory, theme, save_state)
        elif action == "catwalk":
            run_scene("factory_catwalk", stats, inventory, theme, save_state)
        elif action == "engine":
            run_scene("factory_engine_room", stats, inventory, theme, save_state)
        elif action == "leave":
            return
        else:
            animated_effect("You hesitate, uncertain.", "warning")

register_scene("factory_entry", enter_factory)
