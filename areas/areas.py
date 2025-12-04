# areas.py
# ----------------------------------------------------
# Handles area metadata, visited flags, notes system,
# and helper functions for location-based interactions.
# ----------------------------------------------------

from ui import animated_text


# ----------------------------------------------------
# Area Definitions
# ----------------------------------------------------
# These can later be expanded into a folder structure:
# areas/town.py, areas/forest.py, etc.
# ----------------------------------------------------

AREAS = {
    "hollowbridge_factory": {
        "name": "Ruins of Hollowbridge Factory",
        "description": (
            "A towering, skeletal frame of rusted iron and shattered glass. "
            "The wind moans through warped beams like a dying organ."
        )
    },

    "hollowbridge_yard": {
        "name": "Factory Yard",
        "description": (
            "Broken crates and moss-covered tools lie scattered. "
            "Footsteps echo where workers once toiled."
        )
    },

    "old_quarters": {
        "name": "Abandoned Workers’ Quarters",
        "description": (
            "Sagging bunks, torn clothes, and diary scraps frozen in time. "
            "The air tastes of soot and forgotten sorrow."
        )
    },
}


# ----------------------------------------------------
# Notes system
# ----------------------------------------------------

def add_note(save_state, text):
    """
    Adds player notes to the save_state["notes"] string.
    """
    if not isinstance(text, str):
        return
    if save_state.get("notes") is None:
        save_state["notes"] = ""

    if text.strip():
        save_state["notes"] += "- " + text.strip() + "\n"


def show_notes(save_state, theme):
    """
    Displays collected notes.
    """
    animated_text("\n--- Notes ---", color=theme["accent"])

    notes = save_state.get("notes", "").strip()

    if not notes:
        animated_text("You have no notes recorded.", color=theme["text_color"])
        return

    animated_text(notes, color=theme["text_color"])


# ----------------------------------------------------
# Visited area tracking
# ----------------------------------------------------

def mark_visited(save_state, area_id):
    """
    Marks an area as visited.
    """
    if "visited" not in save_state:
        save_state["visited"] = {}

    save_state["visited"][area_id] = True


def has_visited(save_state, area_id):
    """
    Checks if the player has visited the area before.
    """
    return save_state.get("visited", {}).get(area_id, False)


# ----------------------------------------------------
# Entering an area
# ----------------------------------------------------

def enter_area(area_id, save_state, theme):
    """
    Generic area-entrance handler.
    Prints description only the first time.
    """

    if area_id not in AREAS:
        animated_text("This area does not exist.", color=theme["text_color"])
        return

    data = AREAS[area_id]

    first_time = not has_visited(save_state, area_id)

    animated_text(f"\n== {data['name']} ==", color=theme["highlight"])

    if first_time:
        animated_text(data["description"], color=theme["text_color"])
        mark_visited(save_state, area_id)
    else:
        animated_text("(You've been here before.)", color=theme["dimmed"])

    # Return data for quests or gameplay that reacts to areas
    return data
