"""Utility script to dump non-Python static files required for repo.
This is only necessary because the execution environment for the coding
agent only permits saving *.py files. Running this script will generate
`requirements.txt` and `.env.example` files in project root.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

requirements_content = """fastapi\nuvicorn[standard]\nSQLAlchemy\npython-dotenv\npasslib[bcrypt]\nfastapi-login\n"""

env_content = """# Environment configuration for DuoQuanto backend\nSECRET_KEY=change-me\nDATABASE_URL=sqlite:///./duoquanto.db\n"""

def write_file(path: Path, content: str):
    path.write_text(content)
    print(f"Wrote {path}")

def main():
    write_file(ROOT / "requirements.txt", requirements_content)
    write_file(ROOT / ".env.example", env_content)

if __name__ == "__main__":
    main()