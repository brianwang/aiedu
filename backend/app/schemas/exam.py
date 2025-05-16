from typing import List, Optional, Dict, Any
from pydantic import BaseModel


class QuestionBase(BaseModel):
    id: str
    type: str
    content: str
    answer: str
    score: int
    options: Optional[List[Dict[str, Any]]] = None


class ExamCreate(BaseModel):
    title: str
    questions: List[QuestionBase]
    created_by: str


class ExamResultCreate(BaseModel):
    exam_id: str
    student_id: str
    answers: List[Optional[str]]
    score: int
    total_score: int


class Exam(ExamCreate):
    id: str

    class Config:
        from_attributes = True


class ExamResult(ExamResultCreate):
    id: str

    class Config:
        from_attributes = True
