@echo off
echo 正在修复数据库表结构...

REM 尝试使用Python运行SQL脚本
python -c "
import sqlite3
try:
    conn = sqlite3.connect('sql_app.db')
    cursor = conn.cursor()
    
    # 读取SQL文件
    with open('fix_database.sql', 'r', encoding='utf-8') as f:
        sql_script = f.read()
    
    # 执行SQL脚本
    cursor.executescript(sql_script)
    conn.commit()
    print('✅ 数据库修复成功！')
    
    # 显示用户列表
    cursor.execute('SELECT id, username, email, role FROM users ORDER BY id')
    users = cursor.fetchall()
    print('\n📋 用户列表:')
    print('ID  用户名      邮箱                角色')
    print('-' * 50)
    for user in users:
        print(f'{user[0]:<4} {user[1]:<12} {user[2]:<20} {user[3]}')
    
    conn.close()
except Exception as e:
    print(f'❌ 错误: {e}')
" 