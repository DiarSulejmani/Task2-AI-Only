import inspect, importlib, textwrap
s = importlib.import_module('backend.schemas')
print([name for name in dir(s) if name.endswith('Response')])