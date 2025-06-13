import importlib, sys
if 'backend.models' in sys.modules:
    del sys.modules['backend.models']
models = importlib.import_module('backend.models')
print('import success', models)