"""API routers for teacher and student examples."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend import models, schemas
from backend.dependencies import get_db, require_role

teacher_router = APIRouter(prefix="/teacher", tags=["teacher"])
student_router = APIRouter(prefix="/student", tags=["student"])


# -------------------- Teacher routes --------------------
@teacher_router.get("/questions", response_model=list[schemas.QuestionOut])
def list_questions(
    db: Session = Depends(get_db),
    teacher: models.User = Depends(require_role("teacher")),
):
    return db.query(models.Question).filter(models.Question.teacher_id == teacher.id).all()


@teacher_router.post("/questions", response_model=schemas.QuestionOut, status_code=201)
def create_question(
    q_in: schemas.QuestionCreate,
    db: Session = Depends(get_db),
    teacher: models.User = Depends(require_role("teacher")),
):
    q = models.Question(
        teacher_id=teacher.id,
        topic=q_in.topic,
        question_type=q_in.question_type,
        content=q_in.content,
        status=q_in.status or "draft",
    )
    db.add(q)
    db.commit()
    db.refresh(q)
    return q

# -------------------- Student routes --------------------
@student_router.get("/progress", response_model=list[schemas.QuizAttemptOut])
def student_progress(
    db: Session = Depends(get_db),
    student: models.User = Depends(require_role("student")),
):
    return db.query(models.QuizAttempt).filter(models.QuizAttempt.student_id == student.id).all()