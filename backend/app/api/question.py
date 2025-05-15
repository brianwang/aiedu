from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.database import get_db
from app.models.question import Question, QuestionType, QuestionCategory
from app.schemas.question import (QuestionCreate, QuestionUpdate,
                                  QuestionResponse, QuestionCategoryCreate,
                                  QuestionCategoryResponse)
from app.services.question_service import (create_question, get_question,
                                           get_questions_by_category,
                                           create_category)

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
