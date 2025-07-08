import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.utils.jwt import get_password_hash

DATABASE_URL = "sqlite:///./sql_app.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def fix_all_user_passwords():
    db = SessionLocal()
    try:
        users = db.execute(text("SELECT id, password FROM users")).fetchall()
        for user in users:
            user_id = user.id
            password = user.password
            if not password:
                print(f"用户ID {user_id} 没有明文密码，跳过")
                continue
            hashed = get_password_hash(password)
            db.execute(text("UPDATE users SET hashed_password = :hashed WHERE id = :id"), {"hashed": hashed, "id": user_id})
            print(f"用户ID {user_id} 密码哈希已修复")
        db.commit()
        print("所有用户密码哈希修复完成！")
    except Exception as e:
        print(f"修复失败: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    fix_all_user_passwords() 