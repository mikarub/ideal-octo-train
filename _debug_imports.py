print("IMPORT: entry")
import quests.hollowbridge_factory.entry

print("IMPORT: hall")
import quests.hollowbridge_factory.hall

print("IMPORT: stairs")
import quests.hollowbridge_factory.stairs

print("IMPORT: storage")
import quests.hollowbridge_factory.storage

print("IMPORT: catwalk")
import quests.hollowbridge_factory.catwalk

print("IMPORT: engine_room")
import quests.hollowbridge_factory.engine_room

print("IMPORT: workshop")
import quests.hollowbridge_factory.workshop

from scenes.runner import SCENE_REGISTRY
print("SCENES:", SCENE_REGISTRY.keys())
