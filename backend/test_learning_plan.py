#!/usr/bin/env python3
"""
测试AI学习计划功能
"""

import sys
import os
from pathlib import Path

# 添加项目路径
sys.path.append(str(Path(__file__).parent))

from sqlalchemy.orm import Session
from database import get_db
from app.models.user import User
from app.models.learning import UserProfile, LearningGoal
from app.schemas.learning import (
    UserProfileCreate, LearningGoalCreate, LearningPlanGenerationRequest
)
from app.services.learning_plan_service import LearningPlanService
from app.services.auth_service import AuthService
import asyncio


def create_test_user_profile():
    """创建测试用户画像"""
    db = next(get_db())
    
    # 查找测试用户
    user = db.query(User).filter(User.username == "testuser").first()
    if not user:
        print("请先创建测试用户")
        return None
    
    # 检查是否已有画像
    existing_profile = db.query(UserProfile).filter(UserProfile.user_id == user.id).first()
    if existing_profile:
        print(f"用户 {user.username} 已有画像")
        return existing_profile
    
    # 创建用户画像
    profile_data = UserProfileCreate(
        age=25,
        learning_style="visual",
        difficulty_preference="progressive",
        daily_study_time=60,
        weekly_study_days=5,
        learning_environment="online"
    )
    
    profile = UserProfile(
        user_id=user.id,
        **profile_data.dict()
    )
    
    db.add(profile)
    db.commit()
    db.refresh(profile)
    
    print(f"为用户 {user.username} 创建画像成功")
    return profile


def create_test_learning_goals():
    """创建测试学习目标"""
    db = next(get_db())
    
    # 查找测试用户
    user = db.query(User).filter(User.username == "testuser").first()
    if not user:
        print("请先创建测试用户")
        return []
    
    # 检查是否已有目标
    existing_goals = db.query(LearningGoal).filter(LearningGoal.user_id == user.id).all()
    if existing_goals:
        print(f"用户 {user.username} 已有 {len(existing_goals)} 个学习目标")
        return existing_goals
    
    # 创建学习目标
    goals_data = [
        LearningGoalCreate(
            subject="Python编程",
            skill_area="Web开发",
            target_level="intermediate",
            target_timeframe=6,
            priority=1
        ),
        LearningGoalCreate(
            subject="数据结构与算法",
            skill_area="计算机科学",
            target_level="beginner",
            target_timeframe=3,
            priority=2
        )
    ]
    
    goals = []
    for goal_data in goals_data:
        goal = LearningGoal(
            user_id=user.id,
            **goal_data.dict()
        )
        db.add(goal)
        goals.append(goal)
    
    db.commit()
    
    # 刷新获取ID
    for goal in goals:
        db.refresh(goal)
    
    print(f"为用户 {user.username} 创建 {len(goals)} 个学习目标成功")
    return goals


async def test_generate_learning_plan():
    """测试生成学习计划"""
    db = next(get_db())
    
    # 查找测试用户
    user = db.query(User).filter(User.username == "testuser").first()
    if not user:
        print("请先创建测试用户")
        return
    
    # 获取用户画像
    profile = db.query(UserProfile).filter(UserProfile.user_id == user.id).first()
    if not profile:
        print("请先创建用户画像")
        return
    
    # 获取学习目标
    goals = db.query(LearningGoal).filter(LearningGoal.user_id == user.id).all()
    if not goals:
        print("请先创建学习目标")
        return
    
    # 创建学习计划生成请求
    request = LearningPlanGenerationRequest(
        user_id=user.id,
        goals=goals,
        profile=profile
    )
    
    # 生成学习计划
    learning_service = LearningPlanService(db)
    try:
        result = await learning_service.generate_learning_plan(request)
        
        print("\n=== AI学习计划生成成功 ===")
        print(f"短期计划: {result.short_term_plan.title}")
        print(f"中期计划: {result.medium_term_plan.title}")
        print(f"长期计划: {result.long_term_plan.title}")
        print(f"生成任务数: {len(result.tasks)}")
        print(f"预计完成时间: {result.estimated_completion_time} 天")
        print(f"AI置信度: {result.confidence_score:.2f}")
        
        print("\n=== 学习任务列表 ===")
        for i, task in enumerate(result.tasks, 1):
            print(f"{i}. {task.title} ({task.task_type}) - {task.estimated_time}分钟")
        
    except Exception as e:
        print(f"生成学习计划失败: {str(e)}")


def test_learning_statistics():
    """测试学习统计功能"""
    db = next(get_db())
    
    # 查找测试用户
    user = db.query(User).filter(User.username == "testuser").first()
    if not user:
        print("请先创建测试用户")
        return
    
    # 获取学习计划
    plans = db.query(LearningPlan).filter(LearningPlan.user_id == user.id).all()
    print(f"用户 {user.username} 有 {len(plans)} 个学习计划")
    
    for plan in plans:
        tasks = db.query(LearningTask).filter(LearningTask.plan_id == plan.id).all()
        completed_tasks = [t for t in tasks if t.status == "completed"]
        
        print(f"计划: {plan.title}")
        print(f"  总任务数: {len(tasks)}")
        print(f"  已完成: {len(completed_tasks)}")
        print(f"  完成率: {len(completed_tasks)/len(tasks)*100:.1f}%" if tasks else "  完成率: 0%")


def main():
    """主函数"""
    print("=== AI学习计划系统测试 ===")
    
    # 1. 创建用户画像
    print("\n1. 创建用户画像...")
    profile = create_test_user_profile()
    
    # 2. 创建学习目标
    print("\n2. 创建学习目标...")
    goals = create_test_learning_goals()
    
    # 3. 生成学习计划
    print("\n3. 生成AI学习计划...")
    asyncio.run(test_generate_learning_plan())
    
    # 4. 查看学习统计
    print("\n4. 查看学习统计...")
    test_learning_statistics()
    
    print("\n=== 测试完成 ===")


if __name__ == "__main__":
    main() 