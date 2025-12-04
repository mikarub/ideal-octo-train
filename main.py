#!/usr/bin/env python3
# filename: main.py
# auth: miklenn/mikarub 2025
# desc: Entry point for Hollowbridge Prologue
# Part 1/8 of the refactor (absolute imports)

import sys
from engine.themes import THEMES
from engine.player import Player
from engine.ui import animated_text, spinner_input
from engine.save_system import save_menu
from quests.hollowbridge import lament_of_hollowbridge_factory

def main():
	# choose UI theme
	theme = THEMES.get("victorian")
	
	# create player (Player class defined in engine/player.py
	player = Player()
	
	# shared save_state used by save_system + quests
	save_state = {			
		"last_slot": None,	# autosave slot name or None for quick
		"visited": {},		# area visit tracking
		"choices": {},		# major choices
		"notes": ""			# free-form notes / clues
	}
	
	animated_text("=== RPG: Hollowbridge Prologue ===\n", color=theme["accent"])
	animated_text("Type 'exit' at any prompt to quit the demo.\n", color=theme["text_color"])
	animated_text("Type 'save' at the main menu to open the Save Menu.", color=theme["text_color"])
	
	# Main loop
	while True:
		
		choice = spinner_input("\nChoose: [enter quest / inventory / combine / save / exit] ", theme).strip().lower()
		if choice in ("exit", "quit"):
			animated_text("Farewell, wanderer.", color=theme["text_color"])
			break
			
		elif choice in ("inventory", "inv"):
			# Player should provide a method to pretty-print its status
			player.show_stats_(theme=theme)
		
		elif choice in ("combine", "craft"):
			# Player.combine_items() will be implemented in engine/player.py
			# and will use engine.items and engine.combine internally.
			player.combine_items(theme=theme)
				
			
		elif choice in ("save"):
			# open save menu UI; passes references so menu can mutate player/save state
			save_menu(player=player.to_payload(), stats=player.stats, inventory=player.inventory, save_state=save_state)
			
			# After load, ensure player's runtime object reflects loaded data (save_menu will mutate stats/inventory passed)
			player.sync_from_engine_state(stats=player.stats, inventory=player.inventory)
			
		elif choice in ("enter quest", "quest", "enter"):
			# The quest function expects stats, inventory lists, theme and save_state
			lament_of_hollowbridge_factory(stats=player.stats, inventory=player.inventory, theme=theme, save_state=save_state)
			
			# ensure Player object picks up any changes made directly to stats/inventory
			player.sync_from_engine_state(stats=player.stats, inventory=player.inventory)
			
		else:
			animated_text("Command not recognised.", color=theme["text_color"])
			
if __name__ == "__main__":
	main()
	
