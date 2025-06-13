import subprocess, sys, json, os
result = subprocess.run([sys.executable, '-m', 'backend.scripts.init_db'], capture_output=True, text=True)
print('Return', result.returncode)
print(result.stdout)
print(result.stderr)