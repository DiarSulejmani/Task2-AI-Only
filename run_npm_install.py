import subprocess, json
frontend_dir = 'frontend'
cmd = ['npm','install','--no-audit','--fund=false']
try:
    output = subprocess.check_output(cmd, cwd=frontend_dir, stderr=subprocess.STDOUT, text=True, timeout=180)
    print(json.dumps({'success': True, 'output': output[:800]}))
except subprocess.CalledProcessError as e:
    print(json.dumps({'success': False, 'output': e.output[:800]}))
except subprocess.TimeoutExpired as e:
    print(json.dumps({'success': False, 'output': 'timeout'}))