# quests/hollowbridge_factory/entry.py
from ui.animated_text import animated_text, animated_effect
from ui.spinner_input import spinner_input
from scenes.runner import register_scene, run_scene

@register_scene("enter_factory")
def enter_factory(stats, inventory, theme, save_state):
	animated_text("\nYou push open the heavy metal doors.", color=theme["text_color"])
	animated_text("They groan loudly, echoing through the vast factory interior.", color=theme["text_color"])
	from scenes.runner import SCENE_REGISTRY
	print(SCENE_REGISTRY.keys())
			
	if not save_state.get("visited", {}).get("factory_entered"):
		animated_effect("A cloud of dust rises as your footsteps disturb long-settled debris.", "info")
		save_state.setdefault("visited", {})["factory_entered"] = True
		
	while True:
		choice = spinner_input("[enter hall / leave]: ", theme).strip().lower()

		if choice == "enter hall":
			return "factory_hall"

		if choice == "inspect doors":
			#animated_text("The doors are reinforced steel. Whatever was built here, it mattered.", theme["accent"])
			print("The doors are reinforced steel. Whatever was built here, it mattered.")
			
		elif choice == "leave":
			animated_effect("You step back into the fog-lined street.", "info")
			return None

		else:
			animated_effect("You pause, unsure.", "warning")
