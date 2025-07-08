#!/usr/bin/env python3
"""
创建测试用户
"""
import bcrypt
from database import SessionLocal
from app.models.user import User

def create_test_user():
    """创建测试用户"""
    db = SessionLocal()
    
    try:
        # 检查用户是否已存在
        existing_user = db.query(User).filter(User.username == "testuser2").first()
        if existing_user:
            print("用户 testuser2 已存在")
            return
        
        # 创建新用户
        hashed_password = bcrypt.hashpw("password123".encode('utf-8'), bcrypt.gensalt())
        
        new_user = User(
            username="testuser2",
            email="testuser2@example.com",
            hashed_password=hashed_password.decode('utf-8'),
            full_name="测试用户2",
            role="student",
            is_active=True,
            study_level="beginner"
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        print("✅ 测试用户创建成功:")
        print(f"   用户名: testuser2")
        print(f"   密码: password123")
        print(f"   邮箱: testuser2@example.com")
        
    except Exception as e:
        print(f"❌ 创建用户失败: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_test_user() 