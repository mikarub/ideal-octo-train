# game/quests/lament_factory.py
# Part 6/8 — The Lament of Hollowbridge Factory quest module
#
# Depends on:
#   - utils.animation: animated_text, animated_effect, spinner_input
#   - utils.themes: THEMES
#   - game.items: combine_items (and trigger_item_combination_event is used internally there)
#
# This module implements the quest flow and a small timed_challenge helper
# so the quest remains self-contained and runnable once the other modules exist.

import time
import random
import threading
import sys

# UI & theme helpers
from utils.animation import animated_text, animated_effect, spinner_input
from utils.themes import THEMES

# items / combine helpers (combine_items returns created item or None)
from game.items import combine_items

# -----------------------------
# Minimal cross-platform keypress helper
# -----------------------------
try:
    import msvcrt

    def key_pressed():
        return msvcrt.kbhit()

    def read_key():
        ch = msvcrt.getwch()
        return ch

except ImportError:
    import select, tty, termios

    def key_pressed():
        dr, dw, de = select.select([sys.stdin], [], [], 0)
        return bool(dr)

    def read_key():
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
        return ch

# -----------------------------
# Simple timed challenge utility (local to quest)
# -----------------------------
def timed_challenge(prompt, required_key, theme, stats, inventory, timeout=5, effects=None, reward_item=None, allow_skip=False):
    """
    Wait up to `timeout` seconds for the user to press `required_key`.
    Shows spinner while waiting using spinner_input style (but non-blocking).
    Returns True on success, False otherwise.
    Applies effects dict to stats on success/failure, and appends reward_item if provided.
    """
    animated_text(prompt, color=theme["accent"])

    stop_event = threading.Event()
    spinner_chars = itertools_cycle = None

    # lightweight spinner thread to avoid dependency on other spinner implementations
    def spinner():
        chars = ['|', '/', '-', '\\']
        idx = 0
        while not stop_event.is_set():
            sys.stdout.write('\r' + theme["accent"] + "React now! " + chars[idx % len(chars)] + " " + "\033[0m")
            sys.stdout.flush()
            time.sleep(0.10)
            idx += 1
        # clear line
        sys.stdout.write('\r' + ' ' * 40 + '\r')
        sys.stdout.flush()

    t = threading.Thread(target=spinner)
    t.daemon = True
    t.start()

    start = time.time()
    success = False
    try:
        while time.time() - start < timeout:
            if key_pressed():
                ch = read_key()
                if isinstance(ch, str) and ch:
                    if ch.lower() == required_key.lower():
                        success = True
                        break
                if allow_skip and ch in ("\r", "\n"):
                    break
            time.sleep(0.02)
    finally:
        stop_event.set()
        t.join()

    if success:
        animated_effect("✅ Success! You completed the challenge!", "success")
        if effects and "success" in effects:
            for k, v in effects["success"].items():
                stats[k] = max(0, stats.get(k, 0) + v)
        if reward_item:
            inventory.append(reward_item)
            animated_effect(f"You obtained: {reward_item}", "info")
    else:
        animated_effect("❌ Challenge failed (time ran out or wrong key).", "warning")
        if effects and "failure" in effects:
            for k, v in effects["failure"].items():
                stats[k] = max(0, stats.get(k, 0) + v)
    return success

