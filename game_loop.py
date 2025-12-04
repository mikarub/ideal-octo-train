# game_loop.py
# ----------------------------------------------------
# Centralized game loop controlling navigation,
# inventory, quests, save/load and player stats.
# ----------------------------------------------------

from ui.animated_text import animated_text
from ui.spinner_input import spinner_input
from ui.show_stats_inventory import show_stats_inventory
from engine.save_system import save_game_slot, quick_save, quick_load, delete_save_slot, list_save_slots_return, list_save_slots_print
from ui import THEMES

from save_load import save_menu
from inventory import combine_items_menu
from quests.hollowbridge_factory import enter_factory


# ----------------------------------------------------
# MAIN GAME LOOP
# ----------------------------------------------------

def main():
    theme = THEMES["victorian"]

    # Initial player stats
    stats = {
        "Health": 10,
        "Agility": 5,
        "Luck": 3
    }

    # Player inventory
    inventory = []

    # Save metadata (shared across modules)
    save_state = {
        "last_slot": None,
        "visited": {},
        "choices": {},
        "notes": ""
    }

    animated_text("=== RPG: Hollowbridge Prologue ===\n", color=theme["accent"])
    animated_text("Type 'exit' at any prompt to quit the game.\n", color=theme["text_color"])
    animated_text("Type 'save' at the main menu to open the Save Menu.", color=theme["text_color"])
    animated_text("You may also combine items using the 'combine' command.\n", color=theme["text_color"])

    # ------------------------------
    # GAME LOOP
    # ------------------------------
    while True:
        choice = spinner_input(
            "\nChoose: [enter quest / inventory / combine / save / exit] ",
            theme
        ).strip().lower()

        if choice == "exit":
            animated_text("Farewell, wanderer.", color=theme["text_color"])
            break

        # ---------- Inventory ----------
        elif choice in ("inventory", "inv"):
            show_stats_inventory(stats, inventory, theme)

        # ---------- Combine Items ----------
        elif choice in ("combine", "craft", "use"):
            combine_items_menu(inventory, theme)

        # ---------- Save Menu ----------
        elif choice == "save":
            save_menu(
                {"hp": stats.get("Health", 10), "items": inventory.copy()},
                stats,
                inventory,
                save_state,
                theme
            )

        # ---------- Enter Quest ----------
        elif choice in ("enter quest", "quest", "enter", "start"):
            enter_factory(stats, inventory, theme, save_state)

        else:
            animated_text("Command not recognised.", color=theme["text_color"])


# ----------------------------------------------------
# Run directly
# ----------------------------------------------------

if __name__ == "__main__":
    main()
