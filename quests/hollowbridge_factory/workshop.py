# quests/hollowbridge_factory/workshop.py
from ui.animated_text import animated_text, animated_effect
from ui.spinner_input import spinner_input
from scenes.runner import register_scene, run_scene

@register_scene("factory_workshop")
def workshop_scene(stats, inventory, theme, save_state):
    visited = save_state.setdefault("visited", {})
    #items = save_state.setdefault("items", {})
    
    animated_text("Workbenches line the walls. Tools lie scattered under a layer of grime.", color=theme["text_color"])
    
    if not visited.get("workshop"):
        animated_effect("Something metallic glints beneath a torn cloth.", "info")
        visited["workshop"] = True

    while True:
        choice = spinner_input("[inspect / take wrench / hall / leave]: ", theme).strip().lower()
        
        # INSPECT
        if choice == "inspect":
            animated_effect("Most tools are useless, but one wrench looks intact.", "info")
        
        # TAKE WRENCH 
        elif choice == "take wrench":
            if "wrench" in inventory:
                animated_effect("You already took the wrench.", "warning")
            else:
                animated_effect("You take the heavy wrench. It feels reassuring", "success")
                inventory.append("wrench")
    
        # HALL
        elif choice == "hall":
            animated_effect("You leave the workshop.", "info")
            return "factory_hall"
        
        # LEAVE
        elif choice == "leave":
            return "factory_hall"
        
        else:
            animated_effect("The workshop is silent.", "warning")
