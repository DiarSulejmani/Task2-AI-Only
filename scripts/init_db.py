"""Utility to create database tables"""
import sys
from pathlib import Path

# Ensure backend package importable when running as script
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from backend.database import Base, engine  # noqa: E402
import backend.models  # noqa: F401, E402


def init_db():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Done.")


if __name__ == "__main__":
    init_db()