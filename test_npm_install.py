import subprocess, os, json, sys, textwrap, shlex, platform

frontend_dir = 'frontend'
result = {}

def run(cmd):
    try:
        out = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, text=True, cwd=frontend_dir, timeout=60)
        return out
    except subprocess.CalledProcessError as e:
        return f'ERROR: {e.output}'
    except FileNotFoundError as e:
        return f'ERROR: {str(e)}'

# Check node version
result['node_version'] = run('node -v')
result['npm_version'] = run('npm -v')

print(json.dumps(result, indent=2))