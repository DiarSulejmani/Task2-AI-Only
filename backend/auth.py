import os
from passlib.context import CryptContext
from itsdangerous import Signer, BadSignature
from fastapi import Depends, HTTPException, status, Request
from starlette.responses import Response

from .database import SessionLocal
from .models import User

SECRET_KEY = os.getenv('DUOQUANTO_SECRET_KEY', 'dev-secret-key')
SIGNER = Signer(SECRET_KEY)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)


def create_session_cookie(user_id: int) -> str:
    token = SIGNER.sign(str(user_id)).decode()
    return token


def get_current_user(request: Request, db=Depends(get_db)) -> User:
    token = request.cookies.get('session')
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Not authenticated')
    try:
        unsigned = SIGNER.unsign(token).decode()
        user_id = int(unsigned)
    except (BadSignature, ValueError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid session')
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')
    return user


def require_role(role: str):
    def role_dependency(current_user: User = Depends(get_current_user)):
        if current_user.role != role:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Insufficient privileges')
        return current_user
    return role_dependency
