import inspect
import quests.hollowbridge_factory as hf
print("Loaded from:", inspect.getsourcefile(hf))
import quests.hollowbridge_factory.entry as e
print("Entry source:", inspect.getsourcefile(e))
print("Has enter factory():", hasattr(hf, "enter_factory"))

