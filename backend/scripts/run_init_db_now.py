import subprocess, sys, os, pathlib, traceback, json, sys

try:
    import importlib
    # Ensure backend is importable
    sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))
    from backend.database import DATABASE_URL
    print("DATABASE_URL:", DATABASE_URL)
    # run init
    subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), 'init_db.py')], check=True)
except Exception as e:
    print('Error:', e)
    traceback.print_exc()