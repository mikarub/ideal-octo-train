# quests/hollowbridge_factory/storage.py
from ui.animated_text import animated_text, animated_effect
from ui.spinner_input import spinner_input
from scenes.runner import register_scene, run_scene

@register_scene("factory_storage")
def storage_scene(stats, inventory, theme, save_state):
    visited = save_state.setdefault("visited", {})
    
    animated_text("Crates and barrels fill the storage room. Labels have long since faded.", color=theme["text_color"])

    if not visited.get("storage"):
        animated_effect("One crate lies broken open.", "info")
        visited["storage"] = True

    while True:
        choice = spinner_input("[inspect / take manual / take oil / hall / leave]: ", theme).strip().lower()
        
        # INSPECT
        if choice == "inspect":
            animated_effect("Among the debris is a pressure regulation manual.", "info")                
        
        # TAKE MANUAL
        elif choice == "take manual":
            if "pressure_manual" in inventory:
                animated_effect("You already have the manual.", "warning")
            else:
                animated_effect("You take the pressure manual. Some pages are still readable.", "info")
                inventory.append("pressure_manual")
                
        # TAKE OIL        
        elif choice == "take oil":
            if "oil_can" in inventory:
                animated_effect("The oil can is already in your pack.", "warning")
            else:
                animated_effect("You take a small can of machine oil.", "success")
                inventory.append("oil_can")
        
        # HALL    
        elif choice == "hall":
            animated_effect("You return to the main hall.", "info")
            return "factory_hall"
        
        # LEAVE
        elif choice == "leave":
            return "factory_hall"
        
        else:
            animated_effect("The air smells stale.", "warning")