# -----------------------------
# The quest function
# -----------------------------
def lament_of_hollowbridge_factory(stats, inventory, theme, save_state):
    """
    Play through the hollowbridge factory quest.
    stats: dict of player stats (modified in-place)
    inventory: list of item names (modified in-place)
    theme: theme dict (from THEMES)
    save_state: dict with 'last_slot', 'visited', 'choices', 'notes' (mutable)
    """

    visited = save_state.get("visited", {})
    choices = save_state.get("choices", {})
    notes = save_state.get("notes", "")

    animated_effect("You arrive at Hollowbridge Factory - night and smoke cling to the brickwork.", "info")
    time.sleep(0.35)
    animated_text("Rumours say the place breathes. The gate is ajar.", color=theme["text_color"])
    time.sleep(0.25)

    # Stage: Assembly Hall
    animated_text("\n→ Assembly Hall", color=theme["accent"])
    animated_text("You step into the hall. Conveyor belts creak even though no hands feed them.", color=theme["text_color"])

    dodge_ok = timed_challenge(
        "Step aside! Press 's' to leap away.",
        "s",
        theme,
        stats,
        inventory,
        timeout=4,
        effects={"success": {"Agility": 1}, "failure": {"Health": -1}},
        reward_item=None
    )

    if not dodge_ok:
        animated_text("You stumble back, scraped by a rusted bracket. Your coat is torn.", color=theme["text_color"])

    # ambience
    if random.random() < 0.6:
        animated_text("A belt clangs somewhere deeper in the hall — a rhythm to unsettle you.", color=theme["text_color"])

    # show status
    animated_text(f"Stats → {' | '.join([f'{k}: {v}' for k,v in stats.items()])}", color=theme["text_color"])
    animated_text(f"Inventory → {', '.join(inventory) if inventory else 'Empty'}", color=theme["accent"])

    # autosave (to last_slot if set, else quick) — best-effort: if save functions exist externally they will catch calls
    try:
        player_payload = {"hp": stats.get("Health", 10), "items": inventory.copy()}
        if save_state.get("last_slot") and hasattr(save_state, "__getitem__"):  # basic guard
            # The global save system (game.saveload) will be present in other parts.
            from game.saveload import save_game_slot, quick_save
            save_game_slot(save_state["last_slot"], player_payload, visited, choices, notes, stats, inventory)
        else:
            from game.saveload import quick_save
            quick_save(player_payload, visited, choices, notes, stats, inventory)
    except Exception:
        # If save system not yet wired, silently continue (it will be added in engine.save_system)
        pass

    time.sleep(0.45)

    # Stage: Clockwork Mannequin Storage
    animated_text("\n→ Clockwork Mannequin Storage", color=theme["accent"])
    animated_text("Rows upon rows of mannequins stand like sermon pews. Their glass eyes await.", color=theme["text_color"])
    time.sleep(0.3)
    animated_text("Each time you glance away, you sense a subtle shift in posture.", color=theme["text_color"])

    inspect_choice = spinner_input("Do you inspect a mannequin closely or move on? [inspect/move] ", theme).strip().lower()
    if inspect_choice == "inspect":
        animated_text("Leaning in, the mannequin's hand is warm - impossibly warm.", color=theme["text_color"])
        animated_effect("You find a scrap of paper tucked in its sleeve: '3' scribbled in hurried ink.", "info")
        inventory.append("Scrap: '3'")
    else:
        animated_text("You force your gaze forward; your eyes sting as if from long-held fear.", color=theme["text_color"])

    # mannequin movement scare
    if random.random() < 0.6:
        animated_text("When you turn back, a mannequin on the far row is now nearer than before.", color=theme["text_color"])
        brave = timed_challenge("Touch the mannequin? Press 't' to reach out.", "t", theme, stats, inventory,
                                timeout=5, effects={"success": {"Luck": 1}, "failure": {"Health": -1}})
        if brave:
            animated_effect("You feel a pulse - not of blood, but of memory. Words: 'Return to the Heart...'", "info")
            inventory.append("Whisper: 'Return to the Heart'")

    # show status
    animated_text(f"Stats → {' | '.join([f'{k}: {v}' for k,v in stats.items()])}", color=theme["text_color"])
    animated_text(f"Inventory → {', '.join(inventory) if inventory else 'Empty'}", color=theme["accent"])

    # autosave again (best-effort)
    try:
        player_payload = {"hp": stats.get("Health", 10), "items": inventory.copy()}
        if save_state.get("last_slot") and hasattr(save_state, "__getitem__"):
            from game.saveload import save_game_slot, quick_save
            save_game_slot(save_state["last_slot"], player_payload, visited, choices, notes, stats, inventory)
        else:
            from game.saveload import quick_save
            quick_save(player_payload, visited, choices, notes, stats, inventory)
    except Exception:
        pass

    time.sleep(0.4)

    # Allow player to try combining items before final showdown
    if "Mystic Key" in inventory and "Chest of Wonders" not in inventory:
        animated_effect("Your Mystic Key hums faintly; perhaps a chest lies ahead.", "info")

    want_combine = spinner_input("Do you want to attempt any item combinations before proceeding? [yes/no] ", theme).strip().lower()
    if want_combine == "yes":
        # Use the shared combine_items function from game.items
        created = combine_items(inventory, theme)
        if created:
            animated_effect(f"You created {created}.", "success")
        animated_text(f"Inventory → {', '.join(inventory) if inventory else 'Empty'}", color=theme["accent"])

        # autosave after combining (best-effort)
        try:
            player_payload = {"hp": stats.get("Health", 10), "items": inventory.copy()}
            if save_state.get("last_slot") and hasattr(save_state, "__getitem__"):
                from game.saveload import save_game_slot, quick_save
                save_game_slot(save_state["last_slot"], player_payload, visited, choices, notes, stats, inventory)
            else:
                from game.saveload import quick_save
                quick_save(player_payload, visited, choices, notes, stats, inventory)
        except Exception:
            pass

    time.sleep(0.5)

    # Final chamber
    animated_text("\n→ The Heart Engine", color=theme["accent"])
    animated_text("You pass beneath a ring of gears. The air thickens; your breath tastes metallic.", color=theme["text_color"])
    time.sleep(0.4)
    animated_effect("As you step closer, a chorus of half-voices threads through the gears: fragments cry out in half-remembered names.", "info")
    animated_text("You realise with a sickening clarity: the mannequins hold stolen consciousness—this engine devours fear to keep them alive.", color=theme["text_color"])

    choice_final = spinner_input("Do you attempt to quiet the engine (clever puzzle) or destroy it outright (force)? [quiet/destroy] ", theme).strip().lower()

    # autosave before final
    try:
        player_payload = {"hp": stats.get("Health", 10), "items": inventory.copy()}
        if save_state.get("last_slot") and hasattr(save_state, "__getitem__"):
            from game.saveload import save_game_slot, quick_save
            save_game_slot(save_state["last_slot"], player_payload, visited, choices, notes, stats, inventory)
        else:
            from game.saveload import quick_save
            quick_save(player_payload, visited, choices, notes, stats, inventory)
    except Exception:
        pass

    if choice_final == "quiet":
        animated_text("You attempt to align the gears to a pattern that soothes the stolen echoes.", color=theme["text_color"])
        puzzle_answer = spinner_input("Enter the calming phrase (hint: something of solace) or type 'fail' to abort: ", theme).strip().lower()
        if any(k in puzzle_answer for k in ("calm", "heart", "solace")):
            animated_effect("The gears hesitate. For a breath, the world holds its breath. The engine falters.", "success")
            safe_extract = timed_challenge("Now quickly - press 'e' to extract the core while it slumbers!", "e", theme, stats, inventory,
                                           timeout=6, effects={"success": {"Luck": 2}, "failure": {"Health": -3}},
                                           reward_item="Silenced Core Fragment")
            if safe_extract:
                animated_effect("You wrench a humming piece from the engine. Its sound is a child's lullaby.", "info")
                inventory.append("Silenced Core Fragment")
                animated_effect("The mannequins slump; the fragments still whisper, but their cries are muffled.", "info")
            else:
                animated_effect("Extraction failed - the engine sluices fear outward in a violent burst.", "warning")
                choice_final = "destroy"
        else:
            animated_effect("Your words tumble meaningless against the brass. The machine laughs - a grinding rasp.", "warning")
            stats["Health"] = max(0, stats.get("Health", 0) - 1)
            choice_final = "destroy"

    if choice_final == "destroy":
        animated_text("You decide: the horror must end. Destroy the Heart Engine.", color=theme["text_color"])

        bonus = 0
        if "Shadow Token" in inventory or "Stealth Gear" in inventory:
            animated_effect("Your acquired items make the approach surer: you move like a ghost.", "info")
            bonus += 1
        if "Golden Amulet" in inventory or "Phantom Amulet" in inventory:
            animated_effect("A relic hums, lending you courage.", "info")
            bonus += 1

        animated_text("You will need to perform three synchronised actions to rupture the core.", color=theme["text_color"])
        successes = 0

        if timed_challenge("Sever the outer gears! Press 'r' now!", "r", theme, stats, inventory, timeout=max(1, 4 - min(2, bonus)),
                           effects={"success": {}, "failure": {"Health": -2}}):
            successes += 1
        if timed_challenge("Smash the conduit feeding the heart! Press 'h' now!", "h", theme, stats, inventory, timeout=max(1, 4 - min(2, bonus)),
                           effects={"success": {}, "failure": {"Health": -2}}):
            successes += 1
        if timed_challenge("Deliver the final blow to the core! Press 'k' now!", "k", theme, stats, inventory, timeout=max(1, 3 - min(1, bonus)),
                           effects={"success": {}, "failure": {"Health": -4}}):
            successes += 1

        if successes >= 2:
            animated_effect("\nThe gear-sphere cracks. A keening noise fills the chamber as ribbons of light and steam pour forth.", "success")
            inventory.append("Released Echoes")
            stats["Luck"] = max(0, stats.get("Luck", 0) + 2)
            stats["Agility"] = max(0, stats.get("Agility", 0) + 1)
            animated_effect("You have destroyed the Heart Engine. The mannequins collapse, their bindings freed.", "info")
            animated_text("But in the rising steam, you feel the release of many voices — what you have set loose is unknown.", color=theme["text_color"])
        else:
            animated_effect("\nThe engine resists. Your blows ring hollow and you are thrown back by a pulse of dread.", "warning")
            stats["Health"] = max(0, stats.get("Health", 0) - 5)
            animated_text("You barely escape the chamber as machinery smashes and the factory convulses.", color=theme["text_color"])
            if random.random() < 0.5:
                animated_effect("You snatch a fragment as you flee — it hums with trapped memory.", "info")
                inventory.append("Hollow Fragment")

    # Final aftermath
    time.sleep(0.6)
    animated_text("\nYou stumble out into the cold night. The factory behind you groans and then falls silent.", color=theme["text_color"])
    animated_text("In the hush that follows, the city seems unchanged - but something in the fog feels different.", color=theme["text_color"])

    animated_text(f"Stats → {' | '.join([f'{k}: {v}' for k,v in stats.items()])}", color=theme["text_color"])
    animated_text(f"Inventory → {', '.join(inventory) if inventory else 'Empty'}", color=theme["accent"])

    # autosave final state (best-effort)
    try:
        player_payload = {"hp": stats.get("Health", 10), "items": inventory.copy()}
        if save_state.get("last_slot") and hasattr(save_state, "__getitem__"):
            from game.saveload import save_game_slot, quick_save
            save_game_slot(save_state["last_slot"], player_payload, visited, choices, notes, stats, inventory)
        else:
            from game.saveload import quick_save
            quick_save(player_payload, visited, choices, notes, stats, inventory)
    except Exception:
        pass

    if "Released Echoes" in inventory:
        animated_effect("News of strange dreams begins to ripple through the city. You have altered fate.", "info")

    animated_effect("Quest Complete: The Lament of Hollowbridge Factory", "success")
