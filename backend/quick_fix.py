import sqlite3

def fix_database():
    try:
        conn = sqlite3.connect('sql_app.db')
        cursor = conn.cursor()
        
        print("🔧 修复数据库表结构...")
        
        # 添加缺失的字段
        columns_to_add = [
            "full_name VARCHAR(200)",
            "avatar VARCHAR(500)", 
            "phone VARCHAR(20)",
            "bio TEXT",
            "is_active BOOLEAN DEFAULT 1",
            "is_verified BOOLEAN DEFAULT 0",
            "is_superuser BOOLEAN DEFAULT 0",
            "role VARCHAR(50) DEFAULT 'student'",
            "created_at DATETIME",
            "updated_at DATETIME",
            "last_login DATETIME",
            "study_level VARCHAR(50) DEFAULT 'beginner'",
            "preferred_subjects VARCHAR(500)"
        ]
        
        for column_def in columns_to_add:
            try:
                column_name = column_def.split()[0]
                cursor.execute(f"ALTER TABLE users ADD COLUMN {column_def}")
                print(f"✅ 添加字段: {column_name}")
            except sqlite3.OperationalError as e:
                if "duplicate column name" in str(e):
                    print(f"⚠️  字段已存在: {column_name}")
                else:
                    print(f"❌ 添加字段失败: {e}")
        
        # 创建测试用户
        test_users = [
            ("testuser", "test@example.com", "test123", "student", "测试用户"),
            ("admin", "admin@example.com", "admin123", "admin", "管理员"),
            
        ]
        
        for username, email, password, role, full_name in test_users:
            try:
                cursor.execute("""
                    INSERT OR IGNORE INTO users (username, email, password, hashed_password, role, study_level, full_name, is_active, is_verified, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'))
                """, (username, email, password, "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/HS.iQeO", role, "beginner", full_name, 1, 1))
                print(f"✅ 创建用户: {username}")
            except Exception as e:
                print(f"❌ 创建用户失败 {username}: {e}")
        
        conn.commit()
        
        # 显示用户列表
        cursor.execute("SELECT id, username, email, role FROM users ORDER BY id")
        users = cursor.fetchall()
        
        print("\n📋 用户列表:")
        print("ID  用户名      邮箱                角色")
        print("-" * 50)
        for user in users:
            print(f"{user[0]:<4} {user[1]:<12} {user[2]:<20} {user[3]}")
        
        print(f"\n✅ 数据库修复完成！共 {len(users)} 个用户")
        
    except Exception as e:
        print(f"❌ 修复失败: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    fix_database() 