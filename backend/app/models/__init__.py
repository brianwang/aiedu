# 导入所有模型以确保SQLAlchemy关系正确配置
from .user import User, StudySession, WrongQuestion
from .question import Question
from .exam import Exam, ExamResult
from .learning import (
    UserProfile, 
    LearningGoal, 
    LearningPlan, 
    LearningTask, 
    LearningReminder, 
    Achievement, 
    LearningProgress
)

__all__ = [
    "User",
    "StudySession", 
    "WrongQuestion",
    "Question",
    "Exam",
    "ExamResult",
    "UserProfile",
    "LearningGoal",
    "LearningPlan", 
    "LearningTask",
    "LearningReminder",
    "Achievement",
    "LearningProgress"
] 