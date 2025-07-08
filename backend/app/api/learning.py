from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from app.models.learning import UserProfile, LearningGoal, LearningPlan, LearningTask, LearningReminder, Achievement, LearningProgress
from app.schemas.learning import (
    UserProfileCreate, UserProfileUpdate, UserProfile as UserProfileSchema,
    LearningGoalCreate, LearningGoalUpdate, LearningGoal as LearningGoalSchema,
    LearningPlanCreate, LearningPlanUpdate, LearningPlan as LearningPlanSchema,
    LearningTaskCreate, LearningTaskUpdate, LearningTask as LearningTaskSchema,
    LearningReminderCreate, LearningReminderUpdate, LearningReminder as LearningReminderSchema,
    AchievementCreate, Achievement as AchievementSchema,
    LearningProgressCreate, LearningProgressUpdate, LearningProgress as LearningProgressSchema,
    LearningPlanGenerationRequest, LearningPlanGenerationResponse, LearningStatistics
)
from app.services.learning_plan_service import LearningPlanService
from app.services.auth_service import get_current_user
from app.models.user import User
from datetime import datetime, timedelta
from sqlalchemy import func

router = APIRouter(prefix="/learning", tags=["学习计划"])


# 用户画像相关接口
@router.post("/profile", response_model=UserProfileSchema, summary="创建用户画像")
async def create_user_profile(
    profile: UserProfileCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """创建用户学习画像"""
    # 检查是否已存在画像
    existing_profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    if existing_profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户画像已存在，请使用更新接口"
        )
    
    db_profile = UserProfile(
        user_id=current_user.id,
        **profile.dict()
    )
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile


@router.get("/profile", response_model=UserProfileSchema, summary="获取用户画像")
async def get_user_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取用户学习画像"""
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户画像不存在"
        )
    return profile


@router.put("/profile", response_model=UserProfileSchema, summary="更新用户画像")
async def update_user_profile(
    profile: UserProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新用户学习画像"""
    db_profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    if not db_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户画像不存在"
        )
    
    for field, value in profile.dict(exclude_unset=True).items():
        setattr(db_profile, field, value)
    
    db.commit()
    db.refresh(db_profile)
    return db_profile


# 学习目标相关接口
@router.post("/goals", response_model=LearningGoalSchema, summary="创建学习目标")
async def create_learning_goal(
    goal: LearningGoalCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """创建学习目标"""
    db_goal = LearningGoal(
        user_id=current_user.id,
        **goal.dict()
    )
    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)
    return db_goal


@router.get("/goals", response_model=List[LearningGoalSchema], summary="获取学习目标列表")
async def get_learning_goals(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取用户的学习目标列表"""
    goals = db.query(LearningGoal).filter(LearningGoal.user_id == current_user.id).all()
    return goals


@router.get("/goals/{goal_id}", response_model=LearningGoalSchema, summary="获取学习目标详情")
async def get_learning_goal(
    goal_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取学习目标详情"""
    goal = db.query(LearningGoal).filter(
        LearningGoal.id == goal_id,
        LearningGoal.user_id == current_user.id
    ).first()
    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="学习目标不存在"
        )
    return goal


