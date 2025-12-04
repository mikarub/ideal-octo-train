# save_load.py
# ----------------------------------------------------
# Handles save & load operations, slot management,
# serialization, and integration with the main loop.
# ----------------------------------------------------

import os
import json
from ui import animated_text
from ui import spinner_input


SAVE_DIR = "saves"


# ----------------------------------------------------
# Utility: ensure directory
# ----------------------------------------------------

def ensure_save_directory():
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)


# ----------------------------------------------------
# Slot listing
# ----------------------------------------------------

def list_save_slots_return():
    """
    Returns a list of save slot names by scanning SAVE_DIR.
    Slot names are saved as JSON files:  <slot_name>.json
    """
    ensure_save_directory()
    files = os.listdir(SAVE_DIR)
    slots = []
    for f in files:
        if f.endswith(".json"):
            slots.append(f[:-5])  # remove .json
    slots.sort()
    return slots


# ----------------------------------------------------
# Choose slot to LOAD
# ----------------------------------------------------

def choose_slot_for_load():
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


# ----------------------------------------------------
# Choose slot to SAVE
# ----------------------------------------------------

def choose_slot_for_save():
    slots = list_save_slots_return()

    print("\n--- Choose a slot to SAVE ---")
    if slots:
        for i, s in enumerate(slots, start=1):
            print(f"[{i}] {s}")
    else:
        print("(No existing slots)")

    print("[N] New slot")
    print("[B] Back")

    while True:
        choice = input("Choose slot number to overwrite, N to create new or B to cancel: ").strip().lower()
        if choice in ("b", "back"):
            return None
        if choice in ("n", "new"):
            name = input("Enter a name for the new slot (no spaces recommended): ").strip()
            if name:
                return name
            else:
                print("Invalid name.")
        elif choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(slots):
                return slots[idx]
            else:
                print("Invalid slot number.")
        else:
            print("Invalid option.")


# ----------------------------------------------------
# Save data structure
# ----------------------------------------------------

def build_save_data(stats, inventory, save_state):
    """
    Produces a clean dictionary ready for JSON saving.
    """
    data = {
        "player": {
            "stats": stats,
            "inventory": inventory
        },
        "state": {
            "visited": save_state.get("visited", {}),
            "choices": save_state.get("choices", {}),
            "notes": save_state.get("notes", "")
        }
    }
    return data


# ----------------------------------------------------
# SAVE
# ----------------------------------------------------

def perform_save(slot_name, stats, inventory, save_state, theme):
    ensure_save_directory()
    data = build_save_data(stats, inventory, save_state)

    path = os.path.join(SAVE_DIR, f"{slot_name}.json")
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

    save_state["last_slot"] = slot_name
    animated_text(f"Game saved to slot '{slot_name}'.", color=theme["accent"])


# ----------------------------------------------------
# LOAD
# ----------------------------------------------------

def perform_load(slot_name, stats, inventory, save_state, theme):
	ensure_save_directory()
	path = os.path.join(SAVE_DIR, f"{slot_name}.json")
	
	if not os.path.exists(path):
		animated_text("That save file no longer exists.", color=theme["dimmed"])
		return False
		
	with open(path, "r") as f:
		data = json.load(f)
		
	# Inject into existing structure
	stats.clear()
	stats.update(data["player"].get("stats", {}))
	inventory.clear()
	inventory.extend(data["player"].get("inventory", []))

	# NEW: Backwards compatible loading
	if "state" in data:
		state = data["state"]
		save_state["visited"] = state.get("visited", {})
		save_state["choices"] = state.get("choices", {})
		save_state["notes"] = state.get("notes", "")
	else:
		# OLD save (pre-modularization)
		save_state["visited"] = data.get("visited", {})
		save_state["choices"] = data.get("choices", {})
		save_state["notes"] = data.get("notes", "")
		
	save_state["last_slot"] = slot_name
	
	animated_text(f"Game loaded from slot '{slot_name}'.", color=theme["highlight"])
	return True


# ----------------------------------------------------
# SAVE MENU
# ----------------------------------------------------

def save_menu(dummy_player_obj, stats, inventory, save_state, theme=None):
    """
    Combined save/load interface.
    """
    print("\n===== Save Menu =====")
    print("[1] Save Game")
    print("[2] Load Game")
    print("[3] Back")

    while True:
        choice = input("Choose: ").strip()
        if choice == "1":
            slot = choose_slot_for_save()
            if slot:
                perform_save(slot, stats, inventory, save_state, theme)
            return
        elif choice == "2":
            slot = choose_slot_for_load()
            if slot:
                perform_load(slot, stats, inventory, save_state, theme)
            return
        elif choice == "3":
            return
        else:
            print("Invalid choice.")
