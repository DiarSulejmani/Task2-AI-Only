import importlib, json
m = importlib.import_module('backend.auth')
print(json.dumps([name for name in dir(m) if 'role' in name]))