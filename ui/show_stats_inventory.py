# ui/show_stats_inventory.py
# Displays the player's stats and inventory with simple formatting.

from .animated_text import animated_text

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
