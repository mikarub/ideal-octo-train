# quests/hollowbridge_factory/engine_room.py
from ui.animated_text import animated_text, animated_effect
from ui.spinner_input import spinner_input
from scenes.runner import register_scene, run_scene
import random
import time

@register_scene("factory_engine_room")
def engine_room_scene(stats, inventory, theme, save_state):
    animated_text("\nA faint hum echoes as you near the engine room.", color=theme["text_color"])
    animated_text("The massive generator flickers with unstable light.", color=theme["text_color"])
    visited = save_state.setdefault("visited", {})
    notes = save_state.setdefault("notes", "")

    # first-time description
    if not visited.get("factory_engine_first"):
        animated_effect("A central control panel sits cold and half-lit, panels dangling.", "info")
        visited["factory_engine_first"] = True

    # Provide choices: inspect panel (uses oil for hint), attempt repair (requires parts), examine surroundings
    while True:
        choice = spinner_input("[inspect panel / attempt repair / examine / back]: ", theme).strip().lower()

        if choice == "inspect panel":
            # if player has oil_can, consume it for extra hint
            if "oil_can" in inventory:
                animated_effect("You slick the panel's hinges with oil — a hidden schematic flutters into view.", "info")
                # consume oil can
                inventory.remove("oil_can")
                save_state["notes"] += "Engine schematic revealed: red-white-blue wiring order hint.\n"
            else:
                animated_effect("You inspect the panel but only see scorched wiring; something is missing.", "info")

        elif choice == "attempt repair":
            # require small_key or precision screwdriver or brass_gear to do certain repairs
            required = []
            if "precision_screwdriver" not in inventory:
                required.append("precision_screwdriver")
            if "brass_gear" not in inventory:
                required.append("brass_gear")

            if required:
                animated_effect(f"Repair attempt blocked: missing {', '.join(required)}.", "warning")
            else:
                # Basic repair minigame: simple three-step timed input or choice puzzle
                animated_effect("You begin a repair sequence. Keep your nerve.", "info")
                # Option: quick skill check with Agility or Luck
                agi = stats.get("Agility", 0)
                luck = stats.get("Luck", 0)
                # simpler deterministic puzzle: choose correct color order if schematic in notes
                if "wiring order" in save_state.get("notes", "") or "wiring hint" in save_state.get("notes", ""):
                    hint_known = True
                elif "wiring" in save_state.get("notes", ""):
                    hint_known = True
                else:
                    hint_known = False

                # If hint known, present the wiring puzzle
                if hint_known:
                    animated_text("Phase 1 — Diagnostics: read the flickering panel.", color=theme["text_color"])
                    animated_text("Which readout is most relevant? [voltage / frequency / temp] ", color=theme["text_color"])
                    ans = spinner_input("> ", theme).strip().lower()
                    if ans == "voltage":
                        animated_effect("You isolate a circuit. Proceed to phase 2.", "success")
                    else:
                        animated_effect("You misread diagnostics, spark! (-1 Health).", "warning")
                        stats["Health"] = max(0, stats.get("Health", 0) - 1)
                        continue

                    animated_text("Phase 2 — Wiring: which color to rethread first? [red / white / blue] ", color=theme["text_color"])
                    # pull hint from notes if present (we added 'red-white-blue' text earlier)
                    known_order = None
                    if "red-white-blue" in save_state.get("notes", ""):
                        known_order = ["red", "white", "blue"]

                    if known_order:
                        # accept correct sequence input
                        seq = spinner_input("Enter order separated by spaces (e.g. 'red white blue'): ", theme).strip().lower()
                        if seq == "red white blue":
                            animated_effect("Wiring aligned. Finalising repairs...", "success")
                            time.sleep(0.8)
                            animated_effect("The generator slows its frantic stutter — the hum calms.", "info")
                            # reward
                            if "Engine Stabilizer" not in inventory:
                                inventory.append("Engine Stabilizer")
                                animated_effect("You salvage an Engine Stabilizer.", "info")
                            # mark engine repaired
                            save_state.setdefault("choices", {})["engine_repaired"] = True
                        else:
                            animated_effect("You swapped the wrong leads — a shock throws you back (-2 Health).", "warning")
                            stats["Health"] = max(0, stats.get("Health", 0) - 2)
                    else:
                        animated_effect("You fumble the wiring without a schematic and are forced to stop (-1 Health).", "warning")
                        stats["Health"] = max(0, stats.get("Health", 0) - 1)
                else:
                    # no hint — more punishing outcome
                    animated_effect("Without a schematic the repair is guesswork — you abort after a spark.", "warning")
                    stats["Health"] = max(0, stats.get("Health", 0) - 1)

        elif choice == "examine":
            animated_text("The room houses pipes leading to a brass cage and maintenance consoles.", color=theme["text_color"])
            if "small_key" in inventory and "locked_box" not in save_state.get("visited", {}):
                animated_effect("A locked metal box on a shelf matches your small key.", "info")
                take = spinner_input("Open it? (y/n): ", theme).strip().lower()
                if take == "y":
                    animated_effect("Inside is a worn note: 'wiring: red-white-blue'.", "info")
                    save_state["notes"] += "red-white-blue\nwiring hint\n"
                    save_state.setdefault("visited", {})["locked_box"] = True
            else:
                animated_effect("Nothing else of use meets your eye.", "info")

        elif choice in ("back", "b", "leave"):
            return run_scene("factory_hall", stats, inventory, theme, save_state)

        else:
            animated_effect("The engine's air resists your attempt. Decide carefully.", "warning")
