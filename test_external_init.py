import subprocess, sys, json
result = subprocess.run([sys.executable, '-m', 'backend.scripts.init_db'], capture_output=True, text=True)
print('ret', result.returncode)
print(result.stdout)
print(result.stderr)