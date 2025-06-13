import inspect, textwrap
import backend.dependencies as d
print(dir(d))
print(inspect.getsource(d.require_role))