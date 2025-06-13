import importlib
backend_main = importlib.import_module('backend.main')
print('imported backend.main status:', backend_main.status)