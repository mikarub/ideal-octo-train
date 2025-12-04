# inventory/inventory_core.py
from items.items import CRAFTING_RECIPES, ALL_ITEMS
from ui.animated_text import animated_text, animated_effect

def show_inventory(inventory, theme):
    if not inventory:
        animated_effect("Inventory empty.", "info")
        return
    animated_text("Inventory:")
    for it in inventory:
        animated_text(" - " + it)

def combine_items(inventory, theme):
    if len(inventory) < 2:
        animated_effect("You need at least 2 items to combine.", "warning")
        return None

    animated_text("Choose two items to combine by number:")
    for i, item in enumerate(inventory, start=1):
        animated_text(f"[{i}] {item}")

    try:
        a = int(input("First item #: ").strip())
        b = int(input("Second item #: ").strip())
    except Exception:
        animated_effect("Invalid input.", "warning")
        return None

    if a == b or a < 1 or b < 1 or a > len(inventory) or b > len(inventory):
        animated_effect("Invalid selection.", "warning")
        return None

    i1 = inventory[a-1]
    i2 = inventory[b-1]
    key = frozenset([i1, i2])
    recipe = CRAFTING_RECIPES.get(key)
    if not recipe:
        animated_effect("Those items do not combine into anything useful.", "warning")
        return None

    # apply combine
    inventory.remove(i1)
    inventory.remove(i2)
    inventory.append(recipe["id"])
    animated_effect(f"Combined into {recipe['name']}!", "success")
    return recipe["id"]
    
def show_stats_inventory(stats, inventory, theme):
    """
    Display player stats and inventory.
    - stats: dict { "Health": int, "Agility": int, "Luck": int, ... }
    - inventory: list of item names
    - theme: dict containing color values (e.g. text_color, accent)
    """

    accent = theme.get("accent", None)
    text_color = theme.get("text_color", None)

    animated_text("\n=== CHARACTER STATUS ===", color=accent)

    # --- Stats block ---
    animated_text("Stats:", color=text_color)
    for key, value in stats.items():
        animated_text(f"  • {key}: {value}", color=text_color)

    # --- Inventory block ---
    animated_text("\nInventory:", color=text_color)

    if not inventory:
        animated_text("  (empty)", color=text_color)
    else:
        for item in inventory:
            animated_text(f"  • {item}", color=text_color)

    animated_text("========================\n", color=accent)
