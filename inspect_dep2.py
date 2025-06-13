import importlib, inspect
mod = importlib.reload(importlib.import_module('backend.dependencies'))
print(dir(mod))