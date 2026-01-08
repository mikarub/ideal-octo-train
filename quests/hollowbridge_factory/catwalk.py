# quests/hollowbridge_factory/catwalk.py
from ui.animated_text import animated_text, animated_effect
from ui.spinner_input import spinner_input
from scenes.runner import register_scene, run_scene

@register_scene("factory_catwalk")
def catwalk_scene(stats, inventory, theme, save_state):
    visited = save_state.setdefault("visited", {})
    flags = save_state.setdefault("flags", {})
    
    animated_text("A narrow catwalk stretches over the factory floor. Machinery lies dormant below.", color=theme["text_color"])
    
    if not visited.get("catwalk"):
        animated_effect("From here, you can see the engine room through a shattered window.", "info")
        animated_effect("A control panel inside flickers faintly.", "info")
        visited["catwalk"] = True

    while True:
        choice = spinner_input("[inspect engine / cross / go back]: ", theme).strip().lower()
        
        # INSPECT ENGINE
        if choice == "inspect engine":
            animated_effect("Pressure gauges, valves and a cold ignition chamber.", "info")
            animated_effect("You'll need power and proper sequencing to start it.", "info")
            flags["engine_access"] = True
            
        # CROSS CATWALK
        elif choice == "cross":
            if not flags.get("engine_access"):
                animated_effect("You don't understand the machinery well enough yet.", "warning")
            else:
                animated_effect("You carefully cross toward the engine room door.", "info")
                return "factory_engine"
        
        # GO BACK
        elif choice == "go back":
            animated_effect("You retreat down the stairs.", "info")
            return "factory_stairs"
            
        else:
            animated_effect("The metal grating vibrates beneath your boots.", "warning")
