import importlib
import sys

if 'backend.models' in sys.modules:
    del sys.modules['backend.models']
models = importlib.import_module('backend.models')
print('Imported models', models)
print('User relationships:', models.User.__mapper__.relationships)