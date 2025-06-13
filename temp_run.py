import subprocess, sys, json, os
result = subprocess.run([sys.executable, '-m', 'backend.scripts.init_db'], capture_output=True, text=True)
print(json.dumps({'stdout': result.stdout, 'stderr': result.stderr}))