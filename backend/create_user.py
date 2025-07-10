#!/usr/bin/env python3
"""
用户管理脚本
用于创建和管理用户账户
"""

import sys
import os
from datetime import datetime
from sqlalchemy.orm import Session
from database import engine, get_db, Base
from app.models.user import User
from app.services.auth_service import AuthService
from app.utils.jwt import get_password_hash

# 确保所有模型都被导入
from app.models.exam import Exam, ExamResult
from app.models.question import Question

def create_user_interactive():
    """交互式创建用户"""
    print("🚀 AI智能教育平台 - 用户创建工具")
    print("=" * 50)
    
    # 获取用户输入
    username = input("请输入用户名: ").strip()
    if not username:
        print("❌ 用户名不能为空")
        return False
    
    email = input("请输入邮箱: ").strip()
    if not email:
        print("❌ 邮箱不能为空")
        return False
    
    password = input("请输入密码: ").strip()
    if not password:
        print("❌ 密码不能为空")
        return False
    
    confirm_password = input("请确认密码: ").strip()
    if password != confirm_password:
        print("❌ 两次输入的密码不一致")
        return False
    
    # 选择角色
    print("\n请选择用户角色:")
    print("1. 学生 (student)")
    print("2. 管理员 (admin)")
    
    role_choice = input("请输入选择 (1-2): ").strip()
    role_map = {
        "1": "student",
        "2": "admin"
    }
    role = role_map.get(role_choice, "student")
    
    # 选择学习水平（仅学生）
    study_level = "beginner"
    if role == "student":
        print("\n请选择学习水平:")
        print("1. 初学者 (beginner)")
        print("2. 中级 (intermediate)")
        print("3. 高级 (advanced)")
        
        level_choice = input("请输入选择 (1-3): ").strip()
        level_map = {
            "1": "beginner",
            "2": "intermediate",
            "3": "advanced"
        }
        study_level = level_map.get(level_choice, "beginner")
    
    # 获取其他信息
    full_name = input("请输入姓名 (可选): ").strip() or None
    phone = input("请输入电话 (可选): ").strip() or None
    bio = input("请输入个人简介 (可选): ").strip() or None
    
    # 创建用户
    return create_user(
        username=username,
        email=email,
        password=password,
        role=role,
        study_level=study_level,
        full_name=full_name,
        phone=phone,
        bio=bio
    )

def create_user(username: str, email: str, password: str, role: str = "student", 
                study_level: str = "beginner", full_name: str | None = None, 
                phone: str | None = None, bio: str | None = None) -> bool:
    """创建新用户"""
    try:
        # 获取数据库会话
        db = next(get_db())
        
        # 检查用户是否已存在
        existing_user = db.query(User).filter(
            (User.username == username) | (User.email == email)
        ).first()
        
        if existing_user:
            if existing_user.username == username:
                print(f"❌ 用户名 '{username}' 已存在")
            else:
                print(f"❌ 邮箱 '{email}' 已被使用")
            return False
        
        # 创建用户
        hashed_password = get_password_hash(password)
        user = User(
            username=username,
            email=email,
            password=hashed_password,  # 明文密码（用于兼容）
            hashed_password=hashed_password,
            role=role,
            study_level=study_level,
            full_name=full_name,
            phone=phone,
            bio=bio,
            is_active=True,
            is_verified=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        print(f"✅ 用户创建成功！")
        print(f"📋 用户信息:")
        print(f"   - 用户名: {user.username}")
        print(f"   - 邮箱: {user.email}")
        print(f"   - 角色: {user.role}")
        print(f"   - 学习水平: {user.study_level}")
        print(f"   - 用户ID: {user.id}")
        print(f"   - 创建时间: {user.created_at}")
        
        return True
        
    except Exception as e:
        print(f"❌ 创建用户失败: {e}")
        return False
    finally:
        db.close()

def list_users():
    """列出所有用户"""
    try:
        db = next(get_db())
        users = db.query(User).all()
        
        print("📋 用户列表")
        print("=" * 80)
        print(f"{'ID':<5} {'用户名':<15} {'邮箱':<25} {'角色':<10} {'状态':<8} {'创建时间':<20}")
        print("-" * 80)
        
        for user in users:
            status = "✅ 活跃" if user.is_active == True else "❌ 禁用"
            print(f"{user.id:<5} {user.username:<15} {user.email:<25} {user.role:<10} {status:<8} {user.created_at.strftime('%Y-%m-%d %H:%M')}")
        
        print(f"\n总计: {len(users)} 个用户")
        
    except Exception as e:
        print(f"❌ 获取用户列表失败: {e}")
    finally:
        db.close()

def delete_user(user_id: int):
    """删除用户"""
    try:
        db = next(get_db())
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            print(f"❌ 用户ID {user_id} 不存在")
            return False
        
        confirm = input(f"确定要删除用户 '{user.username}' 吗？(y/N): ").strip().lower()
        if confirm != 'y':
            print("❌ 操作已取消")
            return False
        
        db.delete(user)
        db.commit()
        print(f"✅ 用户 '{user.username}' 已删除")
        return True
        
    except Exception as e:
        print(f"❌ 删除用户失败: {e}")
        return False
    finally:
        db.close()

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  python create_user.py create          # 交互式创建用户")
        print("  python create_user.py list            # 列出所有用户")
        print("  python create_user.py delete <id>     # 删除指定用户")
        print("  python create_user.py quick <username> <email> <password> [role]  # 快速创建用户")
        return
    
    command = sys.argv[1].lower()
    
    if command == "create":
        create_user_interactive()
    elif command == "list":
        list_users()
    elif command == "delete":
        if len(sys.argv) < 3:
            print("❌ 请提供用户ID")
            return
        try:
            user_id = int(sys.argv[2])
            delete_user(user_id)
        except ValueError:
            print("❌ 用户ID必须是数字")
    elif command == "quick":
        if len(sys.argv) < 5:
            print("❌ 快速创建用户需要提供: 用户名 邮箱 密码 [角色]")
            return
        username = sys.argv[2]
        email = sys.argv[3]
        password = sys.argv[4]
        role = sys.argv[5] if len(sys.argv) > 5 else "student"
        
        create_user(username, email, password, role)
    else:
        print(f"❌ 未知命令: {command}")

if __name__ == "__main__":
    main() 