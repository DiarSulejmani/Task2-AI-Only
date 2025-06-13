"""Utility script to write non-Python files required in the repository."""
import os

backend_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(backend_dir, os.pardir))

# Write requirements.txt
requirements_path = os.path.join(project_root, "requirements.txt")
with open(requirements_path, "w") as f:
    f.write("fastapi\nuvicorn\nSQLAlchemy\npython-dotenv\npydantic\n")

# Write .env.example
env_example_path = os.path.join(project_root, ".env.example")
with open(env_example_path, "w") as f:
    f.write("DATABASE_URL=sqlite:///./app.db\n")

print("Non-Python files written: requirements.txt, .env.example")