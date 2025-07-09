#!/usr/bin/env python3
"""
初始化学习计划相关的数据库表
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from database import engine, Base
from app.models.learning import *
from app.models.user import User
from sqlalchemy import text
import sqlite3

def init_learning_tables():
    """初始化学习计划相关的数据库表"""
    print("🔧 正在初始化学习计划数据库表...")
    
    try:
        # 创建所有表
        Base.metadata.create_all(bind=engine)
        print("✅ 数据库表创建成功")
        
        # 检查表是否存在
        with engine.connect() as conn:
            # 检查学习计划表
            result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='learning_plans'"))
            if result.fetchone():
                print("✅ learning_plans 表存在")
            else:
                print("❌ learning_plans 表不存在")
            
            # 检查学习任务表
            result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='learning_tasks'"))
            if result.fetchone():
                print("✅ learning_tasks 表存在")
            else:
                print("❌ learning_tasks 表不存在")
            
            # 检查用户画像表
            result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='user_profiles'"))
            if result.fetchone():
                print("✅ user_profiles 表存在")
            else:
                print("❌ user_profiles 表不存在")
        
        # 创建测试数据
        create_test_data()
        
    except Exception as e:
        print(f"❌ 初始化失败: {e}")
        import traceback
        traceback.print_exc()

def create_test_data():
    """创建测试数据"""
    print("\n📝 正在创建测试数据...")
    
    try:
        from sqlalchemy.orm import sessionmaker
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # 检查是否有用户
        users = db.query(User).all()
        if not users:
            print("⚠️  没有找到用户，请先创建用户")
            return
        
        test_user = users[0]  # 使用第一个用户
        print(f"👤 使用用户: {test_user.username}")
        
        # 创建用户画像
        from app.models.learning import UserProfile
        existing_profile = db.query(UserProfile).filter(UserProfile.user_id == test_user.id).first()
        if not existing_profile:
            profile = UserProfile(
                user_id=test_user.id,
                age=25,
                learning_style="visual",
                difficulty_preference="progressive",
                daily_study_time=60,
                weekly_study_days=5,
                learning_environment="online"
            )
            db.add(profile)
            db.commit()
            print("✅ 创建用户画像")
        else:
            print("✅ 用户画像已存在")
        
        # 创建学习计划
        from app.models.learning import LearningPlan
        existing_plans = db.query(LearningPlan).filter(LearningPlan.user_id == test_user.id).all()
        if not existing_plans:
            from datetime import date, timedelta
            
            # 短期计划
            short_plan = LearningPlan(
                user_id=test_user.id,
                user_profile_id=existing_profile.id if existing_profile else None,
                plan_type="short_term",
                title="Vue.js 基础学习计划",
                description="通过系统学习掌握Vue.js的核心概念和实践技能",
                start_date=date.today(),
                end_date=date.today() + timedelta(days=30),
                status="active",
                ai_generated=True
            )
            db.add(short_plan)
            
            # 中期计划
            medium_plan = LearningPlan(
                user_id=test_user.id,
                user_profile_id=existing_profile.id if existing_profile else None,
                plan_type="medium_term",
                title="全栈开发进阶计划",
                description="深入学习前后端开发技术，提升全栈开发能力",
                start_date=date.today(),
                end_date=date.today() + timedelta(days=90),
                status="active",
                ai_generated=True
            )
            db.add(medium_plan)
            
            # 长期计划
            long_plan = LearningPlan(
                user_id=test_user.id,
                user_profile_id=existing_profile.id if existing_profile else None,
                plan_type="long_term",
                title="AI教育平台开发计划",
                description="长期项目：开发一个完整的AI智能教育平台",
                start_date=date.today(),
                end_date=date.today() + timedelta(days=365),
                status="active",
                ai_generated=True
            )
            db.add(long_plan)
            
            db.commit()
            print("✅ 创建学习计划")
            
            # 为短期计划创建任务
            from app.models.learning import LearningTask
            tasks = [
                LearningTask(
                    plan_id=short_plan.id,
                    title="学习Vue.js基础语法",
                    description="掌握Vue.js的基本语法和核心概念",
                    task_type="study",
                    difficulty=2,
                    estimated_time=60,
                    due_date=date.today() + timedelta(days=5),
                    status="pending"
                ),
                LearningTask(
                    plan_id=short_plan.id,
                    title="完成Vue.js组件练习",
                    description="通过实践项目巩固组件开发技能",
                    task_type="practice",
                    difficulty=3,
                    estimated_time=90,
                    due_date=date.today() + timedelta(days=10),
                    status="pending"
                ),
                LearningTask(
                    plan_id=short_plan.id,
                    title="Vue.js路由和状态管理",
                    description="学习Vue Router和Pinia的使用",
                    task_type="study",
                    difficulty=4,
                    estimated_time=120,
                    due_date=date.today() + timedelta(days=15),
                    status="pending"
                )
            ]
            
            for task in tasks:
                db.add(task)
            
            db.commit()
            print("✅ 创建学习任务")
        else:
            print("✅ 学习计划已存在")
        
        db.close()
        
    except Exception as e:
        print(f"❌ 创建测试数据失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    init_learning_tables() 