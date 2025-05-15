from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import schemas
from ..services import exam_service
from ..database import get_db
from ..utils.auth import get_current_user

router = APIRouter(prefix="/api/exam")


@router.post("/", response_model=schemas.Exam)
def create_exam(exam: schemas.ExamCreate,
                db: Session = Depends(get_db),
                current_user: schemas.User = Depends(get_current_user)):
    return exam_service.create_exam(db, exam)


@router.get("/{exam_id}", response_model=schemas.Exam)
def get_exam(exam_id: str, db: Session = Depends(get_db)):
    exam = exam_service.get_exam(db, exam_id)
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    return exam


@router.post("/results", response_model=schemas.ExamResult)
def submit_exam_result(result: schemas.ExamResultCreate,
                       db: Session = Depends(get_db),
                       current_user: schemas.User = Depends(get_current_user)):
    return exam_service.submit_exam_result(db, result)


@router.get("/results/{exam_id}", response_model=List[schemas.ExamResult])
def get_exam_results(exam_id: str,
                     skip: int = 0,
                     limit: int = 100,
                     db: Session = Depends(get_db)):
    return exam_service.get_exam_results(db, exam_id, skip, limit)
