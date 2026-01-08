# quests/hollowbridge_factory/stairs.py
from ui.animated_text import animated_text, animated_effect
from ui.spinner_input import spinner_input
from scenes.runner import register_scene, run_scene

@register_scene("factory_stairs")
def stairs_scene(stats, inventory, theme, save_state):
    visited = save_state.setdefault("visited", {})
    flags = save_state.setdefault("flags", {})
    
    animated_text("The stairwell groans under your weight. Rust flakes drift down like ash.", color=theme["text_color"])

    if not visited.get("stairs"):
        animated_effect("A broken handrail hangs loose. One wrong step could be fatal.", "warning")
        visited["stairs"] = True
        
    while True:
        choice = spinner_input("[climb / inspect / go back]: ", theme).strip().lower()
        
        # INSPECT
        if choice == "inspect":
            animated_effect("You test each step before committing. The structure might hold.", "info")
            flags["stairs_climbed"] = True
            flags["catwalk_access"] = True
            
        # CLIMB    
        if choice == "climb":
            if not flags.get("stairs_climbed"):
                animated_effect("You hesitate. Rushing this could be dangerous.", "warning")
            else:
                animated_effect("You reach the top of the stairwell.", "info")
                return "factory_catwalk"
        
        # GO BACK
        elif choice == "go back":
            animated_effect("You descend back into the hall.", "info")
            return "factory_hall"
        
        else:
            animated_effect("The stairs creak ominously.", "warning")
