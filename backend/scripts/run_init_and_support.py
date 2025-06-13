import subprocess, sys, os

# Create support files
subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), "create_support_files.py")], check=True)
# Init db
subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), "init_db.py")], check=True)