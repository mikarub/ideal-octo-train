#it still loads the old version, where and what do I update to make the game load the new version of hollowbridge_factory
import importlib, quests.hollowbridge_factory as hf
import inspect
print("module:", hf)
print("members:", dir(hf))
print("enter_factory:", getattr(hf, "enter_factory", None))
print("is callable:", callable(getattr(hf, "enter_factory", None)))
print("source file:", inspect.getsourcefile(hf))
	
