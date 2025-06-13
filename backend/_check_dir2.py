import importlib
m = importlib.import_module('backend.auth')
print('require_role in dir?:', 'require_role' in dir(m))