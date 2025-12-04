# inventory/inventory.py

from items import ALL_ITEMS, CRAFTING_RECIPES
from ui.animated_text import animated_effect

# --------------------------
# Display
# --------------------------
def show_inventory(inventory, theme):
    if not inventory:
        animated_effect("Your pockets are empty.", "info")
        return
    animated_effect("You carry:", "info")
    for item in inventory:
        data = ALL_ITEMS.get(item, {"name": item})
        print(f" – {data['name']}")

def show_stats_inventory(stats, inventory, theme):
    animated_effect("Your Condition:", "info")
    for key, val in stats.items():
        print(f"{key}: {val}")

    print("")
    show_inventory(inventory, theme)

# --------------------------
# Crafting / combining
# --------------------------
def combine_items(inventory, theme):
    """
    Smart multi-choice item combiner used in your main loop.
    """
    if len(inventory) < 2:
        animated_effect("Not enough items to combine.", "warning")
        return

    animated_effect("Which two items do you want to combine?", "info")

    # Show numbered list
    for i, item in enumerate(inventory, start=1):
        data = ALL_ITEMS.get(item, {"name": item})
        print(f"[{i}] {data['name']}")

    try:
        c1 = int(input("First item number: ").strip())
        c2 = int(input("Second item number: ").strip())
    except:
        animated_effect("Invalid selection.", "warning")
        return

    if c1 == c2 or c1 < 1 or c2 < 1 or c1 > len(inventory) or c2 > len(inventory):
        animated_effect("Invalid choice.", "warning")
        return

    i1 = inventory[c1 - 1]
    i2 = inventory[c2 - 1]

    key = frozenset([i1, i2])
    recipe = CRAFTING_RECIPES.get(key)

    if not recipe:
        animated_effect("Those items don't seem to combine.", "warning")
        return

    # Craft result
    crafted_id = recipe["id"]
    crafted_name = recipe["name"]
    animated_effect(f"You create: {crafted_name}", "info")

    # Remove ingredients
    inventory.remove(i1)
    inventory.remove(i2)
    inventory.append(crafted_id)
