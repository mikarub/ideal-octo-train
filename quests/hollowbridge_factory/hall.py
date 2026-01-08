# quests/hollowbridge_factory/hall.py
from ui.animated_text import animated_text, animated_effect
from ui.spinner_input import spinner_input
from scenes.runner import register_scene, run_scene

@register_scene("factory_hall")
def hall_scene(stats, inventory, theme, save_state):
    visited = save_state.setdefault("visited", {})
    flags = save_state.setdefault("flags", {})
    
    animated_text("You stand in the factory's main hall. Rusted walkways stretch above you.", color=theme["text_color"])
        
    if not visited.get("hall"):
        animated_effect("Doorways lead to several sections of the factory.", "info")
        visited["hall"] = True
    
    while True:
        choice = spinner_input("[inspect hall / workshop / storage / stairs / leave]: ", theme).strip().lower()
        
        # INSPECT
        if choice == "inspect hall":
             animated_effect("You spot a stairwell leading up, but part of it has collapsed.", "info")
             animated_effect("A narrow catwalk is visible above - accessible from the stairs.", "info")
             animated_effect("A side door leads to a storage room.", "info")
             flags["hall_inspected"] = True
             flags["stairs_unlocked"] = True
        
        # WORKSHOP             
        elif choice == "workshop":
            animated_effect("You head into the workshop.", "info")
            return "factory_workshop"
        
        # STORAGE    
        elif choice == "storage":
            animated_effect("You move towards the storage room.", "info")
            return "factory_storage"
        
        # STAIRS (GATED)
        elif choice == "stairs":
            if not flags.get("stairs_unlocked"):
                animated_effect("You're not sure where the stairs lead. Better inspect the hall.", "warning")
            else:
                animated_effect("You climb the damaged stairs cautiously.", "info")
                return "factory_stairs"
        
        # LEAVE GAME        
        elif choice == "leave":
            animated_effect("You turn back towards the fog outside the factory.", "info")
            return None
            
        else:
            animated_effect("Your footsteps echo through the empty hall.", "warning")
