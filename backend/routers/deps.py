from typing import Generator

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database import SessionLocal

# Dependency to get DB session

def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Example dependency for role checking

def teacher_required(current_user=Depends(lambda: None)):
    """Placeholder teacher role check. Replace with real auth later."""
    if not getattr(current_user, "is_teacher", False):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Teacher access required")
    return True
