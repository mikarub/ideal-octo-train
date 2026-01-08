# game_loop.py
import sys
from colorama import init
init(autoreset=True)
#from quests.hollowbridge_factory.entry import enter_factory
import quests.hollowbridge_factory
from engine.themes import THEMES
theme = THEMES["victorian"]

# Try to import the runner scene system (optional). If it's not present we'll call the quest directly.
try:
    from scenes.runner import run_scene
    have_runner = True
except Exception:
    have_runner = False

# safe imports for engine modules (not-fatal)
try:
	import engine.engine_handlers
except Exception:
	pass

try:
	import engine.engine_puzzle
except Exception:
	pass

# Save helpers: prefer engine.save_system, fall back to save_system.save_system
try:
    from engine.save_system import (
        list_save_slots_return,
        load_game_slot,
        quick_load,
        quick_save,
        save_game_slot
    )
except Exception:
    # fallback names/locations used previously in your tree
    try:
        from save_system.save_system import (
            list_save_slots_return,
            load_game_slot,
            quick_load,
            quick_save,
            save_game_slot
        )
    except Exception:
        # provide stubs so menu still runs (they'll raise if used)
        def list_save_slots_return(): return []
        def load_game_slot(slot): return None
        def quick_load(): return None
        def quick_save(*args, **kwargs): return False
        def save_game_slot(*args, **kwargs): return False
'''
# Try to import the quest entry point as a fallback
# adjust to your exact module path if different
try:
    from quests.hollowbridge_factory import enter_factory as fallback_enter_factory
except Exception:
    # some variants in your tree used different paths
    try:
        from game.quests.lament_factory import lament_of_hollowbridge_factory as fallback_enter_factory
    except Exception:
        fallback_enter_factory = None
'''

def choose_slot_numbered(slots):
    """Show numbered slots and return chosen slot name (or None)."""
    if not slots:
        print("\n(No save slots found)\n")
        return None
    print("\nAvailable save slots:")
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

# Try to import the quest entry point as a fallback
# adjust to your exact module path if different
try:
    from quests.hollowbridge_factory import lament_of_hollowbridge_factory as fallback_enter_factory
except Exception:
    # some variants in your tree used different paths
    try:
        from game.quests.lament_factory import lament_of_hollowbridge_factory as fallback_enter_factory
    except Exception:
        fallback_enter_factory = None


def choose_slot_numbered(slots):
    """Show numbered slots and return chosen slot name (or None)."""
    if not slots:
        print("\n(No save slots found)\n")
        return None
    print("\nAvailable save slots:")
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


def main():
	# basic defaults used if creating a new game
	if not isinstance(theme, dict):
		raise TypeError(f"Theme must be dict, got {type(theme)}")
		
	default_stats = {"Health": 10, "Agility": 5, "Luck": 3}
	default_inventory = []
	
	# Start menu
	print("\n=== HOLLOWBRIDGE: Prologue ===\n")
	print("1) New Game")
	print("2) Load Game (choose a slot)")
	print("3) Quick Load")
	print("4) Exit\n")
	
	choice = input("> ").strip()
	stats = default_stats.copy()
	inventory = default_inventory.copy()
	save_state = {"last_slot": None, "visited": {}, "choices": {}, "notes": ""}
	if choice == "2":
		# show numbered slots using the existing helper
		slots = list_save_slots_return()
		slot = choose_slot_numbered(slots)
		if slot:
			loaded = load_game_slot(slot)
			if loaded:
				player_data, visited, choices, notes, engine, meta = loaded
				# populate stats and inventory from engine block if present,
				# otherwise from player_data for compatibility
				engine_stats = engine.get("stats", {}) if engine else {}
				engine_inventory = engine.get("inventory", []) if engine else player_data.get("items", [])
				if engine_stats:
					stats.update(engine_stats)
				inventory.clear()
				inventory.extend(engine_inventory or player_data.get("items", []))
				# player hp override to keep compatibility
				stats["Health"] = player_data.get("hp", stats.get("Health", 10))
				save_state["visited"] = visited or {}
				save_state["choices"] = choices or {}
				save_state["notes"] = notes or ""
				save_state["last_slot"] = slot
				print(f"\nLoaded slot '{slot}'.\n")
			else:
				print("\nFailed to load slot — starting a new game instead.\n")
	elif choice == "3":
		loaded = quick_load()
		if loaded:
			player_data, visited, choices, notes, engine, meta = loaded
			engine_stats = engine.get("stats", {}) if engine else {}
			engine_inventory = engine.get("inventory", []) if engine else player_data.get("items", [])
			if engine_stats:
				stats.update(engine_stats)
			inventory.clear()
			inventory.extend(engine_inventory or player_data.get("items", []))
			stats["Health"] = player_data.get("hp", stats.get("Health", 10))
			save_state["visited"] = visited or {}
			save_state["choices"] = choices or {}
			save_state["notes"] = notes or ""
			save_state["last_slot"] = "quick"
			print("\nQuickload successful.\n")
		else:
			print("\nNo quicksave found — starting a new game.\n")
	elif choice == "4":
		print("Bye.")
		return
	else:
		print("\nStarting a New Game...\n")
		
	if have_runner:
		try:
			current_scene = "enter_factory"
			while current_scene:
				current_scene = run_scene(current_scene, stats, inventory, theme, save_state)
			print("\nThanks for playing.")
			return
		except Exception:
			import traceback
			traceback.print_exc()
	'''
	# fallback: call quest entry directly (if imported successfully)
	if fallback_enter_factory:
		fallback_enter_factory(stats, inventory, theme, save_state)
	else:
		raise RuntimeError("No scene runner or quest entry function available. Please wire run_scene or provide fallback_enter_factory.")
	'''

if __name__ == "__main__":
    main()


