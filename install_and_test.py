import subprocess, sys, time, os, signal, textwrap, pathlib, tempfile

# Write requirements.txt
requirements = textwrap.dedent("""
fastapi==0.110.0
uvicorn==0.29.0
SQLAlchemy==2.0.29
pydantic==2.6.3
passlib[bcrypt]==1.7.4
python-multipart==0.0.9
jinja2==3.1.3
aiofiles==23.2.1
""")
path = pathlib.Path('backend/requirements.txt')
path.write_text(requirements)
print('requirements.txt written')

# Install packages
print('Installing packages...')
subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', str(path)])
print('Packages installed')

# Start uvicorn server
print('Starting server for test...')
proc = subprocess.Popen([sys.executable, '-m', 'uvicorn', 'backend.main:app', '--port', '8001'])
try:
    time.sleep(5)
    if proc.poll() is None:
        print('Server started successfully (running).')
    else:
        raise RuntimeError('Server exited early')
finally:
    proc.terminate()
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        proc.kill()
print('Server terminated')