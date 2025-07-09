#!/usr/bin/env python3
"""
检查学习计划相关的数据库表和数据
"""

import sqlite3
import os
from pathlib import Path

def check_database():
    db_path = Path(__file__).parent / "sql_app.db"
    
    if not db_path.exists():
        print("❌ 数据库文件不存在")
        return
    
    print(f"📁 数据库文件: {db_path}")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 检查所有表
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"\n📋 数据库表: {[table[0] for table in tables]}")
        
        # 检查学习计划相关表
        learning_tables = [
            'learning_plans',
            'learning_tasks', 
            'learning_progress',
            'learning_reminders',
            'achievements',
            'user_profiles',
            'learning_goals'
        ]
        
        for table in learning_tables:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"📊 {table}: {count} 条记录")
                
                if count > 0:
                    cursor.execute(f"SELECT * FROM {table} LIMIT 3")
                    rows = cursor.fetchall()
                    print(f"   📝 示例数据: {rows[:2]}")
            except sqlite3.OperationalError as e:
                print(f"❌ {table}: 表不存在 - {e}")
        
        # 检查用户表
        try:
            cursor.execute("SELECT COUNT(*) FROM users")
            user_count = cursor.fetchone()[0]
            print(f"\n👥 用户数量: {user_count}")
            
            if user_count > 0:
                cursor.execute("SELECT id, username, email FROM users LIMIT 3")
                users = cursor.fetchall()
                print(f"   📝 用户示例: {users}")
        except sqlite3.OperationalError as e:
            print(f"❌ users表不存在: {e}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ 检查数据库失败: {e}")

if __name__ == "__main__":
    check_database() 