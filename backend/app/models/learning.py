from sqlalchemy import Column, Integer, String, Text, DateTime, Date, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class UserProfile(Base):
    __tablename__ = "user_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    age = Column(Integer)
    learning_style = Column(String(50))  # visual, auditory, kinesthetic
    difficulty_preference = Column(String(50))  # progressive, challenging, comfortable
    daily_study_time = Column(Integer)  # 分钟
    weekly_study_days = Column(Integer)
    learning_environment = Column(String(50))  # online, offline, hybrid
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # 关系
    user = relationship("User", back_populates="profile")
    learning_goals = relationship("LearningGoal", back_populates="user_profile")
    learning_plans = relationship("LearningPlan", back_populates="user_profile")


class LearningGoal(Base):
    __tablename__ = "learning_goals"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user_profile_id = Column(Integer, ForeignKey("user_profiles.id"), nullable=True)
    subject = Column(String(100), nullable=False)
    skill_area = Column(String(100))
    target_level = Column(String(50))  # beginner, intermediate, advanced, expert
    target_timeframe = Column(Integer)  # 月
    priority = Column(Integer, default=1)
    status = Column(String(20), default="active")  # active, completed, paused
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 关系
    user_profile = relationship("UserProfile", back_populates="learning_goals")


class LearningPlan(Base):
    __tablename__ = "learning_plans"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user_profile_id = Column(Integer, ForeignKey("user_profiles.id"), nullable=True)
    plan_type = Column(String(20), nullable=False)  # short_term, medium_term, long_term
    title = Column(String(200), nullable=False)
    description = Column(Text)
    start_date = Column(Date)
    end_date = Column(Date)
    status = Column(String(20), default="active")  # active, completed, paused
    ai_generated = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 关系
    user_profile = relationship("UserProfile", back_populates="learning_plans")
    learning_tasks = relationship("LearningTask", back_populates="learning_plan")


class LearningTask(Base):
    __tablename__ = "learning_tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    plan_id = Column(Integer, ForeignKey("learning_plans.id"), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    task_type = Column(String(50))  # study, practice, review, assessment
    difficulty = Column(Integer, default=1)  # 1-5
    estimated_time = Column(Integer)  # 分钟
    due_date = Column(Date)
    status = Column(String(20), default="pending")  # pending, in_progress, completed, overdue
    completed_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 关系
    learning_plan = relationship("LearningPlan", back_populates="learning_tasks")
    learning_reminders = relationship("LearningReminder", back_populates="learning_task")
    learning_progress = relationship("LearningProgress", back_populates="learning_task")


class LearningReminder(Base):
    __tablename__ = "learning_reminders"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    task_id = Column(Integer, ForeignKey("learning_tasks.id"))
    reminder_time = Column(DateTime(timezone=True), nullable=False)
    reminder_type = Column(String(20), default="push")  # email, sms, push
    status = Column(String(20), default="pending")  # pending, sent, completed
    sent_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 关系
    learning_task = relationship("LearningTask", back_populates="learning_reminders")


class Achievement(Base):
    __tablename__ = "achievements"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    achievement_type = Column(String(50), nullable=False)  # daily_streak, milestone, skill_mastery
    title = Column(String(100), nullable=False)
    description = Column(Text)
    points = Column(Integer, default=0)
    earned_at = Column(DateTime(timezone=True), server_default=func.now())


class LearningProgress(Base):
    __tablename__ = "learning_progress"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    task_id = Column(Integer, ForeignKey("learning_tasks.id"))
    study_time = Column(Integer, default=0)  # 实际学习时间（分钟）
    completion_rate = Column(Float, default=0.0)  # 完成率 0-1
    notes = Column(Text)
    recorded_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 关系
    learning_task = relationship("LearningTask", back_populates="learning_progress") 