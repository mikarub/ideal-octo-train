# inventory/combine_items_core.py
from ui.animated_text import animated_text, animated_effect
from ui.spinner_input import spinner_input
from items.items_db import CRAFTING_RECIPES, possible_recipes_for_inventory, get_recipe_result
import time

def combine_items_with_suggestions(inventory, theme, save_state=None):
    if len(inventory) < 2:
        animated_effect("You need at least 2 items to combine.", "warning")
        return None
    animated_text("Your inventory:", color=theme["accent"])
    for i, it in enumerate(inventory, start=1):
        animated_text(f" [{i}] {it}", color=theme["text_color"])
    suggestions = possible_recipes_for_inventory(inventory)
    if suggestions:
        animated_text("\nSuggested combinations:", color=theme["prompt_color"])
        for i, ((a, b), out) in enumerate(suggestions, start=1):
            animated_text(f" [{i}] {a} + {b} -> {out}", color=theme["text_color"])
        choice = spinner_input("\nPick suggestion number to craft, or type 'manual' to pick items: ", theme).strip().lower()
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(suggestions):
                (a, b), out = suggestions[idx]
                try:
                    inventory.remove(a)
                    inventory.remove(b)
                except ValueError:
                    animated_effect("One of the required items is missing.", "warning")
                    return None
                inventory.append(out)
                animated_effect(f"Combined {a} + {b} -> {out}", "info")
                if save_state is not None:
                    save_state.setdefault("last_craft", out)
                # trigger global combination hook if present
                try:
                    from engine.engine_core import trigger_item_combination_event
                    if trigger_item_combination_event:
                        trigger_item_combination_event(out, inventory, theme)
                except Exception:
                    pass
                return out
            else:
                animated_effect("Invalid suggestion number.", "warning")
                return None
    # manual fallback
    animated_text("\nManual combine: choose two items by number or name.", color=theme["prompt_color"])
    a = spinner_input("First item (name or number): ", theme).strip()
    b = spinner_input("Second item (name or number): ", theme).strip()
    def resolve_choice(choice):
        if not choice:
            return None
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(inventory):
                return inventory[idx]
            else:
                return None
        return choice
    i1 = resolve_choice(a)
    i2 = resolve_choice(b)
    if not i1 or not i2 or i1 not in inventory or i2 not in inventory:
        animated_effect("One or both items not found.", "warning")
        return None
    out = get_recipe_result(i1, i2)
    if out:
        inventory.remove(i1)
        inventory.remove(i2)
        inventory.append(out)
        animated_effect(f"Combined {i1} + {i2} -> {out}", "info")
        if save_state is not None:
            save_state.setdefault("last_craft", out)
        try:
            from engine.engine_core import trigger_item_combination_event
            if trigger_item_combination_event:
                trigger_item_combination_event(out, inventory, theme)
        except Exception:
            pass
        return out
    else:
        animated_effect("Those items do not combine into anything useful.", "warning")
        return None
