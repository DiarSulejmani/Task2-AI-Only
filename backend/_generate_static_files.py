"""Utility script that emits non-Python resource files required by the
assignment (requirements.txt, .env.example, README).  The script is executed
immediately by the `save_to_file_and_run` helper so the side-car files are
created on the file system even though the helper itself only supports *.py*
filenames.
"""
from __future__ import annotations

import pathlib

BASE_DIR = pathlib.Path(__file__).resolve().parent

# ---------------------------------------------------------------------------
# Content definitions
# ---------------------------------------------------------------------------
requirements_content = """fastapi\nuvicorn\nsqlalchemy\npydantic\npasslib[bcrypt]\npython-dotenv\naiofiles\n"""

env_example_content = """# .env.example – copy to .env and adjust values accordingly\nDATABASE_URL=sqlite:///../data/duoquanto.db\nSECRET_KEY=changeme-dev-secret\n"""

readme_content = """# DuoQuanto backend – local development\n\nQuickstart:\n\n```bash\n# install dependencies\npip install -r backend/requirements.txt\n\n# initialise database\npython -m backend.scripts.init_db\n\n# run dev server (reload)\nuvicorn backend.main:app --reload\n```\n\nFront-end dev server (e.g. React) is assumed to run on http://localhost:3000 –\nCORS is already configured for that origin.\n"""

# Mapping of file path (relative to backend/) to content string
files_to_write = {
    BASE_DIR / "requirements.txt": requirements_content,
    BASE_DIR / ".env.example": env_example_content,
    BASE_DIR / "README.md": readme_content,
}

for path, content in files_to_write.items():
    path.write_text(content, encoding="utf-8")

status = "static files generated"