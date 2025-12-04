# quests/hollowbridge_factory.py

from ui.animated_text import animated_text, animated_effect
from ui.spinner_input import spinner_input
from engine.utils import timed_challenge

# =========================================
# AREA 1: MAIN HALL
# =========================================
def explore_hall(stats, inventory, theme, save_state):
    animated_text("\nThe main hall is filled with rusted machines.", color=theme["text_color"])
    animated_text("You hear faint dripping from somewhere deep within.", color=theme["text_color"])

    if not save_state["visited"].get("factory_hall_gears"):
        animated_effect("You find a Brass Gear among the rubble.", "info")
        inventory.append("brass_gear")
        save_state["visited"]["factory_hall_gears"] = True
    else:
        animated_effect("Nothing new catches your eye.", "info")


# =========================================
# AREA 2: STAIRS ➝ UPPER WALKWAY
# =========================================
def climb_stairs(stats, inventory, theme, save_state):
    animated_text("\nThe stairs creak under your weight.", color=theme["text_color"])

    if stats.get("Agility", 0) < 5:
        animated_effect("A step breaks! You fall and bruise yourself (-1 Health).", "warning")
        stats["Health"] = max(0, stats["Health"] - 1)
    else:
        animated_effect("You keep your balance expertly.", "info")

    if not save_state["visited"].get("factory_upper"):
        animated_text("You reach a dusty walkway overlooking the hall below.", color=theme["text_color"])
        animated_effect("You spot an Oil Can on a shelf.", "info")
        inventory.append("oil_can")
        save_state["visited"]["factory_upper"] = True
    else:
        animated_effect("The walkway holds nothing new.", "info")


# =========================================
# AREA 3: LOCKED DOOR TO BASEMENT
# =========================================
def inspect_locked_door(stats, inventory, theme, save_state):
    animated_text("\nA heavy steel door blocks the descent into the basement.", color=theme["text_color"])

    has_gear = "brass_gear" in inventory
    has_oil = "oil_can" in inventory

    if save_state["visited"].get("factory_door_unlocked"):
        animated_effect("The door is already unlocked. You can enter the basement now.", "info")
        return

    if has_gear and has_oil:
        animated_effect("You apply oil to the rusted hinges and insert the brass gear into the mechanism...", "info")
        animated_effect("The machinery grinds and the door shifts open.", "success")
        save_state["visited"]["factory_door_unlocked"] = True
    else:
        animated_effect("It won't budge. Something is missing.", "warning")
        if not has_gear:
            animated_text("You may need a Gear mechanism from the hall.", color=theme["text_color"])
        if not has_oil:
            animated_text("The hinges look completely seized — oil might help.", color=theme["text_color"])


# =========================================
# AREA 4: BASEMENT
# =========================================
def explore_basement(stats, inventory, theme, save_state):
    animated_text("\nYou descend into the dim basement.", color=theme["text_color"])
    animated_text("Pipes hiss with trapped pressure. A rank smell fills the air.", color=theme["text_color"])

    # Luck check encounter
    if not save_state["visited"].get("factory_basement"):
        if stats.get("Luck", 0) >= 4:
            animated_effect("You spot something glinting under a pipe — a Pressure Valve!", "success")
            inventory.append("pressure_valve")
        else:
            animated_effect("A sudden burst of steam startles you! (-1 Health)", "warning")
            stats["Health"] = max(0, stats["Health"] - 1)

        save_state["visited"]["factory_basement"] = True
    else:
        animated_effect("You have already searched this place thoroughly.", "info")


# =========================================
# AREA 5: CATWALK ABOVE THE HALL
# =========================================
def explore_catwalk(stats, inventory, theme, save_state):
    animated_text("\nYou climb a ladder to the high metal catwalk.", color=theme["text_color"])
    animated_text("The entire hall spreads below you like a dead mechanical beast.", color=theme["text_color"])

    if not save_state["visited"].get("factory_catwalk"):
        if stats.get("Agility", 0) < 6:
            animated_effect("A section of the railing collapses! You barely hold on. (-1 Health)", "warning")
            stats["Health"] = max(0, stats["Health"] - 1)
        else:
            animated_effect("You move with confidence along the shaky steel.", "info")

        animated_effect("At the far end, you find a Control Room Key hanging on a hook.", "success")
        inventory.append("control_key")
        save_state["visited"]["factory_catwalk"] = True
    else:
        animated_effect("The catwalk groans but offers nothing new.", "info")

# hollowbridge_factory.py (continued expansions)

