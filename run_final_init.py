import subprocess, sys
result = subprocess.run([sys.executable, '-m', 'backend.scripts.init_db'], capture_output=True, text=True)
print(result.stdout)
print(result.stderr)