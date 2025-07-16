from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from app.models.learning import UserProfile, LearningGoal, LearningPlan, LearningTask, LearningReminder, Achievement, LearningProgress, SkillPoint
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
@router.get("/tasks", response_model=List[LearningTaskSchema], summary="获取学习任务列表")
async def get_learning_tasks(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取用户的学习任务列表"""
    # 通过LearningPlan的user_id来查询任务
    tasks = db.query(LearningTask).join(LearningPlan).filter(LearningPlan.user_id == current_user.id).all()
    return tasks


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
    # 查找任务并确保属于当前用户
    task = db.query(LearningTask).join(LearningPlan).filter(
        LearningTask.id == task_id,
        LearningPlan.user_id == getattr(current_user, 'id', None)
    ).first()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"任务ID {task_id} 不存在或不属于当前用户"
        )
    
    # 验证状态值
    new_status = status_update.get("status")
    valid_statuses = ["pending", "in_progress", "completed", "overdue"]
    
    if not new_status:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="缺少status字段"
        )
    
    if new_status not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"无效的状态值: {new_status}。有效值: {', '.join(valid_statuses)}"
        )
    
    # 更新任务状态
    old_status = getattr(task, 'status', None)
    task.status = new_status
    
    # 如果状态变为completed，设置完成时间
    if new_status == "completed" and old_status != "completed":
        setattr(task, 'completed_at', datetime.utcnow())
    
    # 如果状态变为in_progress，设置开始时间
    if new_status == "in_progress" and old_status == "pending":
        setattr(task, 'started_at', datetime.utcnow())
    
    # 更新其他可选字段
    if "started_at" in status_update:
        setattr(task, 'started_at', status_update["started_at"])
    if "completed_at" in status_update:
        setattr(task, 'completed_at', status_update["completed_at"])
    
    try:
        db.commit()
        db.refresh(task)
        return task
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新任务状态失败: {str(e)}"
        )


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


@router.post("/test-task", response_model=LearningTaskSchema, summary="创建测试任务")
async def create_test_task(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """创建测试任务用于测试"""
    user_id = getattr(current_user, 'id', None)
    
    # 直接使用SQL插入，避免模型字段问题
    from sqlalchemy import text
    
    # 插入学习计划
    plan_result = db.execute(text("""
        INSERT INTO learning_plans (user_id, plan_type, title, description, start_date, end_date, status, ai_generated, created_at)
        VALUES (:user_id, :plan_type, :title, :description, :start_date, :end_date, :status, :ai_generated, :created_at)
        RETURNING id
    """), {
        "user_id": user_id,
        "plan_type": "short_term",
        "title": "测试计划",
        "description": "用于测试的计划",
        "start_date": datetime.now().date(),
        "end_date": datetime.now().date() + timedelta(days=7),
        "status": "active",
        "ai_generated": False,
        "created_at": datetime.utcnow()
    })
    
    plan_row = plan_result.fetchone()
    if not plan_row:
        raise HTTPException(status_code=500, detail="创建计划失败")
    
    plan_id = plan_row[0]
    
    # 插入测试任务
    task_result = db.execute(text("""
        INSERT INTO learning_tasks (plan_id, title, description, task_type, difficulty, estimated_time, due_date, status, created_at)
        VALUES (:plan_id, :title, :description, :task_type, :difficulty, :estimated_time, :due_date, :status, :created_at)
        RETURNING id, plan_id, title, description, task_type, difficulty, estimated_time, due_date, status, created_at
    """), {
        "plan_id": plan_id,
        "title": "测试任务",
        "description": "这是一个测试任务",
        "task_type": "study",
        "difficulty": 1,
        "estimated_time": 30,
        "due_date": datetime.now().date(),
        "status": "pending",
        "created_at": datetime.utcnow()
    })
    
    task_data = task_result.fetchone()
    if not task_data:
        raise HTTPException(status_code=500, detail="创建任务失败")
    
    db.commit()
    
    # 构造返回对象
    task = LearningTask(
        id=task_data[0],
        plan_id=task_data[1],
        title=task_data[2],
        description=task_data[3],
        task_type=task_data[4],
        difficulty=task_data[5],
        estimated_time=task_data[6],
        due_date=task_data[7],
        status=task_data[8],
        created_at=task_data[9]
    )
    
    return task 


@router.post("/learning-path", summary="获取个性化学习路径")
async def get_learning_path(
    target_skill: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取个性化学习路径推荐"""
    try:
        from app.services.ai_service import AIService
        ai_service = AIService()
        
        learning_path = await ai_service.recommend_learning_path(
            db=db,
            user_id=getattr(current_user, 'id', None),
            target_skill=target_skill
        )
        
        return {
            "success": True,
            "data": learning_path
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取学习路径失败: {str(e)}"
        )


@router.get("/learning-report", summary="生成学习报告")
async def generate_learning_report(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """生成个性化学习报告"""
    try:
        from app.services.ai_service import AIService
        ai_service = AIService()
        
        report = await ai_service.generate_learning_report(
            user_id=getattr(current_user, 'id', None),
            db=db
        )
        
        return {
            "success": True,
            "data": report
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"生成学习报告失败: {str(e)}"
        )


@router.get("/learning-style", summary="分析学习风格")
async def analyze_learning_style(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """分析用户学习风格"""
    try:
        from app.services.ai_service import AIService
        ai_service = AIService()
        
        learning_style = await ai_service.identify_learning_style(
            user_id=getattr(current_user, 'id', None),
            db=db
        )
        
        return {
            "success": True,
            "data": learning_style
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"分析学习风格失败: {str(e)}"
        )


@router.get("/motivation-plan", summary="获取学习激励方案")
async def get_motivation_plan(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取个性化学习激励方案"""
    try:
        from app.services.ai_service import AIService
        ai_service = AIService()
        
        motivation = await ai_service.generate_learning_motivation(
            user_id=getattr(current_user, 'id', None),
            db=db
        )
        
        return {
            "success": True,
            "data": motivation
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取激励方案失败: {str(e)}"
        ) 

skill_router = APIRouter(prefix="/skills", tags=["技能点"])

@skill_router.get("/", summary="获取所有技能点")
def get_skills(db: Session = Depends(get_db)):
    skills = db.query(SkillPoint).all()
    return [s.name for s in skills]

@skill_router.post("/", summary="新增技能点")
def add_skill(name: str, db: Session = Depends(get_db)):
    skill = SkillPoint(name=name)
    db.add(skill)
    db.commit()
    return {"success": True, "id": skill.id} 