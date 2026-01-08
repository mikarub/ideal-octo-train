# scenes/interaction.py
from typing import Dict, Any, Callable, Optional, List, Tuple
from ui.animated_text import animated_text, animated_effect
from ui.spinner_input import spinner_input

# Utility / parser for hybrid input (simple verbs + short phrases)
VERB_SYNONYMS = {
    "look": ["look", "look around", "observe"],
    "inspect": ["inspect", "examine", "check", "study"],
    "take": ["take", "get", "pick", "pick up", "grab"],
    "use": ["use", "apply", "operate"],
    "go": ["go", "move", "walk", "enter", "go to", "head"],
    "inventory": ["inventory", "inv", "i"],
    "help": ["help", "?"],
    "quit": ["quit", "exit"],
}

def normalize_command(raw: str) -> Tuple[str, Optional[str], Optional[str]]:
    """Return (verb, target, target2) where verb is canonical verb string."""
    s = raw.strip().lower()
    if not s:
        return ("", None, None)
    # shortcut for single-word inventory / help
    for canon, forms in VERB_SYNONYMS.items():
        if s in forms:
            return (canon, None, None)
    # try to split on prepositions " on ", " with ", " to ", " at ", " into "
    for prep in (" on ", " with ", " to ", " at ", " into ", " using "):
        if prep in s:
            left, right = s.split(prep, 1)
            # detect verb in left
            left = left.strip()
            # if left has two words like "use panel", that's fine
            for canon, forms in VERB_SYNONYMS.items():
                for f in forms:
                    if left.startswith(f):
                        target = left[len(f):].strip()
                        if not target:
                            target = None
                        return (canon, target or None, right.strip() or None)
            # fallback: treat first word as verb, rest as target
            pieces = left.split(None, 1)
            verb = pieces[0]
            target = pieces[1] if len(pieces) > 1 else None
            return (verb, (target or None), right.strip() or None)

    # no prep found — try "verb target"
    pieces = s.split(None, 1)
    if len(pieces) == 1:
        # single word — could be verb or targetless command
        token = pieces[0]
        for canon, forms in VERB_SYNONYMS.items():
            if token in forms:
                return (canon, None, None)
        # otherwise treat as "inspect target"
        return ("inspect", token, None)
    else:
        candidate_verb, rest = pieces[0], pieces[1]
        # map synonyms
        for canon, forms in VERB_SYNONYMS.items():
            if candidate_verb in forms:
                return (canon, rest.strip() or None, None)
        # If the first word isn't a known verb, assume inspect
        return ("inspect", s, None)

# Game object/item structures:
# objects: {name: {"desc": str, "inspect": str|callable, "use": callable or dict, "can_take": bool}}
# items: {item_name: {"desc": str, "on_take": callable, "on_use": callable or dict}}
# exits: list of scene names (without prefix) or dict mapping alias->scene_id
#
# on_use callbacks receive signature: fn(actor_stats, inventory, scene_state, target_optional, save_state) -> bool/None

