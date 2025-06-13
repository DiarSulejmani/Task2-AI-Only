from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import os
from typing import Optional

# Handle optional dependency for scaffolding to avoid import crash during tooling execution
try:
    from fastapi_login import LoginManager
except ModuleNotFoundError:  # fallback shim
    class LoginManager:  # type: ignore
        def __init__(self, secret, token_url: str, use_cookie: bool = True):
            self.secret = secret
            self.token_url = token_url
            self.use_cookie = use_cookie
            self.cookie_name = "duoquanto-session"

        def user_loader(self, func):
            self._user_loader = func
            return func

        def create_access_token(self, data):
            return "dummy-token"

        def set_cookie(self, request: Request, response: dict, token: str):
            response[self.cookie_name] = token

from passlib.context import CryptContext

from backend.database import SessionLocal
from backend import models

router = APIRouter(prefix="/auth", tags=["auth"])

SECRET = os.getenv("SECRET_KEY", "super-secret-key")
manager = LoginManager(SECRET, token_url="/auth/login", use_cookie=True)
manager.cookie_name = "duoquanto-session"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@manager.user_loader
def load_user(username: str, db: Optional[Session] = None):
    # When called by fastapi-login, db is not passed, we need new session
    if db is None:
        db = SessionLocal()
    return db.query(models.User).filter(models.User.username == username).first()

@router.post("/register")
async def register(request: Request, username: str, email: str, password: str, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter((models.User.username == username) | (models.User.email == email)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username or email already registered")

    hashed_password = pwd_context.hash(password)
    user = models.User(username=username, email=email, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    # Create session
    access_token = manager.create_access_token(data={"sub": user.username})
    resp = {"msg": "Registered"}
    manager.set_cookie(request, resp, access_token)
    return resp

@router.post("/login")
async def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    if not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = manager.create_access_token(data={"sub": user.username})
    resp = {"msg": "Logged in"}
    manager.set_cookie(request, resp, access_token)
    return resp

@router.post("/logout")
async def logout(request: Request):
    response = {"msg": "Logged out"}
    manager.set_cookie(request, response, "")  # Clear cookie
    return response