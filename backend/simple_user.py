#!/usr/bin/env python3
"""
简化的用户创建脚本
避免复杂的模型导入问题
"""

import sys
import os
from datetime import datetime
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext

# 密码加密上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 数据库配置
DATABASE_URL = "sqlite:///./sql_app.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_password_hash(password: str) -> str:
    """生成密码哈希"""
    return pwd_context.hash(password)

def create_user_simple(username: str, email: str, password: str, role: str = "student", 
                      study_level: str = "beginner", full_name: str | None = None) -> bool:
    """使用原生SQL创建用户"""
    try:
        db = SessionLocal()
        
        # 检查用户是否已存在
        result = db.execute(text("SELECT id FROM users WHERE username = :username OR email = :email"), 
                           {"username": username, "email": email})
        existing_user = result.fetchone()
        
        if existing_user:
            print(f"❌ 用户名或邮箱已存在")
            return False
        
        # 生成密码哈希
        hashed_password = get_password_hash(password)
        
        # 插入新用户
        db.execute(text("""
            INSERT INTO users (username, email, password, hashed_password, role, study_level, 
                             full_name, is_active, is_verified, created_at, updated_at)
            VALUES (:username, :email, :password, :hashed_password, :role, :study_level,
                   :full_name, :is_active, :is_verified, :created_at, :updated_at)
        """), {
            "username": username,
            "email": email,
            "password": password,
            "hashed_password": hashed_password,
            "role": role,
            "study_level": study_level,
            "full_name": full_name,
            "is_active": True,
            "is_verified": True,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        })
        
        db.commit()
        
        print(f"✅ 用户创建成功！")
        print(f"📋 用户信息:")
        print(f"   - 用户名: {username}")
        print(f"   - 邮箱: {email}")
        print(f"   - 角色: {role}")
        print(f"   - 学习水平: {study_level}")
        
        return True
        
    except Exception as e:
        print(f"❌ 创建用户失败: {e}")
        db.rollback()
        return False
    finally:
        db.close()

def list_users_simple():
    """使用原生SQL列出用户"""
    try:
        db = SessionLocal()
        result = db.execute(text("""
            SELECT id, username, email, role, is_active, created_at 
            FROM users 
            ORDER BY id
        """))
        users = result.fetchall()
        
        print("📋 用户列表")
        print("=" * 80)
        print(f"{'ID':<5} {'用户名':<15} {'邮箱':<25} {'角色':<10} {'状态':<8} {'创建时间':<20}")
        print("-" * 80)
        
        for user in users:
            status = "✅ 活跃" if user.is_active else "❌ 禁用"
            # 安全处理时间格式
            try:
                if hasattr(user.created_at, 'strftime'):
                    created_time = user.created_at.strftime('%Y-%m-%d %H:%M')
                elif isinstance(user.created_at, str):
                    created_time = user.created_at[:16]  # 取前16个字符
                else:
                    created_time = str(user.created_at)[:16] if user.created_at else "未知"
            except:
                created_time = "未知"
            
            print(f"{user.id:<5} {user.username:<15} {user.email:<25} {user.role:<10} {status:<8} {created_time}")
        
        print(f"\n总计: {len(users)} 个用户")
        
    except Exception as e:
        print(f"❌ 获取用户列表失败: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

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
    
    # 创建用户
    return create_user_simple(
        username=username,
        email=email,
        password=password,
        role=role,
        study_level=study_level,
        full_name=full_name
    )

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  python simple_user.py create          # 交互式创建用户")
        print("  python simple_user.py list            # 列出所有用户")
        print("  python simple_user.py quick <username> <email> <password> [role]  # 快速创建用户")
        return
    
    command = sys.argv[1].lower()
    
    if command == "create":
        create_user_interactive()
    elif command == "list":
        list_users_simple()
    elif command == "quick":
        if len(sys.argv) < 5:
            print("❌ 快速创建用户需要提供: 用户名 邮箱 密码 [角色]")
            return
        username = sys.argv[2]
        email = sys.argv[3]
        password = sys.argv[4]
        role = sys.argv[5] if len(sys.argv) > 5 else "student"
        
        create_user_simple(username, email, password, role)
    else:
        print(f"❌ 未知命令: {command}")

if __name__ == "__main__":
    main() 