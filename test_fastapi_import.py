try:
    import fastapi
    print('fastapi available', fastapi.__version__)
except ImportError as e:
    print('fastapi not available', e)