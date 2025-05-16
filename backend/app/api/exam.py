from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas.exam import ExamCreate, ExamResultCreate, Exam, ExamResult
from app.models.user import User
from app.services import exam_service
from database import get_db
from .auth import get_current_user

router = APIRouter(prefix="/api/exam")


@router.post("/", response_model=Exam)
def create_exam(exam: ExamCreate,
                db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    return exam_service.create_exam(db, exam)


@router.get("/{exam_id}", response_model=Exam)
def get_exam(exam_id: str, db: Session = Depends(get_db)):
    exam = exam_service.get_exam(db, exam_id)
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    return exam


@router.post("/results", response_model=ExamResult)
def submit_exam_result(result: ExamResultCreate,
                       db: Session = Depends(get_db),
                       current_user: User = Depends(get_current_user)):
    return exam_service.submit_exam_result(db, result)


@router.get("/results/{exam_id}", response_model=List[ExamResult])
def get_exam_results(exam_id: str,
                     skip: int = 0,
                     limit: int = 100,
                     db: Session = Depends(get_db)):
    return exam_service.get_exam_results(db, exam_id, skip, limit)
