# quests/hollowbridge_factory/engine_room.py
from ui.animated_text import animated_text, animated_effect
from ui.spinner_input import spinner_input
from scenes.runner import register_scene, run_scene

# engine puzzle runner (import here to avoid circulars)
from engine.engine_puzzle import run_engine_puzzle

SAFE_PRESSURE = (40, 60)

@register_scene("factory_engine")
def engine_room_scene(stats, inventory, theme, save_state):
    visited = save_state.setdefault("visited", {})
    flags = save_state.setdefault("flags", {})
    
    animated_text("The engine room smells of oil and cold metal. A massive turbine dominates the chamber..", color=theme["text_color"])
    
    if not visited.get("engine"):
        animated_effect("Three systems stand out: fuel valve, pressure gauge, ignition lever.", "info")
        visited["engine"] = True
        
    while True:
        choice = spinner_input("[fuel / pressure / ignite / inspect / leave]: ", theme).strip().lower()
        
        # INSPECT
        if choice == "inspect":
            if "pressure_manual" in inventory:
                animated_effect("Fuel feeds into a sealed chamber. Pressure must stabilize before ignition.", "info")
                animated_effect("Gauge markings suggest a safe range between {SAFE_PRESSURE[0]}-{SAFE_PRESSURE[1]}.", "info")
            else:
                animated_effect("You need to look in the pressure manual.", "warning")
        
        # FUEL
        elif choice == "fuel":
            if flags.get("fuel_open"):
                animated_effect("The fuel valve is already open.", "warning")
            else:
                animated_effect("You turn the fuel valve. A low hum fills the room.", "info")
                flags["fuel_open"] = True
                
        # PRESSURE
        elif choice == "pressure":
            if not flags.get("fuel_open"):
                animated_effect("There's no pressure without fuel.", "warning")
            else:
                animated_effect("You adjust the pressure regulator...", "info")
                flags["pressure_set"] = True
        
        # IGNITION    
        elif choice == "ignite":
            if not flags.get("fuel_open"):
                animated_effect("Ignition fails. The chamber is empty.", "danger")
            
            elif not flags.get("pressure_set"):
                animated_effect("The engine coughs ciolently and vents steam!", "danger")
                
                if "wrench" in inventory:
                    animated_effect("You brace the valve with the wrench, preventing damage.", "success")
                else:
                    animated_effect("Systems reset.", "warning")
                    flags.pop("fuel_open", None)
                    flags.pop("pressure_set", None)
                
            else:
                animated_effect("The turbine roars to life. Power surges through the factory.", "info")
                flags["engine_started"] = True
                return "factory_powered"
                            
        # LEAVE
        elif choice == "leave":
            animated_effect("You step back onto the catwalk.", "info")
            return "factory_catwalk"
            
        else:
            animated_effect("The engine vibrates impatiently.", "warning")
