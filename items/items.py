# items/items.py
"""
Item registry and crafting recipes.
This file is authoritative for ALL_ITEMS and CRAFTING_RECIPES.
"""

ITEM_CATEGORIES = {
    "materials": ["Scrap Metal", "Cloth", "Wood", "Brass Gear", "Oil Can"],
    "consumables": ["Bandage", "Health Potion"],
    "tools": ["Lever Tool", "Refined Mechanism"],
    "quest": ["Old Gear", "Clockwork Core", "Engineer’s Logbook"]
}

# Flattened list
ALL_ITEMS = sorted({item for items in ITEM_CATEGORIES.values() for item in items})

# Optional descriptions
ITEM_DESCRIPTIONS = {
    "Scrap Metal": "Bent and broken metal pieces.",
    "Cloth": "A strip of torn fabric.",
    "Wood": "A short, sturdy pole.",
    "Brass Gear": "An ornate gear from factory machinery.",
    "Oil Can": "A small can of oil.",
    "Bandage": "Stops bleeding and heals small wounds.",
    "Health Potion": "Restores a chunk of health.",
    "Lever Tool": "Useful for prying and repairs.",
    "Refined Mechanism": "A repaired mechanical assembly.",
    "Old Gear": "Worn but valuable machine part.",
    "Clockwork Core": "Hums with strange power.",
    "Engineer’s Logbook": "Notes of an engineer."
}

# -----------------------
# CRAFTING_RECIPES
# keys are frozenset({ingredient_a, ingredient_b}) for order-independence
# -----------------------
CRAFTING_RECIPES = {
    frozenset(["Scrap Metal", "Cloth"]): {
        "id": "Makeshift Bandage",
        "name": "Makeshift Bandage",
        "description": "A simple bandage made from cloth and metal - odd, but useful."
    },
    frozenset(["Wood", "Brass Gear"]): {
        "id": "Lever Tool",
        "name": "Lever Tool",
        "description": "A crude lever useful for prying machinery."
    },
    frozenset(["Scrap Metal", "Oil Can"]): {
        "id": "Refined Mechanism",
        "name": "Refined Mechanism",
        "description": "A cleaned and oiled mechanism useful in repairs."
    },
    frozenset(["Old Gear", "Clockwork Core"]): {
        "id": "Glowing Rune Fragment",
        "name": "Glowing Rune Fragment",
        "description": "A fragment born from combining ancient parts."
    }
}

def get_item_description(item):
    return ITEM_DESCRIPTIONS.get(item, "An unremarkable object.")
