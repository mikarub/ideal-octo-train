# engine/utils.py
import random

def skill_check(stats, skill_name, difficulty):
    """
    Simple skill check: uses stat value + roll vs difficulty.
    Returns (success:bool, roll:int, total:int)
    """
    stat = stats.get(skill_name, 0)
    roll = random.randint(1, 20)
    total = stat + roll
    return (total >= difficulty, roll, total)
