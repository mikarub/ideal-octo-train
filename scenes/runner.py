# scenes/runner.py
SCENE_REGISTRY = {}
SPECIAL_HANDLERS = {}

def register_scene(name):
    """Register a standard scene by name."""
    def decorator(func):
        SCENE_REGISTRY[name] = func
        return func
    return decorator

def register_special_handler(name, func):
    """Register a special-use handler."""
    SPECIAL_HANDLERS[name] = func

def run_scene(name, *args, **kwargs):
    """Run any scene by name."""
    scene = SCENE_REGISTRY.get(name)
    if not scene:
        raise ValueError(f"Scene '{name}' is not registered.")
    return scene(*args, **kwargs)

def run_handler(name, *args, **kwargs):
    """Run a special handler (used for puzzles, wiring, etc)."""
    func = SPECIAL_HANDLERS.get(name)
    if not func:
        raise ValueError(f"Handler '{name}' is not registered.")
    return func(*args, **kwargs)
