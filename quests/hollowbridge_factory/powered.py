# quests/hollowbridge_factory/powered.py
from ui.animated_text import animated_text, animated_effect
from ui.spinner_input import spinner_input
from scenes.runner import register_scene, run_scene

@register_scene("factory_powered")
def factory_powered(stats, inventory, theme, save_state):
	animated_text("Lights flicker on across the factory. Somewhere, a locked door unlocks.", color=theme["accent"])
	animated_text("HOLLOWBRIDGE awakens.", color=theme["accent"])
	return None
