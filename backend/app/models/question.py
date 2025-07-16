from datetime import datetime
from enum import Enum
from typing import List, Optional

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON, Boolean, Float
from sqlalchemy.orm import relationship

from database import Base


class QuestionType(str, Enum):
    SINGLE_CHOICE = "single_choice"
    MULTIPLE_CHOICE = "multiple_choice"
    FILL_BLANK = "fill_blank"
    SHORT_ANSWER = "short_answer"
    ESSAY = "essay"


class QuestionDifficulty(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class QuestionSource(str, Enum):
    MANUAL = "manual"  # 人工录入
    AI_GENERATED = "ai_generated"  # AI生成
    IMPORTED = "imported"  # 导入


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    question_type = Column(String(50), nullable=False)
    content = Column(Text, nullable=False)
    options = Column(JSON, nullable=True)  # For choice questions
    answer = Column(Text, nullable=False)
    explanation = Column(Text, nullable=True)
    difficulty = Column(String(20), default=QuestionDifficulty.MEDIUM)
    source = Column(String(20), default=QuestionSource.MANUAL)
    tags = Column(JSON, nullable=True)  # 知识点标签
    skill = Column(JSON, nullable=True)  # 技能点
    estimated_time = Column(Integer, default=2)  # 预估答题时间(分钟)
    success_rate = Column(Float, default=0.0)  # 正确率
    usage_count = Column(Integer, default=0)  # 使用次数
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    category_id = Column(Integer, ForeignKey("question_categories.id"))
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # 关系
    category = relationship("QuestionCategory", back_populates="questions")
    creator = relationship("User")
    exam_questions = relationship("ExamQuestion", back_populates="question")
    user_answers = relationship("UserAnswer", back_populates="question")


class QuestionCategory(Base):
    __tablename__ = "question_categories"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    parent_id = Column(Integer, ForeignKey("question_categories.id"), nullable=True)
    icon = Column(String(50), nullable=True)
    color = Column(String(20), nullable=True)
    question_count = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    questions = relationship("Question", back_populates="category")
    children = relationship("QuestionCategory")


class KnowledgePoint(Base):
    __tablename__ = "knowledge_points"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    category_id = Column(Integer, ForeignKey("question_categories.id"))
    parent_id = Column(Integer, ForeignKey("knowledge_points.id"), nullable=True)
    difficulty_level = Column(Integer, default=1)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    category = relationship("QuestionCategory")
    children = relationship("KnowledgePoint")


class UserAnswer(Base):
    __tablename__ = "user_answers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    question_id = Column(Integer, ForeignKey("questions.id"))
    answer = Column(Text, nullable=False)
    is_correct = Column(Boolean, nullable=False)
    time_spent = Column(Integer, default=0)  # 答题时间(秒)
    confidence_level = Column(Integer, default=0)  # 自信度 0-100
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")
    question = relationship("Question", back_populates="user_answers")


class PracticeSession(Base):
    __tablename__ = "practice_sessions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    session_type = Column(String(50), nullable=False)  # random, category, ai_recommended
    category_id = Column(Integer, ForeignKey("question_categories.id"), nullable=True)
    question_count = Column(Integer, default=10)
    correct_count = Column(Integer, default=0)
    total_time = Column(Integer, default=0)  # 总用时(秒)
    accuracy_rate = Column(Float, default=0.0)
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    is_completed = Column(Boolean, default=False)

    user = relationship("User")
    category = relationship("QuestionCategory")
    session_questions = relationship("PracticeSessionQuestion", back_populates="session")


class PracticeSessionQuestion(Base):
    __tablename__ = "practice_session_questions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    session_id = Column(Integer, ForeignKey("practice_sessions.id"))
    question_id = Column(Integer, ForeignKey("questions.id"))
    sequence = Column(Integer, nullable=False)
    user_answer = Column(Text, nullable=True)
    is_correct = Column(Boolean, nullable=True)
    time_spent = Column(Integer, default=0)
    answered_at = Column(DateTime, nullable=True)

    session = relationship("PracticeSession", back_populates="session_questions")
    question = relationship("Question")


class ExamPaper(Base):
    __tablename__ = "exam_papers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    total_score = Column(Integer, default=100)
    time_limit = Column(Integer)  # in minutes
    difficulty = Column(String(20), default=QuestionDifficulty.MEDIUM)
    category_id = Column(Integer, ForeignKey("question_categories.id"), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    category = relationship("QuestionCategory")
    exam_questions = relationship("ExamQuestion", back_populates="exam")


class ExamQuestion(Base):
    __tablename__ = "exam_questions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    exam_id = Column(Integer, ForeignKey("exam_papers.id"))
    question_id = Column(Integer, ForeignKey("questions.id"))
    score = Column(Integer, default=10)
    sequence = Column(Integer)

    exam = relationship("ExamPaper", back_populates="exam_questions")
    question = relationship("Question", back_populates="exam_questions")
