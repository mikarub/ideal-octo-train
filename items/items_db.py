# items/items_db.py
ALL_ITEMS = [
    "brass_gear",
    "oil_can",
    "tinkers_screwdriver",
    "bottle_of_oil",
    "strange_spring",
    "cloth_bundle",
    "vial_of_gear_oil",
    "hidden_blueprint",
    "repaired_console_note",
    "silenced_core_fragment",
    "shadow_token",
    "golden_amulet",
    "photonic_lens",
    "mystic_key",
    "chest_of_wonders",
    "clockwork_core",
    "lensed_gear",
    "repaired_toolset",
    "lubricant_mixture",
    "engine_map_fragment",
    "oiled_gear",
    "resonant_spring",
    "double_gear",
    "stabilised_lens",
    "maintenance_kit",
    "stealth_gear_fragment",
    "stabiliscope",
    "resonator",
    "winding_key",
    "soldered_plate",
    "glass_eye"
]

ITEM_CATEGORIES = {
    "components": ["brass_gear", "strange_spring", "photonic_lens", "double_gear", "glass_eye"],
    "tools": ["tinkers_screwdriver", "repaired_toolset", "winding_key"],
    "consumables": ["oil_can", "bottle_of_oil", "vial_of_gear_oil", "lubricant_mixture"],
    "relics": ["hidden_blueprint", "mystic_key", "golden_amulet", "chest_of_wonders"],
    "finished": ["clockwork_core", "silenced_core_fragment"]
}

CRAFTING_RECIPES = {
    # core machine builds
    ("brass_gear", "strange_spring"): "clockwork_core",
    ("brass_gear", "photonic_lens"): "lensed_gear",
    ("brass_gear", "brass_gear"): "double_gear",
    ("double_gear", "strange_spring"): "resonant_spring",
    ("resonant_spring", "photonic_lens"): "stealth_gear_fragment",
    ("strange_spring", "mystic_key"): "resonant_spring",
    ("photonic_lens", "repaired_console_note"): "stabilised_lens",

    # tools / maintenance
    ("tinkers_screwdriver", "cloth_bundle"): "repaired_toolset",
    ("repaired_toolset", "lubricant_mixture"): "maintenance_kit",
    ("bottle_of_oil", "vial_of_gear_oil"): "lubricant_mixture",

    # small useful combos
    ("brass_gear", "oil_can"): "oiled_gear",
    ("oiled_gear", "winding_key"): "winding_assembly",
    ("hidden_blueprint", "mystic_key"): "engine_map_fragment",
    ("engine_map_fragment", "clockwork_core"): "silenced_core_fragment",

    # lens / sensor combos
    ("lensed_gear", "resonant_spring"): "steg_lens_assembly",
    ("steg_lens_assembly", "repaired_toolset"): "stabiliscope",

    # decoration or utility
    ("cloth_bundle", "glass_eye"): "doll_eye_talisman",
    ("soldered_plate", "brass_gear"): "reinforced_plate",

    # late game variety
    ("maintenance_kit", "stabiliscope"): "engine_tuning_kit",
    ("shadow_token", "golden_amulet"): "phantom_relic",
    ("photonic_lens", "glass_eye"): "eye_of_lens",
    ("clockwork_core", "stabiliscope"): "stabilised_core_fragment",
    ("stealth_gear_fragment", "winding_key"): "stealth_gear"
}

def possible_recipes_for_inventory(inventory):
    inv_set = set(inventory)
    results = []
    for (a, b), out in CRAFTING_RECIPES.items():
        if a in inv_set and b in inv_set:
            results.append(((a, b), out))
        elif b in inv_set and a in inv_set:
            results.append(((b, a), out))
    return results

def get_recipe_result(a, b):
    return CRAFTING_RECIPES.get((a, b)) or CRAFTING_RECIPES.get((b, a))
