# ==========================
# ui/save_menu.py
# Text-based save/load menu
# ==========================

from utils.textfx import animated_text, animated_effect, spinner_input
from utils.themes import THEMES
from game.saveload import (
	list_save_slots_return,
	list_save_slots_print,
	save_game_slot,
	load_game_slot,
	delete_game_slot,
	quick_save,
	quick_load
)

# ------------------------------
# Numbered slot chooser helpers
# ------------------------------
def choose_slot_for_load():
	"""
	Shows a numbered list of existing slots and returns the chosen slot name (string),
	or None if cancelled.
	"""
	slots = list_save_slots_return()
	if not slots:
		print("\n(No slots found)\n")
		return None
		
	print("\n--- Choose a slot to LOAD ---")
	for i, s in enumerate(slots, start=1):
		print(f"[{i}] {s}")
	print("[B] Back")
	
	while True:
		choice = input("Choose slot number to load (or B): ").strip().lower()
		if choice in ("b", "back"):
			return None
		if choice.isdigit():
			idx = int(choice) - 1
			if 0 <= idx < len(slots):
				return slots[idx]
		print("Invalid choice. Try again.")
		
def choose_slot_for_save():
	"""
	Shows existing slots and lets the player pick one to overwrite
	or create a new named slots. Returns slot name or None.
	"""
	slots = list_save_slots_return()
	print("\n--- Choose a slot to SAVE ---")
	if slots:
		for i, s in enumerate(slots, start=1):
			print(f"[{i}] {s}")
	else:
		print("No existing slots)")
		
	print("[N] New slot")
	print("[B] Back")
	
	while True:
		choice = input("Choose slot number to overwrite, N to create new or B to cancel: ").strip().lower()
		
		if choice in ("b", "back"):
			return None
		elif choice in ("n", "new"):
			name = input("Enter a name for the new slot (no spaces recommended): ").strip()
			if name:
				return name
			else:
				print("Invalid name.")
				continue
		if choice.isdigit():
			idx = int(choice) - 1
			if 0 <= idx < len(slots):
				return slots[idx]
			else:
				print("Invalid slot number.")
			else:
				print("Invalid option.")
				
# -------------
# Save Menu UI
# -------------
def save_menu(player, stats, inventory, save_state):
	"""
	Presents a save/load/delete UI with numbered slot selection.
	Commands:
		list
		save
		load
		delete
		quicksave
		quickload
		setslot <name>
		clearslot
		exit
	"""
	theme = THEMES["victorian"]
	animated_text("\n--- Save Menu ---", color=theme["accent"])
	animated_text("Commands: list | save | load | delete | quicksave | quickload | setslot <name | clearslot | exit",
			color=theme["text_color"])
			
	while True:
		cmd = spinner_input("\nEnter save command: ", theme).strip()
		if not cmd:
			continue
			
		parts = cmd.split()
		verb = parts[0].lower()
		
		# ----------
		# Exit menu
		# ----------
		if verb == "exit":
			break
			
		# ----------------
		# List save slots
		# ----------------
		elif verb == "list":
			list_save_slots_print()
			
		# ----------------------
		# Save a game to a slot
		# ----------------------
		elif verb == "save":
			slot = choose_slot_for_save()
			if slot:
				player_payload = {
					"hp": stats.get("Health", 10),
					"items": inventory.copy()
				}
				save_game_slot(
					slot,
					player_payload,
					save_state.get("visited", {}),
					save_state.get("choices", {}),
					save_state.get("notes", ""),
					stats,
					inventory
				)
				save_state["last_slot"] = slot
				
		# ---------------
		# Load from slot
		# ---------------
		elif verb == "load":
			slot = choose_slot_for_load()
			if slot:
				loaded = load_game_slot(slot)
				if loaded:
					player_data, visited, choices, notes, engine, meta = loaded
					
					stats_from_engine = engine.get("stats", {})
					inventory_from_engine = engine.get("inventory", player_data_get("items", []))
					
					# Apply loaded stats and inventory
					if stats_from_engine:
						stats.update(stats_from_engine)
						
					inventory.clear()
					inventory.extend(inventory_from_engine)
					
					stats["Health"] = player_data.get("hp", stats.get("Health", 10))
					
					save_state["visited"] = visited
					save_state["choices"] = choices
					save_state["notes"] = notes
					save_state["last_slot"] = slot
					
					animated_effect(f"Loaded slot '{slot}'.", "info")
				else:
					animated_effect(f"Failed to load slot '{slot}'.", "warning")
					
		# ------------
		# Delete slot
		# ------------
		elif verb == "delete":
			slot = choose_slot_for_load()
			if slot:
				confirm = input(f"Delete slot '{slot}'? Type 'YES' to confirm: ").strip()
				if confirm == "YES":
					delete_save_slot(slot)
					
		# ----------------
		# Quick save/load
		# ----------------
		elif verb == "quicksave":
			player_payload = {
				"hp": stats.get("Health", 10),
				"items": inventory.copy()
			}
			quick_save(
				player_payload(),
				save_state.get("visited", {}),
				save_state.get("choices", {}),
				save_state.get("notes", ""),
				stats,
				inventory
			)
			
		elif verb == "quickload":
			loaded = quick_load()
			if loaded:
				player_data, visited, choices, notes, engine, meta = loaded
				
				stats_from_engine = engine.get("stats", {})
				inventory_from_engine = engine.get("inventory", player_data.get("items", []))
				
				if stats_from_engine:
					stats.update(stats_from_engine)
					
				inventory.clear()
				inventory.extend(inventory_from_engine)
				
				stats["Health" = player_data.get("hp", stats.get("Health", 10))
				
				save_state["visited"] = visited
				save_state["choices"] = choices
				save_state["notes"] = notes
				
				animated_effect("Quickload successful.", "info")
			else:
				animated_effect("No quicksave found.", "warning")
				
		# -----------------------
		# Autosave slot controls
		# -----------------------
		elif verb == "setslot" and len(parts) >= 2:
			slot = "_".join(parts[1:])
			save_state["last_slot"] = slot
			animated_effect(f"Autosave slot set to '{slot}'. Autosaves will go to this slot.", "info")
			
		elif verb == "clearslot":
			save_state["last_slot"] = None
			animated_effect("Autosave slot cleared. Autosaves will go to quick slot.", "info")
			
		else:
			animated_text("Unknown command. Try: list/save/load/delete/quicksave/quickload/setslot/clearshot/exit",
				color=theme["text_color"])
