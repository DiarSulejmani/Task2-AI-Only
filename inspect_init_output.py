import subprocess, sys, json
result = subprocess.run([sys.executable, '-m', 'backend.scripts.init_db'], capture_output=True, text=True)
print(result.stdout or 'no stdout')
print(result.stderr or 'no stderr')