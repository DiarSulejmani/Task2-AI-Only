import inspect, textwrap, backend.database as db
print('\n'.join(textwrap.dedent(inspect.getsource(db)).splitlines()))