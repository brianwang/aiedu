from datetime import datetime
from enum import Enum
from typing import List, Optional

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship

from database.database import Base

class QuestionType(str, Enum):
    SINGLE_CHOICE = "single_choice"
    MULTIPLE_CHOICE = "multiple_choice"
    FILL_BLANK = "fill_blank"
    SHORT_ANSWER = "short_answer"
    ESSAY = "essay"

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    question_type = Column(String(50), nullable=False)
    content = Column(Text, nullable=False)
    options = Column(JSON, nullable=True)  # For choice questions
    answer = Column(Text, nullable=False)
    explanation = Column(Text, nullable=True)
    difficulty = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    category_id = Column(Integer, ForeignKey("question_categories.id"))
    
    category = relationship("QuestionCategory", back_populates="questions")

class QuestionCategory(Base):
    __tablename__ = "question_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    parent_id = Column(Integer, ForeignKey("question_categories.id"), nullable=True)
    
    questions = relationship("Question", back_populates="category")
    children = relationship("QuestionCategory")

class ExamPaper(Base):
    __tablename__ = "exam_papers"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    total_score = Column(Integer, default=100)
    time_limit = Column(Integer)  # in minutes
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ExamQuestion(Base):
    __tablename__ = "exam_questions"

    id = Column(Integer, primary_key=True, index=True)
    exam_id = Column(Integer, ForeignKey("exam_papers.id"))
    question_id = Column(Integer, ForeignKey("questions.id"))
    score = Column(Integer, default=10)
    sequence = Column(Integer)
    
    exam = relationship("ExamPaper")
    question = relationship("Question")