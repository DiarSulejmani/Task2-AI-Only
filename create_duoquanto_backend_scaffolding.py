import os, textwrap

# Create necessary directories
os.makedirs('backend/scripts', exist_ok=True)

# 1. requirements.txt
requirements_content = textwrap.dedent('''\
    fastapi
    uvicorn
    sqlalchemy
    passlib[bcrypt]
    python-multipart
    itsdangerous
''')
with open('backend/requirements.txt', 'w') as f:
    f.write(requirements_content.strip() + '\n')

# 2. database.py
database_py = textwrap.dedent('''\
    from sqlalchemy import create_engine
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import sessionmaker
    import pathlib

    # Ensure data directory exists
    data_dir = pathlib.Path(__file__).resolve().parent / ".." / "data"
    data_dir.mkdir(exist_ok=True)
    DATABASE_URL = f"sqlite:///{data_dir / 'duoquanto.db'}"

    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False}
    )

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
''')
with open('backend/database.py', 'w') as f:
    f.write(database_py)

# 3. models.py
models_py = textwrap.dedent('''\
    import datetime as _dt
    from sqlalchemy import Column, Integer, String, DateTime, Text, JSON, ForeignKey

    from .database import Base


    class User(Base):
        __tablename__ = 'users'

        id = Column(Integer, primary_key=True, index=True)
        full_name = Column(String, nullable=False)
        email = Column(String, unique=True, index=True, nullable=False)
        password_hash = Column(String, nullable=False)
        role = Column(String, nullable=False)  # 'teacher' or 'student'
        created_at = Column(DateTime, default=_dt.datetime.utcnow)


    class Question(Base):
        __tablename__ = 'questions'

        id = Column(Integer, primary_key=True, index=True)
        teacher_id = Column(Integer, ForeignKey('users.id'), nullable=False)
        topic = Column(String, nullable=False)
        question_type = Column(String, nullable=False)  # e.g., 'mcq'
        text = Column(Text, nullable=False)
        options = Column(JSON, nullable=True)
        correct_answer = Column(String, nullable=True)
        explanation = Column(Text, nullable=True)
        status = Column(String, default='draft')  # 'draft', 'published', etc.
        created_at = Column(DateTime, default=_dt.datetime.utcnow)
''')
with open('backend/models.py', 'w') as f:
    f.write(models_py)

# 4. auth.py
auth_py = textwrap.dedent('''\
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
''')
with open('backend/auth.py', 'w') as f:
    f.write(auth_py)

# 5. main.py
main_py = textwrap.dedent('''\
    import os
    from fastapi import FastAPI, Depends, HTTPException, status, Request, Response
    from fastapi.middleware.cors import CORSMiddleware
    from starlette.middleware.sessions import SessionMiddleware

    from .database import Base, engine
    from .models import User
    from .auth import get_db, hash_password, verify_password, create_session_cookie, get_current_user, require_role

    # Ensure tables exist when app starts
    Base.metadata.create_all(bind=engine)

    app = FastAPI(title="DuoQuanto API")

    # Middlewares
    origins = ["http://localhost:3000", "http://127.0.0.1:3000"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    SESSION_SECRET = os.getenv('DUOQUANTO_SESSION_KEY', 'dev-session-key')
    app.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET)


    # Routes
    @app.post('/register')
    def register(full_name: str, email: str, password: str, role: str, db=Depends(get_db)):
        if role not in {'teacher', 'student'}:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid role')
        existing = db.query(User).filter(User.email == email).first()
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Email already registered')
        user = User(
            full_name=full_name,
            email=email,
            password_hash=hash_password(password),
            role=role
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return {"id": user.id, "email": user.email, "role": user.role}


    @app.post('/login')
    def login(response: Response, email: str, password: str, db=Depends(get_db)):
        user = db.query(User).filter(User.email == email).first()
        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials')
        cookie_value = create_session_cookie(user.id)
        response.set_cookie('session', cookie_value, httponly=True, samesite='lax')
        return {"message": "Logged in successfully", "role": user.role}


    @app.get('/logout')
    def logout(response: Response):
        response.delete_cookie('session')
        return {"message": "Logged out"}


    # Teacher dashboard
    @app.get('/teacher/dashboard')
    def teacher_dashboard(current_user = Depends(require_role('teacher'))):
        # Dummy data
        return {
            "total_questions": 0,
            "pending_reviews": 0,
            "course_coverage": 0
        }


    # Student dashboard
    @app.get('/student/dashboard')
    def student_dashboard(current_user = Depends(require_role('student'))):
        return {
            "progress": 0,
            "completed_lessons": 0,
            "average_score": 0
        }
''')
with open('backend/main.py', 'w') as f:
    f.write(main_py)

# 6. scripts/init_db.py
init_db_py = textwrap.dedent('''\
    import pathlib
    from backend.database import Base, engine


    def init():
        # Ensure parent data directory exists (database.py handles path creation)
        Base.metadata.create_all(bind=engine)
        print("Database initialized at", engine.url)


    if __name__ == '__main__':
        init()
''')
with open('backend/scripts/init_db.py', 'w') as f:
    f.write(init_db_py)

# Create __init__.py files
open('backend/__init__.py', 'w').close()
open('backend/scripts/__init__.py', 'w').close()

result = 'scaffolding_created'