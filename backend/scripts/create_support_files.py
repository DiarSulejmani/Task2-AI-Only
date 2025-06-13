"""Script to create non-Python support files under backend directory."""
import os

backend_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.abspath(os.path.join(backend_dir, os.pardir))  # parent -> backend

requirements_path = os.path.join(backend_dir, "requirements.txt")
env_example_path = os.path.join(backend_dir, ".env.example")

with open(requirements_path, "w", encoding="utf-8") as req_f:
    req_f.write("fastapi\nuvicorn\nSQLAlchemy\npython-dotenv\npydantic\n")

with open(env_example_path, "w", encoding="utf-8") as env_f:
    env_f.write("DATABASE_URL=sqlite:///./app.db\n")

print("Support files created: requirements.txt, .env.example")