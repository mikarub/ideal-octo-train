# quests/hollowbridge_factory/__init__.py
# Import scenes so they register with scenes.runner on module import.
# Force-import all scene modules so their @register_scene decorators run

from .entry import enter_factory
from .hall import hall_scene
from .stairs import stairs_scene
from .workshop import workshop_scene
from .storage import storage_scene
from .catwalk import catwalk_scene
from .engine_room import engine_room_scene

__all__ = [
    "enter_factory",
    "hall_scene",
    "stairs_scene",
    "workshop_scene",
    "storage_scene",
    "catwalk_scene",
    "engine_room_scene",
]
