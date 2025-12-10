# engine/engine_puzzle.py
"""
Engine Puzzle handler — multi-phase repair puzzle for the Hollowbridge engine.
Register name: "engine_repair_panel" (so scenes calling that handler will find it).

Phases:
  1) Diagnostics (a simple multiple-choice "read the panel" check; gives hint)
  2) Wiring (connect three pairs by choosing matching indices)
  3) Capacitor timing (timed QTE using timed_challenge if available)
Outcomes:
  - Full success: add 'repaired_panel' and maybe a 'Silenced Core Fragment'
  - Partial success: add 'repaired_panel' but trigger a warning consequence
  - Failure: damage player Health and leave state unchanged

Integrations:
  - Uses save_state["visited"]["engine_attempts"]
  - Honors inventory items to give bonuses (precision_screwdriver, insulated_wire)
  - Uses animated_text/animated_effect/spinner_input from ui
  - Tries to use engine.engine_core.timed_challenge if available; otherwise uses a simple fallback
"""

import random
import time
from scenes.runner import register_special_handler
from ui.animated_text import animated_text, animated_effect
from ui.spinner_input import spinner_input

# Attempt to import the timed_challenge from engine_core (your project may provide it)
try:
    from engine.engine_core import timed_challenge as _timed_challenge
except Exception:
    _timed_challenge = None

# small helper wrapper to safely call timed_challenge or fallback
def call_timed_challenge(prompt, required_key, timeout=4):
    if _timed_challenge:
        try:
            return _timed_challenge(prompt, required_key, timeout=timeout)
        except Exception:
            pass
    # Fallback: print prompt, wait up to timeout for correct single-character input
    print(prompt)
    start = time.time()
    while time.time() - start < timeout:
        try:
            # non-blocking check is environment dependent — use simple input with reduced effect
            # we won't block for full timeout to keep behavior simple: ask user quickly
            ch = input(f"(Press '{required_key}' within {int(timeout)}s) >>> ").strip()
            if ch and ch[0].lower() == required_key.lower():
                return True
            else:
                return False
        except Exception:
            return False
    return False

def _diagnostics_phase(stats, inventory, theme, save_state):
    """
    Phase 1: diagnostics.
    Simple multiple-choice question that gives a hint for wiring.
    Returns True if player selects well (bonus), False otherwise (no penalty).
    """
    animated_text("\nPhase 1 — Diagnostics: read the flickering panel.", color=theme["text_color"])
    choices = [
        "A) The generator reports a grounding fault on sector 3.",
        "B) Capacitor pressure nominal; valves leaking.",
        "C) Wiring matrix: misrouted pairs detected (3 mismatches).",
    ]
    animated_text("Which readout is most relevant to a wiring repair?", color=theme["text_color"])
    for c in choices:
        animated_text(c, color=theme["text_color"], delay=0.005)
    answer = spinner_input("Choose A, B or C: ", theme).strip().lower()
    good = answer == "c"
    if good:
        animated_effect("Correct — the panel hints at exactly three mismatches.", "info")
        return True
    else:
        animated_effect("You note the panel but nothing obvious stands out.", "warning")
        return False

# --- Replace existing _wiring_phase with this Option C (hybrid) implementation ---

def _display_wiring_board(left, right, mapping):
    """
    Return a multiline string ASCII representation of current wiring state.
    mapping: dict left_index(str) -> right_index(str)
    """
    lines = []
    lines.append("   LEFT SOCKETS        MAPPINGS        RIGHT SOCKETS")
    lines.append("  ----------------    ---------    ----------------")
    for i, L in enumerate(left, start=1):
        li = str(i)
        mapped = mapping.get(li)
        if mapped:
            connector = f"  ─── [{mapped}] ──▶"
        else:
            connector = "  ─── [ ] ──▶"
        rdisplay = f"({mapped}) {right[int(mapped)-1]}" if mapped else "( ) ?"
        # show right side index or placeholder
        right_preview = f"({mapped}) {right[int(mapped)-1]}" if mapped else "( ) ?"
        # We'll show right socket list separately for clarity below
        lines.append(f"   [{li}] {L:12}{connector}")
    lines.append("\n Right sockets (index -> label):")
    for j, R in enumerate(right, start=1):
        lines.append(f"   ({j}) {R}")
    return "\n".join(lines)


