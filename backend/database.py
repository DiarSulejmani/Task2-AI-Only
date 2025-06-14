import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

try:
    from dotenv import load_dotenv
except ModuleNotFoundError:  # pragma: no cover – optional dependency
    def load_dotenv() -> None:
        """Fallback no-op when python-dotenv isn't installed."""
        return None

# Load environment variables from `.env` if present
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./duoquanto.db")

# For SQLite, allow usage across threads
engine_args: dict = {}
if DATABASE_URL.startswith("sqlite"):
    engine_args["connect_args"] = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, **engine_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
