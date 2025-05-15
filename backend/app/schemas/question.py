from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel


class QuestionType(str, Enum):
    SINGLE_CHOICE = "single_choice"
    MULTIPLE_CHOICE = "multiple_choice"
    FILL_BLANK = "fill_blank"
    SHORT_ANSWER = "short_answer"
    ESSAY = "essay"


class QuestionBase(BaseModel):
    question_type: QuestionType
    content: str
    answer: str
    explanation: Optional[str] = None
    difficulty: int = 1
    category_id: Optional[int] = None


class QuestionCreate(QuestionBase):
    options: Optional[List[str]] = None


class QuestionUpdate(BaseModel):
    content: Optional[str] = None
    answer: Optional[str] = None
    explanation: Optional[str] = None
    difficulty: Optional[int] = None
    category_id: Optional[int] = None
    options: Optional[List[str]] = None


class QuestionResponse(QuestionBase):
    id: int
    created_at: datetime
    updated_at: datetime
    options: Optional[List[str]] = None

    class Config:
        orm_mode = True


class QuestionCategoryBase(BaseModel):
    name: str
    parent_id: Optional[int] = None


class QuestionCategoryCreate(QuestionCategoryBase):
    pass


class QuestionCategoryResponse(QuestionCategoryBase):
    id: int

    class Config:
        orm_mode = True