def run_interaction_scene(scene_id: str,
                          description: str,
                          objects: Dict[str, Dict[str, Any]],
                          items: Dict[str, Dict[str, Any]],
                          exits: List[str],
                          stats: Dict[str, Any],
                          inventory: List[str],
                          theme: Dict[str, Any],
                          save_state: Dict[str, Any],
                          room_state: Optional[Dict[str, Any]] = None):
    """
    Generic interaction loop for a room.
    - scene_id: id for saving visited flags etc.
    - description: printed once when entering (or when 'look')
    - objects: dict of interactive objects in room
    - items: dict of pickable items present (visible flag)
    - exits: list of exit scene names (strings)
    - room_state: persisted per-room temporary state (mutable dict)
    """
    if room_state is None:
        room_state = {}
    # ensure save_state structure exists
    visited = save_state.setdefault("visited", {})
    room_visited_flag = f"{scene_id}_entered"
    if not visited.get(room_visited_flag):
        animated_text(description, color=theme["text_color"])
        visited[room_visited_flag] = True
    else:
        animated_text(f"You are back at {scene_id.replace('_', ' ')}.", color=theme["text_color"])

    # build item visibility map
    item_visibility = {}
    for it_name, meta in items.items():
        item_visibility[it_name] = bool(meta.get("visible", True))

    # local helper functions
    def list_exits():
        animated_text("Exits: " + ", ".join(exits), color=theme["prompt_color"])

    def list_inventory():
        inv_text = ", ".join(inventory) if inventory else "Empty"
        animated_text(f"Inventory → {inv_text}", color=theme["accent"])

    def show_help():
        animated_text("Available verbs: look, inspect <obj>, take <item>, use <item> [on target], go <exit>, inventory, help", color=theme["text_color"])

    def resolve_target(name: str) -> Tuple[Optional[str], Optional[Dict[str, Any]]]:
        """Return ('object'/'item', meta) found, prioritise objects then visible items"""
        if not name:
            return (None, None)
        name = name.lower()
        # exact match - objects
        for oname, meta in objects.items():
            if oname.lower() == name or name in oname.lower():
                return ("object", meta)
        # items
        for iname, meta in items.items():
            if iname.lower() == name or name in iname.lower():
                if item_visibility.get(iname, True):
                    return ("item", meta)
        # fuzzy: find if any objects contain word
        for oname, meta in objects.items():
            if name in oname.lower() or name in (meta.get("aliases","")).lower():
                return ("object", meta)
        for iname, meta in items.items():
            if name in iname.lower() or name in (meta.get("aliases","")).lower():
                if item_visibility.get(iname, True):
                    return ("item", meta)
        return (None, None)

    # main loop
    while True:
        prompt = f"[{ ' / '.join(exits) } / look / inspect / take / use / inv / help / leave]: "
        raw = spinner_input(prompt, theme).strip()
        if not raw:
            continue
        verb, target, target2 = normalize_command(raw)

        # handle movement
        if verb == "go" and target:
            # map target to exit name exactly if possible
            chosen = None
            for ex in exits:
                if target in ex or ex in target or target == ex:
                    chosen = ex
                    break
            if chosen:
                # assume scenes.runner.run_scene exists and will be called by caller
                return chosen
            else:
                animated_effect("You can't go there.", "warning")
                continue

        if verb in ("quit",):
            return None

        if verb == "inventory":
            list_inventory()
            continue

        if verb == "help":
            show_help()
            continue

        if verb == "look":
            animated_text(description, color=theme["text_color"])
            # list visible items and objects
            visible_items = [n for n in items.keys() if item_visibility.get(n, True)]
            if visible_items:
                animated_text("You notice: " + ", ".join(visible_items), color=theme["accent"])
            if objects:
                animated_text("Nearby: " + ", ".join(objects.keys()), color=theme["text_color"])
            list_exits()
            continue

        # INSPECT
        if verb == "inspect":
            if not target:
                animated_effect("Inspect what?", "warning")
                continue
            typ, meta = resolve_target(target)
            if not typ:
                animated_effect("There's nothing like that here.", "warning")
                continue
            # meta can be a dict with 'inspect' key or 'desc'
            if typ == "object":
                func = meta.get("inspect")
                if callable(func):
                    func(stats, inventory, room_state, save_state)
                else:
                    animated_text(meta.get("inspect", meta.get("desc", "You see nothing special.")), color=theme["text_color"])
            else:  # item in world (not in inventory)
                animated_text(meta.get("desc", "It looks ordinary."), color=theme["text_color"])
            continue

        # TAKE
        if verb == "take":
            if not target:
                animated_effect("Take what?", "warning")
                continue
            typ, meta = resolve_target(target)
            if typ != "item":
                animated_effect("You cannot take that.", "warning")
                continue
            # check on_take hook
            if not meta.get("can_take", True):
                animated_effect("You can't take that.", "warning")
                continue
            item_name = None
            # find canonical name for that item key
            for k in items.keys():
                if target == k or target in k.lower():
                    item_name = k
                    break
            if not item_name:
                # fallback: take first matching visible item
                for k in items.keys():
                    if target in k.lower() and item_visibility.get(k, True):
                        item_name = k
                        break
            if not item_name:
                animated_effect("Item not found.", "warning")
                continue
            # actually take
            inventory.append(item_name)
            item_visibility[item_name] = False
            on_take = items[item_name].get("on_take")
            animated_effect(f"You take the {item_name}.", "info")
            if callable(on_take):
                on_take(stats, inventory, room_state, save_state)
            continue

        # USE
        if verb == "use":
            if not target:
                animated_effect("Use what?", "warning")
                continue
            # `target` may be an item in inventory or world. Check inventory first.
            target_key = None
            for inv_item in inventory:
                if target in inv_item.lower() or target == inv_item:
                    target_key = inv_item
                    break
            # resolve primary target (object to use on) from target2 if present
            if target_key and not target2:
                # using an inventory item without a target tries the item's on_use( ) if there
                meta = None
                if target_key in items:
                    meta = items[target_key]
                on_use = meta.get("on_use") if meta else None
                if callable(on_use):
                    ok = on_use(stats, inventory, room_state, None, save_state)
                    if ok is False:
                        animated_effect("It doesn't seem to work.", "warning")
                else:
                    animated_effect("You fiddle with it, but nothing happens.", "info")
                continue
            # target2: use <item> on <object>
            # first find item (inventory) and object (room)
            item_meta = None
            item_key = None
            if target_key:
                item_key = target_key
                item_meta = items.get(item_key, {})
            else:
                # maybe using a visible item in the world
                ttyp, tmeta = resolve_target(target)
                if ttyp == "item":
                    # pick world item key
                    for k in items.keys():
                        if target in k.lower():
                            item_key = k
                            item_meta = tmeta
                            break
            # resolve object to apply to
            o_typ, o_meta = resolve_target(target2) if target2 else (None, None)
            if o_typ != "object" and target2:
                animated_effect("There's nothing like that to use it on.", "warning")
                continue
            # try object's use handler first
            used = False
            if o_meta:
                handler = o_meta.get("use")
                if callable(handler):
                    result = handler(stats, inventory, room_state, (item_key or target), save_state)
                    used = True
                    # result semantics: True success, False fail, None neutral
                    if result is True:
                        animated_effect("It worked.", "success")
                    elif result is False:
                        animated_effect("That didn't do the trick.", "warning")
                    else:
                        # allow handler to produce own messages
                        pass
                else:
                    # object has no handler
                    used = False
            # if not used by object, try item-specific on_use
            if not used and item_key:
                item_on_use = items.get(item_key, {}).get("on_use")
                if callable(item_on_use):
                    res = item_on_use(stats, inventory, room_state, target2, save_state)
                    if res is True:
                        animated_effect("You used it successfully.", "success")
                    elif res is False:
                        animated_effect("Nothing happened.", "warning")
                    else:
                        pass
                    used = True
            if not used:
                animated_effect("You can't see how to use that here.", "warning")
            continue

        # fallback:
        animated_effect("I don't understand that command.", "warning")
