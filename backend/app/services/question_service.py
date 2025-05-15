from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.question import (Question, QuestionType, QuestionCategory,
                                 ExamPaper, ExamQuestion)


def create_question(db: Session,
                    question_type: QuestionType,
                    content: str,
                    answer: str,
                    options: Optional[List[str]] = None,
                    explanation: Optional[str] = None,
                    difficulty: int = 1,
                    category_id: Optional[int] = None) -> Question:
    db_question = Question(question_type=question_type,
                           content=content,
                           options=options,
                           answer=answer,
                           explanation=explanation,
                           difficulty=difficulty,
                           category_id=category_id,
                           created_at=datetime.utcnow(),
                           updated_at=datetime.utcnow())
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question


def get_question(db: Session, question_id: int) -> Optional[Question]:
    return db.query(Question).filter(Question.id == question_id).first()


def get_questions_by_category(db: Session,
                              category_id: int,
                              skip: int = 0,
                              limit: int = 100) -> List[Question]:
    return (db.query(Question).filter(
        Question.category_id == category_id).offset(skip).limit(limit).all())


def create_category(db: Session,
                    name: str,
                    parent_id: Optional[int] = None) -> QuestionCategory:
    db_category = QuestionCategory(name=name, parent_id=parent_id)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def create_exam_paper(db: Session,
                      title: str,
                      description: Optional[str] = None,
                      total_score: int = 100,
                      time_limit: Optional[int] = None) -> ExamPaper:
    db_exam = ExamPaper(title=title,
                        description=description,
                        total_score=total_score,
                        time_limit=time_limit,
                        created_at=datetime.utcnow(),
                        updated_at=datetime.utcnow())
    db.add(db_exam)
    db.commit()
    db.refresh(db_exam)
    return db_exam


def add_question_to_exam(db: Session,
                         exam_id: int,
                         question_id: int,
                         score: int = 10,
                         sequence: Optional[int] = None) -> ExamQuestion:
    db_exam_question = ExamQuestion(exam_id=exam_id,
                                    question_id=question_id,
                                    score=score,
                                    sequence=sequence)
    db.add(db_exam_question)
    db.commit()
    db.refresh(db_exam_question)
    return db_exam_question
