import importlib, inspect
mod = importlib.import_module('backend.dependencies')
print('attrs:', dir(mod))
if hasattr(mod, 'require_role'):
    print(inspect.getsource(mod.require_role))