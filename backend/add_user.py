#!/usr/bin/env python3
"""
用户管理脚本
用于添加用户到数据库
"""

import sys
import os
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.models.user import User
from app.services.auth_service import AuthService
from app.utils.jwt import get_password_hash
from database import get_db, engine
from app.models import user as user_models

def create_admin_user():
    """创建管理员用户"""
    db = next(get_db())
    
    # 检查是否已存在管理员用户
    existing_admin = db.query(User).filter(User.username == "admin").first()
    if existing_admin:
        print("管理员用户已存在！")
        return existing_admin
    
    # 创建管理员用户
    admin_user = User(
        username="admin",
        email="admin@aiedu.com",
        password="admin123",  # 明文密码
        hashed_password=get_password_hash("admin123"),  # 哈希密码
        full_name="系统管理员",
        role="admin",
        is_active=True,
        is_verified=True,
        is_superuser=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    
    db.add(admin_user)
    db.commit()
    db.refresh(admin_user)
    
    print(f"✅ 管理员用户创建成功！")
    print(f"   用户名: {admin_user.username}")
    print(f"   邮箱: {admin_user.email}")
    print(f"   角色: {admin_user.role}")
    print(f"   创建时间: {admin_user.created_at}")
    
    return admin_user

def create_test_users():
    """创建测试用户"""
    db = next(get_db())
    
    test_users = [

        {
            "username": "student1",
            "email": "student1@aiedu.com",
            "password": "student123",
            "full_name": "李同学",
            "role": "student"
        },
        {
            "username": "student2",
            "email": "student2@aiedu.com",
            "password": "student123",
            "full_name": "王同学",
            "role": "student"
        }
    ]
    
    created_users = []
    
    for user_data in test_users:
        # 检查用户是否已存在
        existing_user = db.query(User).filter(User.username == user_data["username"]).first()
        if existing_user:
            print(f"用户 {user_data['username']} 已存在，跳过...")
            continue
        
        # 创建用户
        user = User(
            username=user_data["username"],
            email=user_data["email"],
            password=user_data["password"],
            hashed_password=get_password_hash(user_data["password"]),
            full_name=user_data["full_name"],
            role=user_data["role"],
            is_active=True,
            is_verified=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        db.add(user)
        created_users.append(user)
    
    db.commit()
    
    print(f"✅ 成功创建 {len(created_users)} 个测试用户")
    for user in created_users:
        print(f"   - {user.username} ({user.full_name}) - {user.role}")

def list_users():
    """列出所有用户"""
    db = next(get_db())
    users = db.query(User).all()
    
    print(f"📋 数据库中共有 {len(users)} 个用户:")
    print("-" * 80)
    print(f"{'ID':<4} {'用户名':<15} {'邮箱':<25} {'角色':<10} {'状态':<8} {'创建时间':<20}")
    print("-" * 80)
    
    for user in users:
        status = "活跃" if getattr(user, 'is_active', False) else "禁用"
        created_time = getattr(user, 'created_at', None)
        time_str = created_time.strftime('%Y-%m-%d %H:%M') if created_time else "未知"
        print(f"{user.id:<4} {user.username:<15} {user.email:<25} {user.role:<10} {status:<8} {time_str}")

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  python add_user.py create_admin    # 创建管理员用户")
        print("  python add_user.py create_test     # 创建测试用户")
        print("  python add_user.py list            # 列出所有用户")
        return
    
    command = sys.argv[1]
    
    try:
        if command == "create_admin":
            create_admin_user()
        elif command == "create_test":
            create_test_users()
        elif command == "list":
            list_users()
        else:
            print(f"未知命令: {command}")
            print("可用命令: create_admin, create_test, list")
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 