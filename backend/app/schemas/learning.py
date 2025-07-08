from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime
from enum import Enum


class LearningStyle(str, Enum):
    VISUAL = "visual"
    AUDITORY = "auditory"
    KINESTHETIC = "kinesthetic"


class DifficultyPreference(str, Enum):
    PROGRESSIVE = "progressive"
    CHALLENGING = "challenging"
    COMFORTABLE = "comfortable"


class LearningEnvironment(str, Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    HYBRID = "hybrid"


class TargetLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class PlanType(str, Enum):
    SHORT_TERM = "short_term"
    MEDIUM_TERM = "medium_term"
    LONG_TERM = "long_term"


class TaskType(str, Enum):
    STUDY = "study"
    PRACTICE = "practice"
    REVIEW = "review"
    ASSESSMENT = "assessment"


class ReminderType(str, Enum):
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"


class AchievementType(str, Enum):
    DAILY_STREAK = "daily_streak"
    MILESTONE = "milestone"
    SKILL_MASTERY = "skill_mastery"


# 用户画像相关
class UserProfileBase(BaseModel):
    age: Optional[int] = Field(None, ge=1, le=120, description="用户年龄")
    learning_style: Optional[LearningStyle] = Field(None, description="学习风格")
    difficulty_preference: Optional[DifficultyPreference] = Field(None, description="难度偏好")
    daily_study_time: Optional[int] = Field(None, ge=0, le=1440, description="每日学习时间（分钟）")
    weekly_study_days: Optional[int] = Field(None, ge=0, le=7, description="每周学习天数")
    learning_environment: Optional[LearningEnvironment] = Field(None, description="学习环境偏好")


class UserProfileCreate(UserProfileBase):
    pass


class UserProfileUpdate(UserProfileBase):
    pass


class UserProfile(UserProfileBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# 学习目标相关
class LearningGoalBase(BaseModel):
    subject: str = Field(..., min_length=1, max_length=100, description="学习科目")
    skill_area: Optional[str] = Field(None, max_length=100, description="技能领域")
    target_level: Optional[TargetLevel] = Field(None, description="目标水平")
    target_timeframe: Optional[int] = Field(None, ge=1, le=60, description="目标时间框架（月）")
    priority: Optional[int] = Field(1, ge=1, le=5, description="优先级")


class LearningGoalCreate(LearningGoalBase):
    pass


class LearningGoalUpdate(LearningGoalBase):
    status: Optional[str] = Field(None, description="目标状态")


class LearningGoal(LearningGoalBase):
    id: int
    user_id: int
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True


# 学习计划相关
class LearningPlanBase(BaseModel):
    plan_type: PlanType = Field(..., description="计划类型")
    title: str = Field(..., min_length=1, max_length=200, description="计划标题")
    description: Optional[str] = Field(None, description="计划描述")
    start_date: Optional[date] = Field(None, description="开始日期")
    end_date: Optional[date] = Field(None, description="结束日期")


class LearningPlanCreate(LearningPlanBase):
    pass


class LearningPlanUpdate(LearningPlanBase):
    status: Optional[str] = Field(None, description="计划状态")


class LearningPlan(LearningPlanBase):
    id: int
    user_id: int
    status: str
    ai_generated: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# 学习任务相关
class LearningTaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="任务标题")
    description: Optional[str] = Field(None, description="任务描述")
    task_type: Optional[TaskType] = Field(None, description="任务类型")
    difficulty: Optional[int] = Field(1, ge=1, le=5, description="难度等级")
    estimated_time: Optional[int] = Field(None, ge=1, description="预计时间（分钟）")
    due_date: Optional[date] = Field(None, description="截止日期")


class LearningTaskCreate(LearningTaskBase):
    plan_id: int = Field(..., description="所属计划ID")


class LearningTaskUpdate(LearningTaskBase):
    status: Optional[str] = Field(None, description="任务状态")


class LearningTask(LearningTaskBase):
    id: int
    plan_id: int
    status: str
    completed_at: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True


# 学习提醒相关
class LearningReminderBase(BaseModel):
    reminder_time: datetime = Field(..., description="提醒时间")
    reminder_type: ReminderType = Field(ReminderType.PUSH, description="提醒类型")


class LearningReminderCreate(LearningReminderBase):
    task_id: Optional[int] = Field(None, description="关联任务ID")


class LearningReminderUpdate(LearningReminderBase):
    status: Optional[str] = Field(None, description="提醒状态")


class LearningReminder(LearningReminderBase):
    id: int
    user_id: int
    task_id: Optional[int]
    status: str
    sent_at: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True


# 成就相关
class AchievementBase(BaseModel):
    achievement_type: AchievementType = Field(..., description="成就类型")
    title: str = Field(..., min_length=1, max_length=100, description="成就标题")
    description: Optional[str] = Field(None, description="成就描述")
    points: Optional[int] = Field(0, ge=0, description="成就点数")


class AchievementCreate(AchievementBase):
    pass


class Achievement(AchievementBase):
    id: int
    user_id: int
    earned_at: datetime
    
    class Config:
        from_attributes = True


# 学习进度相关
class LearningProgressBase(BaseModel):
    study_time: Optional[int] = Field(0, ge=0, description="学习时间（分钟）")
    completion_rate: Optional[float] = Field(0.0, ge=0.0, le=1.0, description="完成率")
    notes: Optional[str] = Field(None, description="学习笔记")


class LearningProgressCreate(LearningProgressBase):
    task_id: Optional[int] = Field(None, description="关联任务ID")


class LearningProgressUpdate(LearningProgressBase):
    pass


class LearningProgress(LearningProgressBase):
    id: int
    user_id: int
    task_id: Optional[int]
    recorded_at: datetime
    
    class Config:
        from_attributes = True


# AI学习计划生成请求
class LearningPlanGenerationRequest(BaseModel):
    user_id: int = Field(..., description="用户ID")
    goals: List[LearningGoal] = Field(..., description="学习目标列表")
    profile: UserProfile = Field(..., description="用户画像")


# 学习计划生成响应
class LearningPlanGenerationResponse(BaseModel):
    short_term_plan: LearningPlan
    medium_term_plan: LearningPlan
    long_term_plan: LearningPlan
    tasks: List[LearningTask]
    estimated_completion_time: int = Field(..., description="预计完成时间（天）")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="AI置信度")


# 学习统计
class LearningStatistics(BaseModel):
    total_study_time: int = Field(..., description="总学习时间（分钟）")
    completed_tasks: int = Field(..., description="完成任务数")
    total_tasks: int = Field(..., description="总任务数")
    completion_rate: float = Field(..., ge=0.0, le=1.0, description="完成率")
    current_streak: int = Field(..., description="当前连续学习天数")
    total_achievements: int = Field(..., description="总成就数")
    total_points: int = Field(..., description="总点数") 