# ==========================================
# game/items.py
# Handles items data, combination rules and
# post-combination secret events.
# ==========================================

from utils.textfx import animated_text, animated effect, spinner_input
from utils.themes import THEMES

# ---------------------------------
# Master item database (expandable
# ---------------------------------
ITEMS = {
	"Healing Herb": {
		"desc": "A fragrant herb with minor healing properties."
	},
	"Lucky Coin": {
		"desc": "An old coin etched with a faint star."
	},
	"Boots": {
		"desc": "Sturdy leather boots."
	},
	"Cloak": {
		"desc": "A worn grey cloak with hidden pockets."
	},
	"Mystic Key": {
		"desc": "A strange key huming with energy."
	},
	"Chest of Wonders": {
		"desc": "Heavy chest sealed by ancient forces."
	},
	
	# Result items (crafted)
	"Elixir of Fortune": {
		"desc": "A shimmering vial that radiates luck."
	},
	"Stealth Gear": {
		"desc": "A silent fusion of cloak and boots. Shadows cling to it."
	},
	"Celestial Relic": {
		"desc": "A relic that vibrates faintly with cosmic resonance."
	},
	
	# Secret post-combination rewards
	"Golden Amulet": {"desc": "Warm to the touch. You feel luckier."},
	"Shadow Token": {"desc": "An obsidian chip that absorbs light."},
	"Phantom Amulet": {"desc": Flickersat the edge of vision."}
}

# --------------------------------
# Combination recipe lookup table
# ------------------- ------------
COMBINATION_RULES = {
	("Healing Herb", "Lucky Coin"): "Elixir of Fortune",
	("Boots", "Cloak"): "Stealth Gear",
	("Mystic Key", "Chest of Wonders"): "Celestial Relic"
}

# --------------------------------------------------
# Secret event triggers after a new item is created
# --------------------------------------------------
def trigger_item_combination_event(new_item, inventory, theme):
	""" Triggers hidden events when certain crafted items appear. """
	if new_item == "Elixir of Fortune":
		animated_effect("A whispered fortune follows... you feel luckier.", "success")
		inventory.append("Golden Amulet")
		
	elif new_item == "Stealth Gear":
		animated_effect("Shadows cling to you. A token slips into your pocket.", "info")
		inventory.append("Shadow Token")
		
	elif new_item == "Celestial Relic":
		animated_effect("A distant hum answers the relic... the world shifts slightly.", "success")
		inventory.append("Phantom Amulet")
		
# ------------------------
# Main combination engine
# ------------------------
def combine_items(inventory, theme):
	""" Combine two items from inventory using recipe database. """
	if len(inventory) < 2:
		animated_effect("You need at least 2 items to combine.", "warning")
		return None
	
	animated_text("Choose two items to combine by name.", color=theme["accent"])
	animated_text(f"Inventory: {', '.join(inventory)}", color=theme["text_color"])
	
	i1 = spinner_input("First item: ", theme).strip()
	i2 = spinner_input("Second item: ", theme).strip()
	
	if i1 not in inventory or i2 not in inventory:
		animated_effect("One or both items not found in inventory.", "warning")
		return None
		
	key = (i1, i2)
	key_rev = (i2, i1)
	
	if key not in COMBINATION RULES and key_rev not in COMBINATION RULES:
		animated_effect("The items do not combine into anything useful.", "warning")
		return None
		
	# Create item
	new_item = COMBINATION_RULES.get(key) or COMBINATION_RULES.get(key_rev)
	
	# Remove old items
	inventory.remove(i1)
	inventory.remove(i2)
	
	# Add the new one
	inventory.append(new_item)
	
	animated_effect(f"Combined items to create {new_item}!", "info")
	
	# Trigger hidden events
	trigger_item_combination_event(new_item, inventory, theme)
	
	return new_item









































