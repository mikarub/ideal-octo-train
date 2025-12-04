# save_system/save_system.py
import os
import json
from datetime import datetime
from ui.animated_text import animated_text, animated_effect
from ui.spinner_input import spinner_input
from engine.utils import timed_challenge

SAVE_DIR = "saves"
QUICK_NAME = "_quick"

os.makedirs(SAVE_DIR, exist_ok=True)

def _slot_path(name):
    return os.path.join(SAVE_DIR, f"{name}.json")

def save_game_slot(slot_name, player, visited, choices, notes, stats=None, inventory=None):
    path = _slot_path(slot_name)
    data = {
        "meta": {"saved_at": datetime.utcnow().isoformat() + "Z", "slot_name": slot_name},
        "player": {"hp": player.get("hp"), "items": player.get("items", [])},
        "visited": visited,
        "choices": choices,
        "notes": notes,
        "engine": {"stats": stats or {}, "inventory": inventory or []}
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return True

def load_game_slot(slot_name):
    path = _slot_path(slot_name)
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def quick_save(player, visited, choices, notes, stats=None, inventory=None):
    return save_game_slot(QUICK_NAME, player, visited, choices, notes, stats, inventory)

def quick_load():
    return load_game_slot(QUICK_NAME)

def delete_save_slot(slot_name):
    path = _slot_path(slot_name)
    if os.path.exists(path):
        os.remove(path)
        return True
    return False

def list_save_slots_return():
    files = [f[:-5] for f in os.listdir(SAVE_DIR) if f.endswith(".json") and not f.startswith("_")]
    return sorted(files)

def list_save_slots_print():
    slots = list_save_slots_return()
    if not slots:
        print("\n(No save slots found)\n")
        return
    print("\nAvailable save slots:")
    for s in slots:
        with open(_slot_path(s), "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                saved_at = data.get("meta", {}).get("saved_at", "unknown")
                engine_stats = data.get("engine", {}).get("stats", {})
                health = engine_stats.get("Health", "-")
                inv = data.get("player", {}).get("items", [])
                inv_summary = ", ".join(inv[:3]) + ("..." if len(inv) > 3 else "")
                print(f" - {s} (saved: {saved_at}) HP:{health} items:[{inv_summary}]")
            except Exception:
                print(f" - {s} (corrupt)")
