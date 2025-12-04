# inventory/combine_items_menu.py

from ui.animated_text import animated_text, animated_effect
from items.items import CRAFTING_RECIPES

def combine_items_menu(inventory, theme):
    """
    Allows the player to attempt combining two items using the crafting recipes.
    """
    animated_text("\n-- Item Combination Menu --", color=theme["header_color"])

    if len(inventory) < 2:
        animated_effect("You don't have enough items to combine anything.", "warning")
        return

    # List items
    animated_text("Your items:", color=theme["text_color"])
    for idx, item in enumerate(inventory, 1):
        animated_text(f"{idx}. {item}", color=theme["text_color"])

    # Choose items
    try:
        animated_text("\nSelect the first item number:", color=theme["text_color"])
        i1 = int(input("> ")) - 1

        animated_text("Select the second item number:", color=theme["text_color"])
        i2 = int(input("> ")) - 1
    except ValueError:
        animated_effect("Invalid choice.", "warning")
        return

    if i1 < 0 or i1 >= len(inventory) or i2 < 0 or i2 >= len(inventory) or i1 == i2:
        animated_effect("Invalid item selection.", "warning")
        return

    item_a = inventory[i1]
    item_b = inventory[i2]

    # Check recipes
    pair = tuple(sorted([item_a, item_b]))
    result = CRAFTING_RECIPES.get(pair)

    if not result:
        animated_effect("Those items can't be combined.", "warning")
        return

    # Perform combination
    new_item = result
    inventory.remove(item_a)
    inventory.remove(item_b)
    inventory.append(new_item)

    animated_effect(f"You combine {item_a} + {item_b} → {new_item}!", "info")
