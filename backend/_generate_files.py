"""Utility script to generate non-Python resource files when executed via save_to_file_and_run."""
from pathlib import Path

backend_dir = Path(__file__).resolve().parent

# requirements.txt content
requirements_content = """fastapi
uvicorn[standard]
sqlalchemy
alembic
bcrypt
python-multipart
python-dotenv
"""
(backend_dir / "requirements.txt").write_text(requirements_content)

# .env.example content
env_example_content = "SECRET_KEY=changeme"
(backend_dir / ".env.example").write_text(env_example_content)

success_message = "Generated requirements.txt and .env.example"