import os

base_dir = os.path.dirname(__file__)

files_content = {
    "requirements.txt": "fastapi\nuvicorn\nsqlalchemy\npydantic\npython-dotenv\npasslib[bcrypt]\nstarlette\n",
    ".env.example": "SESSION_SECRET=changeme\nDATABASE_URL=sqlite:///./app.db\n",
    "README.md": "# Backend Scaffold\n\n## Setup\n\n1. Create and activate a virtual environment.\n2. Install dependencies:\n```bash\npip install -r requirements.txt\n```\n3. Copy `.env.example` to `.env` and adjust values as needed.\n4. Initialize the database:\n```bash\npython -m backend.scripts.init_db\n```\n5. Run the server:\n```bash\nuvicorn backend.main:app --reload\n```\n",
}

for name, content in files_content.items():
    path = os.path.join(base_dir, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
print("Misc files written: ", ", ".join(files_content.keys()))