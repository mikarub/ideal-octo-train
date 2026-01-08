# scenes/runner.py
SCENE_REGISTRY = {}
SPECIAL_HANDLERS = {}

def register_scene(name):
    """Decorator that registers a scene function by name."""
    def decorator(func):
        SCENE_REGISTRY[name] = func
        return func
    return decorator

def register_special_handler(name, func):
    """Register a special-use handler."""
    SPECIAL_HANDLERS[name] = func

def run_scene(scene_name, stats, inventory, theme, save_state):
    scene_func = SCENE_REGISTRY.get(scene_name)
    
    if not scene_func:
        raise RuntimeError(f"Scene not registered: {scene_name}")
        
    next_scene = scene_func(stats, inventory, theme, save_state)
        
    if next_scene is None:
        return None
        
    if not isinstance(next_scene, str):
        raise TypeError(f"Scene '{scene_name}' returned {type(next_scene)} instead of str")
            
    return next_scene
        

def run_handler(name, *args, **kwargs):
    """Run a special handler (used for puzzles, wiring, etc)."""
    func = SPECIAL_HANDLERS.get(name)
    if not func:
        raise ValueError(f"Handler '{name}' is not registered.")
    return func(*args, **kwargs)
    

