"""Shared FastAPI dependency utilities."""
from typing import Generator, Optional

from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from backend.database import SessionLocal
from backend import models


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(request: Request, db: Session = Depends(get_db)) -> models.User:
    user_id: Optional[int] = request.session.get("user_id")
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        # session contains stale user id
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


def require_role(role: str):
    def role_checker(user: models.User = Depends(get_current_user)) -> models.User:
        if user.role != role:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
        return user

    return role_checker