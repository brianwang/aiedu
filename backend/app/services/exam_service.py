from sqlalchemy.orm import Session
from ..models import Exam, ExamResult
from ..schemas import ExamCreate, ExamResultCreate


def create_exam(db: Session, exam: ExamCreate):
    db_exam = Exam(**exam.dict())
    db.add(db_exam)
    db.commit()
    db.refresh(db_exam)
    return db_exam


def get_exam(db: Session, exam_id: str):
    return db.query(Exam).filter(Exam.id == exam_id).first()


def submit_exam_result(db: Session, result: ExamResultCreate):
    db_result = ExamResult(**result.dict())
    db.add(db_result)
    db.commit()
    db.refresh(db_result)
    return db_result


def get_exam_results(db: Session,
                     exam_id: str,
                     skip: int = 0,
                     limit: int = 100):
    return db.query(ExamResult)\
        .filter(ExamResult.exam_id == exam_id)\
        .offset(skip)\
        .limit(limit)\
        .all()
