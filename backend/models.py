from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from backend.database import Base  # absolute import within package

# Ensure metadata is clean when script re-runs in the same interpreter during development
Base.metadata.clear()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_teacher = Column(Boolean, default=False)

    quiz_attempts = relationship("QuizAttempt", back_populates="user", cascade="all, delete-orphan")
    answers = relationship("StudentAnswer", back_populates="user", cascade="all, delete-orphan")
    badges = relationship("Badge", back_populates="user", cascade="all, delete-orphan")
    topic_progress = relationship("TopicProgress", back_populates="user", cascade="all, delete-orphan")

class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, index=True)
    prompt = Column(Text, nullable=False)
    correct_answer = Column(String, nullable=False)
    topic = Column(String, index=True)

    answers = relationship("StudentAnswer", back_populates="question", cascade="all, delete-orphan")

class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    score = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="quiz_attempts")
    answers = relationship("StudentAnswer", back_populates="quiz_attempt", cascade="all, delete-orphan")

class StudentAnswer(Base):
    __tablename__ = "student_answers"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    question_id = Column(Integer, ForeignKey("questions.id"))
    quiz_attempt_id = Column(Integer, ForeignKey("quiz_attempts.id"))
    answer_text = Column(String)
    is_correct = Column(Boolean)

    user = relationship("User", back_populates="answers")
    question = relationship("Question", back_populates="answers")
    quiz_attempt = relationship("QuizAttempt", back_populates="answers")

class Badge(Base):
    __tablename__ = "badges"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="badges")

class TopicProgress(Base):
    __tablename__ = "topic_progress"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    topic = Column(String, index=True)
    progress = Column(Integer, default=0)  # percentage 0-100

    user = relationship("User", back_populates="topic_progress")