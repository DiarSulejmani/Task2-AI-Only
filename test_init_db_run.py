import subprocess, sys
result = subprocess.run([sys.executable, '-m', 'backend.scripts.init_db'], capture_output=True, text=True)
print('EXIT', result.returncode)
print('STDOUT')
print(result.stdout)
print('STDERR')
print(result.stderr)