@router.put("/goals/{goal_id}", response_model=LearningGoalSchema, summary="更新学习目标")
async def update_learning_goal(
    goal_id: int,
    goal: LearningGoalUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新学习目标"""
    db_goal = db.query(LearningGoal).filter(
        LearningGoal.id == goal_id,
        LearningGoal.user_id == current_user.id
    ).first()
    if not db_goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="学习目标不存在"
        )
    
    for field, value in goal.dict(exclude_unset=True).items():
        setattr(db_goal, field, value)
    
    db.commit()
    db.refresh(db_goal)
    return db_goal


@router.delete("/goals/{goal_id}", summary="删除学习目标")
async def delete_learning_goal(
    goal_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """删除学习目标"""
    db_goal = db.query(LearningGoal).filter(
        LearningGoal.id == goal_id,
        LearningGoal.user_id == current_user.id
    ).first()
    if not db_goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="学习目标不存在"
        )
    
    db.delete(db_goal)
    db.commit()
    return {"message": "学习目标已删除"}


# AI学习计划生成接口
@router.post("/generate-plan", response_model=LearningPlanGenerationResponse, summary="生成AI学习计划")
async def generate_learning_plan(
    request: LearningPlanGenerationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """生成个性化AI学习计划"""
    # 验证用户ID
    if request.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只能为自己的用户ID生成学习计划"
        )
    
    # 验证用户画像和目标是否存在
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="请先创建用户画像"
        )
    
    goals = db.query(LearningGoal).filter(LearningGoal.user_id == current_user.id).all()
    if not goals:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="请先创建学习目标"
        )
    
    # 调用AI服务生成学习计划
    learning_service = LearningPlanService(db)
    result = await learning_service.generate_learning_plan(request)
    
    return result


# 学习计划相关接口
@router.post("/plans", response_model=LearningPlanSchema, summary="创建学习计划")
async def create_learning_plan(
    plan: LearningPlanCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """创建学习计划"""
    db_plan = LearningPlan(
        user_id=current_user.id,
        **plan.dict()
    )
    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)
    return db_plan


@router.get("/plans", response_model=List[LearningPlanSchema], summary="获取学习计划列表")
async def get_learning_plans(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取用户的学习计划列表"""
    plans = db.query(LearningPlan).filter(LearningPlan.user_id == current_user.id).all()
    return plans


@router.get("/plans/{plan_id}", response_model=LearningPlanSchema, summary="获取学习计划详情")
async def get_learning_plan(
    plan_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取学习计划详情"""
    plan = db.query(LearningPlan).filter(
        LearningPlan.id == plan_id,
        LearningPlan.user_id == current_user.id
    ).first()
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="学习计划不存在"
        )
    return plan


@router.put("/plans/{plan_id}", response_model=LearningPlanSchema, summary="更新学习计划")
async def update_learning_plan(
    plan_id: int,
    plan: LearningPlanUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新学习计划"""
    db_plan = db.query(LearningPlan).filter(
        LearningPlan.id == plan_id,
        LearningPlan.user_id == current_user.id
    ).first()
    if not db_plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="学习计划不存在"
        )
    
    for field, value in plan.dict(exclude_unset=True).items():
        setattr(db_plan, field, value)
    
    db.commit()
    db.refresh(db_plan)
    return db_plan


@router.delete("/plans/{plan_id}", summary="删除学习计划")
async def delete_learning_plan(
    plan_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """删除学习计划"""
    db_plan = db.query(LearningPlan).filter(
        LearningPlan.id == plan_id,
        LearningPlan.user_id == current_user.id
    ).first()
    if not db_plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="学习计划不存在"
        )
    
    db.delete(db_plan)
    db.commit()
    return {"message": "学习计划已删除"}


@router.get("/plans/{plan_id}/tasks", response_model=List[LearningTaskSchema], summary="获取计划任务列表")
async def get_plan_tasks(
    plan_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取学习计划的任务列表"""
    # 验证计划是否存在且属于当前用户
    plan = db.query(LearningPlan).filter(
        LearningPlan.id == plan_id,
        LearningPlan.user_id == current_user.id
    ).first()
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="学习计划不存在"
        )
    
    tasks = db.query(LearningTask).filter(LearningTask.plan_id == plan_id).all()
    return tasks


# 学习任务相关接口
@router.post("/tasks", response_model=LearningTaskSchema, summary="创建学习任务")
async def create_learning_task(
    task: LearningTaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """创建学习任务"""
    # 验证计划是否存在且属于当前用户
    plan = db.query(LearningPlan).filter(
        LearningPlan.id == task.plan_id,
        LearningPlan.user_id == current_user.id
    ).first()
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="学习计划不存在"
        )
    
    db_task = LearningTask(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@router.put("/tasks/{task_id}/status", response_model=LearningTaskSchema, summary="更新任务状态")
async def update_task_status(
    task_id: int,
    status_update: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新任务状态"""
    task = db.query(LearningTask).join(LearningPlan).filter(
        LearningTask.id == task_id,
        LearningPlan.user_id == current_user.id
    ).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="任务不存在"
        )
    
    new_status = status_update.get("status")
    if new_status not in ["pending", "in_progress", "completed", "overdue"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="无效的状态值"
        )
    
    task.status = new_status
    if new_status == "completed":
        task.completed_at = datetime.utcnow()
    
    db.commit()
    db.refresh(task)
    return task


# 学习进度相关接口
@router.post("/progress", response_model=LearningProgressSchema, summary="记录学习进度")
async def record_learning_progress(
    progress: LearningProgressCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """记录学习进度"""
    db_progress = LearningProgress(
        user_id=current_user.id,
        **progress.dict()
    )
    db.add(db_progress)
    db.commit()
    db.refresh(db_progress)
    return db_progress


# 学习统计接口
@router.get("/statistics", response_model=LearningStatistics, summary="获取学习统计")
async def get_learning_statistics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取用户学习统计信息"""
    # 计算总学习时间
    total_study_time = db.query(func.sum(LearningProgress.study_time)).filter(
        LearningProgress.user_id == current_user.id
    ).scalar() or 0
    
    # 计算完成率
    total_tasks = db.query(func.count(LearningTask.id)).join(LearningPlan).filter(
        LearningPlan.user_id == current_user.id
    ).scalar() or 0
    
    completed_tasks = db.query(func.count(LearningTask.id)).join(LearningPlan).filter(
        LearningPlan.user_id == current_user.id,
        LearningTask.status == "completed"
    ).scalar() or 0
    
    completion_rate = completed_tasks / total_tasks if total_tasks > 0 else 0.0
    
    # 计算连续学习天数（简化版本）
    current_streak = 7  # 这里可以添加更复杂的逻辑
    
    # 计算成就数量
    total_achievements = db.query(func.count(Achievement.id)).filter(
        Achievement.user_id == current_user.id
    ).scalar() or 0
    
    # 计算总点数
    total_points = db.query(func.sum(Achievement.points)).filter(
        Achievement.user_id == current_user.id
    ).scalar() or 0
    
    return LearningStatistics(
        total_study_time=total_study_time,
        completed_tasks=completed_tasks,
        total_tasks=total_tasks,
        completion_rate=completion_rate,
        current_streak=current_streak,
        total_achievements=total_achievements,
        total_points=total_points
    )


# 学习提醒相关接口
@router.post("/reminders", response_model=LearningReminderSchema, summary="创建学习提醒")
async def create_learning_reminder(
    reminder: LearningReminderCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """创建学习提醒"""
    db_reminder = LearningReminder(
        user_id=current_user.id,
        **reminder.dict()
    )
    db.add(db_reminder)
    db.commit()
    db.refresh(db_reminder)
    return db_reminder


@router.get("/reminders", response_model=List[LearningReminderSchema], summary="获取提醒列表")
async def get_learning_reminders(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取用户的学习提醒列表"""
    reminders = db.query(LearningReminder).filter(LearningReminder.user_id == current_user.id).all()
    return reminders


# 成就相关接口
@router.get("/achievements", response_model=List[AchievementSchema], summary="获取成就列表")
async def get_achievements(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取用户的成就列表"""
    achievements = db.query(Achievement).filter(Achievement.user_id == current_user.id).all()
    return achievements


@router.post("/achievements", response_model=AchievementSchema, summary="创建成就")
async def create_achievement(
    achievement: AchievementCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """创建成就记录"""
    db_achievement = Achievement(
        user_id=current_user.id,
        **achievement.dict()
    )
    db.add(db_achievement)
    db.commit()
    db.refresh(db_achievement)
    return db_achievement 