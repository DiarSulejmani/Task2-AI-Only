import importlib, sys
backend_main = importlib.import_module('backend.main')
print('status attr?', hasattr(backend_main, 'status'))
print('status:', getattr(backend_main, 'status', None))