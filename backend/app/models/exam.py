from sqlalchemy import Column, Integer, String, JSON, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from datetime import datetime
from .question import Question


class Exam(Base):
    __tablename__ = "exams"

    id = Column(String, primary_key=True, index=True)
    title = Column(String)
    created_by = Column(String, ForeignKey("users.id"))
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    duration = Column(Integer)  # in minutes

    creator = relationship("User", back_populates="exams")


class ExamResult(Base):
    __tablename__ = "exam_results"

    id = Column(String, primary_key=True, index=True)
    exam_id = Column(String, ForeignKey("exams.id"))
    student_id = Column(String, ForeignKey("users.id"))
    answers = Column(JSON)
    score = Column(Integer)
    total_score = Column(Integer)

    exam = relationship("Exam")
    student = relationship("User")


class ExamPaper(Base):
    __tablename__ = "exam_papers"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    total_score = Column(Integer, default=100)
    time_limit = Column(Integer)  # in minutes
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime,
                        default=datetime.utcnow,
                        onupdate=datetime.utcnow)
