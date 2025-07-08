#!/usr/bin/env python3
"""
使用sqlite3直接操作数据库的用户创建脚本（哈希密码）
"""

import sqlite3
import sys
from datetime import datetime
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def create_user(username: str, email: str, password: str, role: str = "student", 
                study_level: str = "beginner", full_name: str | None = None) -> bool:
    """创建新用户（密码哈希存储）"""
    try:
        conn = sqlite3.connect('sql_app.db')
        cursor = conn.cursor()
        
        # 检查用户是否已存在
        cursor.execute("SELECT id FROM users WHERE username = ? OR email = ?", (username, email))
        existing_user = cursor.fetchone()
        
        if existing_user:
            print(f"❌ 用户名或邮箱已存在")
            return False
        
        # 生成密码哈希
        hashed = hash_password(password)
        
        # 插入新用户
        cursor.execute("""
            INSERT INTO users (username, email, password, hashed_password, role, study_level, 
                             full_name, is_active, is_verified, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            username, email, password, hashed, role, study_level,
            full_name, True, True, datetime.utcnow(), datetime.utcnow()
        ))
        
        conn.commit()
        
        print(f"✅ 用户创建成功！")
        print(f"📋 用户信息:")
        print(f"   - 用户名: {username}")
        print(f"   - 邮箱: {email}")
        print(f"   - 角色: {role}")
        print(f"   - 学习水平: {study_level}")
        
        return True
        
    except Exception as e:
        print(f"❌ 创建用户失败: {e}")
        return False
    finally:
        conn.close()

def list_users():
    """列出所有用户"""
    try:
        conn = sqlite3.connect('sql_app.db')
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, username, email, role, is_active, created_at 
            FROM users 
            ORDER BY id
        """)
        users = cursor.fetchall()
        
        print("📋 用户列表")
        print("=" * 80)
        print(f"{'ID':<5} {'用户名':<15} {'邮箱':<25} {'角色':<10} {'状态':<8} {'创建时间':<20}")
        print("-" * 80)
        
        for user in users:
            status = "✅ 活跃" if user[4] else "❌ 禁用"
            created_time = user[5] if user[5] else "未知"
            print(f"{user[0]:<5} {user[1]:<15} {user[2]:<25} {user[3]:<10} {status:<8} {created_time}")
        
        print(f"\n总计: {len(users)} 个用户")
        
    except Exception as e:
        print(f"❌ 获取用户列表失败: {e}")
    finally:
        conn.close()

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
    print("2. 教师 (teacher)")
    print("3. 管理员 (admin)")
    
    role_choice = input("请输入选择 (1-3): ").strip()
    role_map = {
        "1": "student",
        "2": "teacher", 
        "3": "admin"
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
    return create_user(
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
        print("  python add_user.py create          # 交互式创建用户")
        print("  python add_user.py list            # 列出所有用户")
        print("  python add_user.py quick <用户名> <邮箱> <密码> [角色]  # 快速创建用户")
        return
    
    command = sys.argv[1].lower()
    
    if command == "create":
        create_user_interactive()
    elif command == "list":
        list_users()
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