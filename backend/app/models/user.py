from datetime import datetime
from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)

    # 用户信息
    full_name = Column(String(200), nullable=True)
    avatar = Column(String(500), nullable=True)
    phone = Column(String(20), nullable=True)
    bio = Column(Text, nullable=True)

    # 用户状态
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)

    # 角色管理
    role = Column(String(50), default="student")  # student, teacher, admin

    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)

    # 学习相关
    # beginner, intermediate, advanced
    study_level = Column(String(50), default="beginner")
    preferred_subjects = Column(String(500), nullable=True)  # JSON格式存储偏好学科

    # 关系
    profile = relationship("UserProfile", back_populates="user", uselist=False)
    exams = relationship("Exam", back_populates="creator")
    exam_results = relationship("ExamResult", back_populates="student")
    study_sessions = relationship("StudySession", back_populates="user")
    wrong_questions = relationship("WrongQuestion", back_populates="user")


class StudySession(Base):
    __tablename__ = "study_sessions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    subject = Column(String(100), nullable=False)
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime, nullable=True)
    duration_minutes = Column(Integer, default=0)
    questions_answered = Column(Integer, default=0)
    correct_answers = Column(Integer, default=0)

    user = relationship("User", back_populates="study_sessions")


class WrongQuestion(Base):
    __tablename__ = "wrong_questions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    wrong_answer = Column(Text, nullable=True)
    wrong_count = Column(Integer, default=1)
    last_wrong_time = Column(DateTime, default=datetime.utcnow)
    is_reviewed = Column(Boolean, default=False)

    user = relationship("User", back_populates="wrong_questions")
    question = relationship("Question")
