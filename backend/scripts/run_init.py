import subprocess, sys
result = subprocess.run([sys.executable, "backend/scripts/init_db.py"], capture_output=True, text=True)
print(result.stdout)
print(result.stderr)