import subprocess, json, os
try:
    output = subprocess.check_output(['npm','run','build','--silent'], cwd='frontend', stderr=subprocess.STDOUT, text=True, timeout=120)
    print(json.dumps({'success': True, 'output': output[-1000:]}))
except subprocess.CalledProcessError as e:
    print(json.dumps({'success': False, 'output': e.output[-1000:]}))
except subprocess.TimeoutExpired:
    print(json.dumps({'success': False, 'output': 'timeout'}))