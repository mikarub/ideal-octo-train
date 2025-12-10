# scenes/loot_map.py
"""
Loot placements keyed by scene name. Use this in your scene entry
points to place items once when a scene is first visited.
"""

LOOT_BY_SCENE = {
    "hall": ["brass_gear"],
    "upper_walkway": ["oil_can"],
    "workshop": ["tinkers_screwdriver", "cloth_bundle"],
    "storage": ["vial_of_gear_oil", "strange_spring"],
    "tool_shelf": ["soldered_plate"],
    "attic": ["hidden_blueprint"],
    "mannequin_row": ["glass_eye"],
    "basement": ["photonic_lens"],
    "engine_anteroom": ["winding_key"],
    "secret_chamber": ["mystic_key"],
    "chest_room": ["chest_of_wonders"]
}

def spawn_loot_for_scene(scene_name, inventory, save_state):
    visited = save_state.setdefault("visited", {})
    key = f"loot:{scene_name}"
    if visited.get(key):
        return []
    items = LOOT_BY_SCENE.get(scene_name, [])
    for it in items:
        if it not in inventory:
            inventory.append(it)
    visited[key] = True
    return items