def _wiring_phase(stats, inventory, theme, save_state):
    """
    Hybrid ASCII wiring UI (Option C).
    Player chooses a left socket (1-3), then a right socket (1-3) to connect.
    Commands: inspect, reset, done, help.
    Returns score: 2 = perfect, 1 = partial, 0 = fail.
    """
    animated_text("\nPhase 2 — Wiring: reconnect the misrouted pairs.", color=theme["text_color"])

    # canonical pairs (internal)
    left = ["L1 (red)", "L2 (blue)", "L3 (green)"]
    right_correct = ["R2 (blue)", "R3 (green)", "R1 (red)"]  # scrambled intentionally
    right = right_correct.copy()
    random.shuffle(right)

    # determine the correct mapping based on shuffled 'right'
    correct_map = {
        "1": str(right.index("R1 (red)") + 1),
        "2": str(right.index("R2 (blue)") + 1),
        "3": str(right.index("R3 (green)") + 1)
    }

    mapping = {}       # player mapping left_index -> right_index (strings)
    attempts = 0
    max_attempts = 6   # allow a few tries; player control mostly via 'done'

    # quick hint availability
    def show_hint():
        # If player has oil_can, consume it for a stronger hint
        if "oil_can" in inventory:
            inventory.remove("oil_can")
            # reveal one correct mapping explicitly
            # choose the first unmapped correct one:
            for left_idx in ("1", "2", "3"):
                if left_idx not in mapping:
                    correct_right = correct_map[left_idx]
                    animated_effect(
                        f"Using the oil can, you clean away grime and reveal faint etched lines: "
                        f"Left {left_idx} should connect to Right {correct_right}.",
                        "success"
                    )
                    return
            # fallback if everything already mapped:
            animated_effect("The oil can reveals no new information; everything is already mapped.", "info")
        else:
            # weaker hint (unchanged)
            animated_effect(
                "You study the sockets. The coloring seems related — "
                "red aligns with red, blue with blue, green with green.",
                "info"
            )

    while attempts < max_attempts and len(mapping) < 3:
        attempts += 1
        board = _display_wiring_board(left, right, mapping)
        animated_text("\n" + board, color=theme["text_color"])
        choice = spinner_input("Select action (format: left right OR command): ", theme).strip().lower()

        if not choice:
            animated_effect("No input provided.", "warning")
            continue

        if choice in ("help", "h", "?"):
            animated_text("Enter mappings like: 1 3  (meaning connect left 1 to right 3).", color=theme["prompt_color"])
            animated_text("Or use: inspect, reset, done", color=theme["prompt_color"])
            continue

        if choice in ("inspect", "i"):
            show_hint()
            continue

        if choice in ("reset", "r"):
            mapping.clear()
            animated_effect("Mappings cleared.", "info")
            continue

        if choice in ("done", "d"):
            # allow finishing early if at least one mapping set
            if len(mapping) == 0:
                animated_effect("You haven't mapped any connections yet.", "warning")
                continue
            break

        # parse "left right" style input; accept "1-3" or "1 3"
        entry = choice.replace("-", " ").split()
        if len(entry) != 2:
            animated_effect("Invalid format. Provide two indices like '1 3' or a command.", "warning")
            continue

        left_idx, right_idx = entry[0].strip(), entry[1].strip()
        if left_idx not in ("1", "2", "3") or right_idx not in ("1", "2", "3"):
            animated_effect("Indices must be 1, 2 or 3.", "warning")
            continue

        # disallow reusing a left index
        if left_idx in mapping:
            animated_effect(f"Left {left_idx} is already mapped to {mapping[left_idx]}. Use 'reset' to start over.", "warning")
            continue
        # disallow reusing a right index
        if right_idx in mapping.values():
            animated_effect(f"Right {right_idx} is already used by another mapping. Choose a different right socket.", "warning")
            continue

        # record mapping
        mapping[left_idx] = right_idx
        animated_effect(f"Recorded mapping: Left {left_idx} → Right {right_idx}", "info")

    # Evaluate correctness
    correct = sum(1 for k, v in mapping.items() if correct_map.get(k) == v)
    animated_text(f"You made {correct} correct connections out of 3.", color=theme["text_color"])

    if correct == 3:
        animated_effect("Wiring fully restored.", "success")
        return 2  # perfect
    elif correct >= 1:
        animated_effect("Partial wiring established; some mismatches remain.", "info")
        return 1  # partial
    else:
        animated_effect("No correct connections made.", "warning")
        return 0  # fail


