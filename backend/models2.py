from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, JSON, Float
from sqlalchemy.orm import relationship
from backend.database import Base

# clear metadata to avoid duplicates
Base.metadata.clear()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False, default="student")
    created_at = Column(DateTime, default=datetime.utcnow)

    questions = relationship("Question", back_populates="teacher")
    attempts = relationship("QuizAttempt", back_populates="student")

class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, ForeignKey("users.id"))
    topic = Column(String, nullable=False)
    question_type = Column(String, nullable=False)
    content = Column(JSON, nullable=False)
    status = Column(String, default="draft")
    created_at = Column(DateTime, default=datetime.utcnow)

    teacher = relationship("User", back_populates="questions")
    answers = relationship("StudentAnswer", back_populates="question")

class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"))
    score = Column(Float)
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)

    student = relationship("User", back_populates="attempts")
    answers = relationship("StudentAnswer", back_populates="attempt")

class StudentAnswer(Base):
    __tablename__ = "student_answers"
    id = Column(Integer, primary_key=True, index=True)
    attempt_id = Column(Integer, ForeignKey("quiz_attempts.id"))
    question_id = Column(Integer, ForeignKey("questions.id"))
    is_correct = Column(Boolean)
    answer_text = Column(String)

    attempt = relationship("QuizAttempt", back_populates="answers")
    question = relationship("Question", back_populates="answers")

print("models2 defined")