import backend.dependencies as dep, inspect, textwrap
print(textwrap.dedent(inspect.getsource(dep)))