def _capacitor_phase(stats, inventory, theme, save_state, difficulty_bonus=0):
    """
    Phase 3: capacitor timing. Three quick QTEs. Use call_timed_challenge for portability.
    Returns number of successes (0..3).
    Inventory or stats may increase timeout or lower difficulty.
    """
    animated_text("\nPhase 3 — Capacitor timing: synchronize the discharge.", color=theme["text_color"])
    animated_text("You'll need to hit the right key quickly for three steps.", color=theme["text_color"])

    # base timeout; modify by items/stats
    base_timeout = 3.5
    if "insulated_wire" in inventory:
        base_timeout += 0.5
    if stats.get("Agility", 0) > 6:
        base_timeout += 0.5
    base_timeout += difficulty_bonus

    keys = [random.choice(list("rhtk")) for _ in range(3)]
    successes = 0
    for i, k in enumerate(keys, start=1):
        prompt = f"Capacitor {i}: press '{k}'!"
        ok = call_timed_challenge(prompt, k, timeout=max(1.0, base_timeout - i*0.6))
        if ok:
            animated_effect(f"Capacitor {i} synchronized.", "success")
            successes += 1
        else:
            animated_effect(f"Capacitor {i} missed!", "warning")
    return successes

def engine_repair_panel(stats, inventory, theme, save_state):
    """
    Main handler entry. Returns True on success (panel repaired), False otherwise.
    """
    animated_text("\nYou kneel before the engine's maintenance panel.", color=theme["text_color"])
    # count attempts
    attempts = save_state.setdefault("visited", {}).get("engine_attempts", 0)
    attempts += 1
    save_state["visited"]["engine_attempts"] = attempts

    # Quick check: items required for a chance at full success (but you can try without)
    required = {"brass_gear", "oil_can"}
    has_required = required.issubset(set(inventory))

    if not has_required:
        animated_effect("Warning: you lack some recommended parts (brass_gear, oil_can). Proceeding is riskier.", "warning")
        choice = spinner_input("Try improvising anyway? (y/n): ", theme).strip().lower()
        if choice != "y":
            animated_text("You step away from the panel for now.", color=theme["text_color"])
            return False

    # PHASE 1: Diagnostics (gives a bonus if correct)
    diag_bonus = 1 if _diagnostics_phase(stats, inventory, theme, save_state) else 0

    # PHASE 2: Wiring
    wiring_score = _wiring_phase(stats, inventory, theme, save_state)  # returns 0/1/2

    # PHASE 3: Capacitor timing; difficulty increases if wiring poor
    difficulty = 0 if wiring_score == 2 else 0.5
    cap_successes = _capacitor_phase(stats, inventory, theme, save_state, difficulty_bonus=difficulty)

    # Determine result
    total_score = diag_bonus + wiring_score + cap_successes  # higher is better
    animated_text(f"\nRepair assessment: diagnostic {diag_bonus} + wiring {wiring_score} + timing {cap_successes} = {total_score}", color=theme["text_color"])

    # Success thresholds:
    if total_score >= 4:
        # Full success
        animated_effect("The panel channels settle into a harmonious purr. Repair complete.", "success")
        if "repaired_panel" not in inventory:
            inventory.append("repaired_panel")
        # reward: silenced fragment with good chance
        if random.random() < 0.7:
            inventory.append("Silenced Core Fragment")
            animated_effect("You extract a Silenced Core Fragment and tuck it away.", "info")
        # record state
        save_state.setdefault("visited", {})["engine_panel_repaired_full"] = True
        return True
    elif total_score >= 2:
        # Partial success: panel stabilized but unstable
        animated_effect("The panel mostly holds; you patch the worst faults but it remains jittery.", "info")
        if "repaired_panel" not in inventory:
            inventory.append("repaired_panel")
        # penalty: small Health drain from sparks
        stats["Health"] = max(0, stats.get("Health", 0) - 1)
        save_state.setdefault("visited", {})["engine_panel_repaired_partial"] = True
        return True
    else:
        # Failure: sparks, damage, no repair
        animated_effect("A spark streaks across the panel. The repair attempt fails.", "warning")
        stats["Health"] = max(0, stats.get("Health", 0) - 3)
        # small chance to break an item
        if inventory and random.random() < 0.2:
            lost = random.choice(inventory)
            try:
                inventory.remove(lost)
                animated_effect(f"You drop and lose '{lost}' in the chaos.", "warning")
            except ValueError:
                pass
        return False

# Register handler on import
register_special_handler("engine_repair_panel", engine_repair_panel)
