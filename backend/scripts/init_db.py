"""backend/scripts/init_db.py

Initialises the SQLite database by creating all tables defined in
backend.models.  Usage::

    python -m backend.scripts.init_db
"""
from __future__ import annotations

import importlib
import sys

# Ensure package root is on sys.path when executing as module
if __name__ == "__main__" and ("backend" not in sys.modules):
    import pathlib

    ROOT = pathlib.Path(__file__).resolve().parent.parent
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT.parent))

from backend.database import Base, engine  # noqa: E402

# Import models so that they register with Base.metadata
importlib.import_module("backend.models")  # noqa: E402  # pragma: no cover

Base.metadata.create_all(bind=engine)

print("Database tables created successfully!")

status = "ok"