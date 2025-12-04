# game/saveload.py
# Part 7/8 — Save/load backend module
# High‑level, file‑based JSON save system for the text adventure game.

import json
import os
import time
from datetime import datetime

SAVE_DIR = "saves"

if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

# -----------------------------
# Helpers
# -----------------------------

def _slot_path(slot_name: str) -> str:
    return os.path.join(SAVE_DIR, f"{slot_name}.json")


def _timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# -----------------------------
# Write operations
# -----------------------------

def save_game_slot(slot_name: str, player_data, visited, choices, notes, stats, inventory):
    """
    Create or overwrite a named save slot.
    """
    path = _slot_path(slot_name)
    payload = {
        "slot": slot_name,
        "timestamp": _timestamp(),
        "player": player_data,
        "visited": visited,
        "choices": choices,
        "notes": notes,
        "stats": stats,
        "inventory": inventory,
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    return True


def quick_save(player_data, visited, choices, notes, stats, inventory):
    """
    Save to a special `quick.json` slot.
    """
    return save_game_slot("quick", player_data, visited, choices, notes, stats, inventory)

# -----------------------------
# Read operations
# -----------------------------

def load_game_slot(slot_name: str):
    """
    Load a slot. Returns dict or None.
    """
    path = _slot_path(slot_name)
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def quick_load():
    return load_game_slot("quick")

# -----------------------------
# Listing / metadata
# -----------------------------

def list_saves():
    """
    Return metadata for all .json saves.
    """
    out = []
    for file in os.listdir(SAVE_DIR):
        if file.endswith(".json"):
            path = os.path.join(SAVE_DIR, file)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                out.append({
                    "slot": data.get("slot", file[:-5]),
                    "timestamp": data.get("timestamp", "unknown"),
                    "path": path
                })
            except Exception:
                continue
    return sorted(out, key=lambda x: x["timestamp"], reverse=True)

# -----------------------------
# Delete
# -----------------------------

def delete_slot(slot_name: str) -> bool:
    path = _slot_path(slot_name)
    if os.path.exists(path):
        os.remove(path)
        return True
    return False