# -----------------------------
# WORKSHOP
# -----------------------------
def explore_workshop(stats, inventory, theme, save_state):
    animated_text("\nThe workshop smells of oil and rust.", color=theme["text_color"])
    if not save_state["visited"].get("factory_workshop"):
        animated_effect("You find a Tinker's Screwdriver lying on a bench.", "info")
        inventory.append("tinkers_screwdriver")
        save_state["visited"]["factory_workshop"] = True
    else:
        animated_effect("The workshop is empty now.", "info")

# -----------------------------
# STORAGE ROOM
# -----------------------------
def explore_storage(stats, inventory, theme, save_state):
    animated_text("\nCrates are stacked high in the storage room.", color=theme["text_color"])
    if not save_state["visited"].get("factory_storage"):
        animated_effect("You discover a Bottle of Oil and a Cog.", "info")
        inventory.extend(["bottle_of_oil", "metal_cog"])
        save_state["visited"]["factory_storage"] = True
    else:
        animated_effect("Nothing else of interest remains here.", "info")

# -----------------------------
# ENGINE PREP ROOM
# -----------------------------
def approach_engine_room(stats, inventory, theme, save_state):
    animated_text("\nA faint hum echoes as you near the engine room.", color=theme["text_color"])
    if not save_state["visited"].get("factory_engine_prep"):
        # simple timed challenge
        #from engine.engine_core import timed_challenge  # adjust import if needed
        success = timed_challenge(
            "Avoid falling debris! Press 'd' quickly!", "d", theme, stats, inventory,
            timeout=4, effects={"success": {"Agility":1}, "failure":{"Health":-2}}
        )
        if success:
            animated_effect("You dodge the debris skillfully.", "success")
        else:
            animated_effect("You are struck slightly by debris.", "warning")
        save_state["visited"]["factory_engine_prep"] = True
    else:
        animated_effect("The room is quiet now, only the engine's distant hum remains.", "info")

# -----------------------------
# SECRET BALCONY / CATWALK
# -----------------------------
def explore_catwalk(stats, inventory, theme, save_state):
    animated_text("\nA narrow catwalk runs along the upper walls.", color=theme["text_color"])
    if not save_state["visited"].get("factory_catwalk"):
        animated_effect("You find a Hidden Blueprint and a small Vial of Gear Oil.", "info")
        inventory.extend(["hidden_blueprint", "vial_of_gear_oil"])
        save_state["visited"]["factory_catwalk"] = True
    else:
        animated_effect("Nothing new is revealed from above.", "info")


# =========================================
# AREA 6: CONTROL ROOM / FINALE
# =========================================
def control_room(stats, inventory, theme, save_state):
    animated_text("\nThe control room overlooks all of Hollowbridge Factory.", color=theme["text_color"])

    if "control_key" not in inventory:
        animated_effect("The control panel is locked behind a thick glass case.", "warning")
        return

    animated_effect("You unlock the glass cover and access the ancient controls.", "info")

    has_all_items = (
        "brass_gear" in inventory and
        "oil_can" in inventory and
        "pressure_valve" in inventory
    )

    if has_all_items:
        animated_text("With all components recovered, you can restart the generator.", color=theme["text_color"])
        animated_effect("You repair the mechanisms and pull the master lever...", "success")
        animated_text("The factory hums back to life. Lights flicker. Machines breathe again.", color=theme["accent"])
        save_state["visited"]["factory_completed_good"] = True
    else:
        animated_text("You could force an overload… or shut everything down forever.", color=theme["text_color"])
        animated_effect("You choose the path of silence. The factory dies completely.", "warning")
        save_state["visited"]["factory_completed_bad"] = True


# =========================================
# MAIN FACTORY ENTRY POINT
# =========================================
def enter_factory(stats, inventory, theme, save_state):
    animated_text("\nYou push open the heavy metal doors.", color=theme["text_color"])
    animated_text("They groan loudly, echoing through the vast factory interior.", color=theme["text_color"])

    if "factory_entered" not in save_state["visited"]:
        animated_effect("A cloud of dust rises as your footsteps disturb long-settled debris.", "info")
        save_state["visited"]["factory_entered"] = True

    while True:
        action = spinner_input("[hall / stairs / workshop / storage / catwalk / engine / leave]: ", theme).strip().lower()
        if action == "hall":
            explore_hall(stats, inventory, theme, save_state)
        elif action == "stairs":
            climb_stairs(stats, inventory, theme, save_state)
        elif action == "workshop":
            explore_workshop(stats, inventory, theme, save_state)
        elif action == "storage":
            explore_storage(stats, inventory, theme, save_state)
        elif action == "catwalk":
            explore_catwalk(stats, inventory, theme, save_state)
        elif action == "engine":
            approach_engine_room(stats, inventory, theme, save_state)
        elif action == "leave":
            return
        else:
            animated_effect("You pause, unsure.", "warning")

