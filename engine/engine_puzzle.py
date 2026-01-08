# engine/engine_puzzle.py
from ui.animated_text import animated_text, animated_effect
from ui.spinner_input import spinner_input
from engine.utils import skill_check
import time
import random

# A compact wiring puzzle:
# - 4x5 grid of nodes with simple wires; the goal is to connect left 'power' to right 'core' via closed path.
# - player toggles nodes (open/closed) and then 'run' to test.
# - oil hint reveals one necessary closed node.

class WiringPuzzle:
    def __init__(self, width=5, height=4, seed=None):
        self.width = width
        self.height = height
        self.seed = seed or random.randint(0, 999999)
        random.seed(self.seed)
        # grid True = closed/connected, False = open/broken
        self.grid = [[random.choice([True, False, False]) for _ in range(width)] for _ in range(height)]
        # ensure endpoints mostly closed
        for r in range(height):
            self.grid[r][0] = True  # left column some connection
        for r in range(height):
            self.grid[r][-1] = random.choice([True, False, False])
        self.max_moves = 8
        self.moves = 0
        self.solution_hint = None  # uncovered by oil

    def display(self, theme):
        # ASCII representation: O = closed (●), . = open (·)
        lines = []
        header = "   " + " ".join(str(i+1) for i in range(self.width))
        lines.append(header)
        for r in range(self.height):
            row = f"{chr(ord('A')+r)}  " + " ".join("●" if self.grid[r][c] else "·" for c in range(self.width))
            lines.append(row)
        animated_text("\n".join(lines), color=theme["text_color"], speed=0)  # instant draw

    def toggle(self, pos):
        r, c = pos
        if 0 <= r < self.height and 0 <= c < self.width:
            self.grid[r][c] = not self.grid[r][c]
            self.moves += 1
            return True
        return False

    def run_test(self):
        # simple connectivity: see if any path exists from left edge to right edge
        visited = [[False]*self.width for _ in range(self.height)]
        stack = []
        for r in range(self.height):
            if self.grid[r][0]:
                stack.append((r,0))
                visited[r][0] = True
        while stack:
            r,c = stack.pop()
            if c == self.width-1 and self.grid[r][c]:
                return True
            for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)]:
                nr, nc = r+dr, c+dc
                if 0<=nr<self.height and 0<=nc<self.width and not visited[nr][nc] and self.grid[nr][nc]:
                    visited[nr][nc] = True
                    stack.append((nr,nc))
        return False

    def reveal_hint(self):
        # pick a closed cell on path or suggest coordinates to close
        # naive: reveal a random cell that if closed increases chance (prefer middle columns)
        c = random.randint(1, self.width-2)
        r = random.randint(0, self.height-1)
        return (r,c)

def run_engine_puzzle(stats, inventory, theme, save_state):
    """
    Interactive loop. Returns True on success, False otherwise.
    """
    animated_text("\nPhase 1 — Diagnostics: read the flickering panel.", color=theme["text_color"])
    # small skill check to pick up a useful diagnostic
    ok, roll, total = skill_check(stats, "Agility", 8)
    if ok:
        animated_effect(f"Diagnostic scan: baseline stable. (roll {roll} total {total})", "info")
    else:
        animated_effect(f"Diagnostic scan noisy. (roll {roll} total {total})", "warning")

    # create puzzle
    puzzle = WiringPuzzle(width=5, height=4)
    if save_state.get("visited", {}).get("engine_oiled_hint"):
        # provide one revealed coordinate as hint
        hint_cell = puzzle.reveal_hint()
        save_state["visited"]["engine_hint_cell"] = hint_cell
    else:
        hint_cell = None

    attempts = 3
    animated_text("Phase 2 — Repair: you may toggle nodes (e.g. A1) up to moves, then 'run' to test connection.", color=theme["text_color"])
    while attempts > 0:
        puzzle.display(theme)
        if hint_cell:
            r,c = hint_cell
            animated_effect(f"Hint: try closing {chr(ord('A')+r)}{c+1} (revealed by oil).", "info")
        animated_text(f"Moves used: {puzzle.moves}/{puzzle.max_moves} | Attempts left: {attempts}", color=theme["text_color"])

        cmd = spinner_input("Command [toggle <A1> | run | auto | hint | quit]: ", theme).strip().lower()
        if cmd.startswith("toggle ") or cmd.startswith("t "):
            token = cmd.split(None,1)[1].strip().upper()
            if len(token) >= 2 and token[0].isalpha() and token[1:].isdigit():
                r = ord(token[0]) - ord('A')
                c = int(token[1:]) - 1
                if puzzle.toggle((r,c)):
                    animated_effect(f"Toggled {token}.", "info")
                else:
                    animated_effect("Invalid coordinate.", "warning")
            else:
                animated_effect("Invalid format. Try A1.", "warning")
        elif cmd == "run":
            success = puzzle.run_test()
            if success:
                animated_effect("✔ Wiring test: Connection established. Repair successful!", "success")
                return True
            else:
                attempts -= 1
                animated_effect("✖ Wiring test: No connection. Adjust and try again.", "warning")
                # optional: small stat penalty for failure
                stats["Health"] = max(0, stats.get("Health", 0) - 0)
        elif cmd == "auto":
            # attempt automatic repair using skills + items
            skill_ok, roll, total = skill_check(stats, "Luck", 10)
            if "precision_screwdriver" in inventory and skill_ok:
                animated_effect("Using precision screwdriver and luck, you re-seat several contacts.", "info")
                # flip some random cells towards success
                for _ in range(3):
                    rr = random.randint(0, puzzle.height-1)
                    cc = random.randint(0, puzzle.width-1)
                    puzzle.grid[rr][cc] = True
                if puzzle.run_test():
                    animated_effect("Auto-repair succeeded.", "success")
                    return True
                else:
                    animated_effect("Auto-repair incomplete.", "warning")
                    attempts -= 1
            else:
                animated_effect("Auto-repair failed (need precision screwdriver + Luck).", "warning")
                attempts -= 1
        elif cmd == "hint":
            # show a friendly hint (consumes oil if not already used)
            if save_state.get("visited", {}).get("engine_oiled_hint"):
                animated_effect("Oil hint already applied — use the revealed coordinate.", "info")
            else:
                if "oil_can" in inventory:
                    inventory.remove("oil_can")
                    save_state.setdefault("visited", {})["engine_oiled_hint"] = True
                    hint_cell = puzzle.reveal_hint()
                    save_state["visited"]["engine_hint_cell"] = hint_cell
                    animated_effect("Oil reveals a faint contact: it suggests a coordinate.", "info")
                else:
                    animated_effect("You have no oil to use for cleaning.", "warning")
        elif cmd == "quit":
            animated_effect("You step away from the panel, hands greasy.", "info")
            return False
        else:
            animated_effect("Unknown command.", "warning")

    animated_effect("All attempts exhausted. The panel locks down.", "warning")
    return False

