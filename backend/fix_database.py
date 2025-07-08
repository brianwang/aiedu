#!/usr/bin/env python3
"""
数据库表结构检查和修复脚本
"""

import sqlite3
import sys
from datetime import datetime

def check_table_structure():
    """检查users表结构"""
    try:
        conn = sqlite3.connect('sql_app.db')
        cursor = conn.cursor()
        
        # 获取表结构
        cursor.execute("PRAGMA table_info(users)")
        columns = cursor.fetchall()
        
        print("📋 当前users表结构:")
        print("=" * 80)
        print(f"{'序号':<4} {'字段名':<20} {'类型':<15} {'可空':<6} {'默认值':<10} {'主键':<6}")
        print("-" * 80)
        
        for col in columns:
            print(f"{col[0]:<4} {col[1]:<20} {col[2]:<15} {col[3]:<6} {str(col[4]):<10} {col[5]:<6}")
        
        # 检查缺失的字段
        expected_columns = {
            'id': 'INTEGER PRIMARY KEY',
            'email': 'VARCHAR(255)',
            'username': 'VARCHAR(100)',
            'password': 'VARCHAR(255)',
            'hashed_password': 'VARCHAR(255)',
            'full_name': 'VARCHAR(200)',
            'avatar': 'VARCHAR(500)',
            'phone': 'VARCHAR(20)',
            'bio': 'TEXT',
            'is_active': 'BOOLEAN',
            'is_verified': 'BOOLEAN',
            'is_superuser': 'BOOLEAN',
            'role': 'VARCHAR(50)',
            'created_at': 'DATETIME',
            'updated_at': 'DATETIME',
            'last_login': 'DATETIME',
            'study_level': 'VARCHAR(50)',
            'preferred_subjects': 'VARCHAR(500)'
        }
        
        existing_columns = {col[1] for col in columns}
        missing_columns = set(expected_columns.keys()) - existing_columns
        
        if missing_columns:
            print(f"\n❌ 缺失的字段: {', '.join(missing_columns)}")
            return missing_columns
        else:
            print(f"\n✅ 表结构完整")
            return []
            
    except Exception as e:
        print(f"❌ 检查表结构失败: {e}")
        return []
    finally:
        conn.close()

def add_missing_columns(missing_columns):
    """添加缺失的字段"""
    try:
        conn = sqlite3.connect('sql_app.db')
        cursor = conn.cursor()
        
        # 字段定义
        column_definitions = {
            'full_name': 'VARCHAR(200)',
            'avatar': 'VARCHAR(500)',
            'phone': 'VARCHAR(20)',
            'bio': 'TEXT',
            'is_active': 'BOOLEAN DEFAULT 1',
            'is_verified': 'BOOLEAN DEFAULT 0',
            'is_superuser': 'BOOLEAN DEFAULT 0',
            'role': 'VARCHAR(50) DEFAULT "student"',
            'created_at': 'DATETIME',
            'updated_at': 'DATETIME',
            'last_login': 'DATETIME',
            'study_level': 'VARCHAR(50) DEFAULT "beginner"',
            'preferred_subjects': 'VARCHAR(500)'
        }
        
        for column in missing_columns:
            if column in column_definitions:
                try:
                    sql = f"ALTER TABLE users ADD COLUMN {column} {column_definitions[column]}"
                    cursor.execute(sql)
                    print(f"✅ 添加字段: {column}")
                except sqlite3.OperationalError as e:
                    if "duplicate column name" in str(e):
                        print(f"⚠️  字段已存在: {column}")
                    else:
                        print(f"❌ 添加字段失败 {column}: {e}")
        
        conn.commit()
        print("✅ 数据库表结构修复完成")
        
    except Exception as e:
        print(f"❌ 修复表结构失败: {e}")
        conn.rollback()
    finally:
        conn.close()

def create_test_user():
    """创建测试用户"""
    try:
        conn = sqlite3.connect('sql_app.db')
        cursor = conn.cursor()
        
        # 检查是否已存在测试用户
        cursor.execute("SELECT id FROM users WHERE username = ?", ("testuser",))
        existing_user = cursor.fetchone()
        
        if existing_user:
            print("⚠️  测试用户已存在")
            return
        
        # 创建测试用户
        import bcrypt
        password = "test123"
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        cursor.execute("""
            INSERT INTO users (username, email, password, hashed_password, role, study_level, 
                             full_name, is_active, is_verified, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            "testuser", "test@example.com", password, hashed_password, "student", "beginner",
            "测试用户", True, True, datetime.utcnow(), datetime.utcnow()
        ))
        
        conn.commit()
        print("✅ 测试用户创建成功")
        print("📋 测试用户信息:")
        print("   - 用户名: testuser")
        print("   - 密码: test123")
        print("   - 邮箱: test@example.com")
        print("   - 角色: student")
        
    except Exception as e:
        print(f"❌ 创建测试用户失败: {e}")
        conn.rollback()
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

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  python fix_database.py check        # 检查表结构")
        print("  python fix_database.py fix          # 修复表结构")
        print("  python fix_database.py create       # 创建测试用户")
        print("  python fix_database.py list         # 列出用户")
        print("  python fix_database.py all          # 执行所有操作")
        return
    
    command = sys.argv[1].lower()
    
    if command == "check":
        check_table_structure()
    elif command == "fix":
        missing_columns = check_table_structure()
        if missing_columns:
            add_missing_columns(missing_columns)
    elif command == "create":
        create_test_user()
    elif command == "list":
        list_users()
    elif command == "all":
        print("🔧 执行完整的数据库修复流程...")
        missing_columns = check_table_structure()
        if missing_columns:
            add_missing_columns(missing_columns)
        create_test_user()
        list_users()
    else:
        print(f"❌ 未知命令: {command}")

if __name__ == "__main__":
    main() 