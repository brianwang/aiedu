from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from app.schemas.question import ExamPaperCreate
from app.models.exam import ExamPaper
from app.models.question import Question, QuestionType, QuestionCategory, ExamQuestion
from app.schemas.question import (QuestionCreate, QuestionUpdate,
                                  QuestionResponse, QuestionCategoryCreate,
                                  QuestionCategoryResponse, ExamPaperCreate)
from app.services.question_service import (create_question, get_question,
                                           get_questions_by_category,
                                           create_category, create_exam_paper,
                                           add_question_to_exam)

router = APIRouter(prefix="/questions", tags=["questions"])


@router.post("/", response_model=QuestionResponse)
def create_new_question(question: QuestionCreate,
                        db: Session = Depends(get_db)):
    return create_question(db, **question.dict())


@router.get("/{question_id}", response_model=QuestionResponse)
def read_question(question_id: int, db: Session = Depends(get_db)):
    db_question = get_question(db, question_id=question_id)
    if not db_question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Question not found")
    return db_question


@router.get("/category/{category_id}", response_model=list[QuestionResponse])
def read_questions_by_category(category_id: int,
                               skip: int = 0,
                               limit: int = 100,
                               db: Session = Depends(get_db)):
    return get_questions_by_category(db,
                                     category_id=category_id,
                                     skip=skip,
                                     limit=limit)


@router.post("/categories/", response_model=QuestionCategoryResponse)
def create_new_category(category: QuestionCategoryCreate,
                        db: Session = Depends(get_db)):
    return create_category(db,
                           name=category.name,
                           parent_id=category.parent_id)


@router.put("/{question_id}", response_model=QuestionResponse)
def update_question(question_id: int,
                    question: QuestionUpdate,
                    db: Session = Depends(get_db)):
    db_question = get_question(db, question_id=question_id)
    if not db_question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Question not found")

    for var, value in question.dict(exclude_unset=True).items():
        setattr(db_question, var, value)

    db_question.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_question)
    return db_question


@router.delete("/{question_id}")
def delete_question(question_id: int, db: Session = Depends(get_db)):
    db_question = get_question(db, question_id=question_id)
    if not db_question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Question not found")

    db.delete(db_question)
    db.commit()
    return {"message": "Question deleted successfully"}


@router.post("/exams/", response_model=ExamPaperCreate)
def create_exam(exam: ExamPaperCreate, db: Session = Depends(get_db)):
    return create_exam_paper(db, **exam.dict())


@router.post("/exams/{exam_id}/questions")
def add_exam_question(exam_id: int,
                      question_id: int,
                      score: int = 10,
                      sequence: Optional[int] = None,
                      db: Session = Depends(get_db)):
    return add_question_to_exam(db,
                                exam_id=exam_id,
                                question_id=question_id,
                                score=score,
                                sequence=sequence)
