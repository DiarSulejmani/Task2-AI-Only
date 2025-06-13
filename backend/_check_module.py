import importlib, inspect, textwrap
m = importlib.reload(importlib.import_module('backend.auth'))
print('import success, module id', id(m))
print('attributes: ', [name for name in dir(m) if 'role' in name])
print('source snippet:', textwrap.dedent(inspect.getsource(m.require_role)))