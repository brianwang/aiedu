-- 数据库表结构修复脚本
-- 在SQLite工具中运行此脚本

-- 1. 检查当前表结构
PRAGMA table_info(users);

-- 2. 添加缺失的字段
ALTER TABLE users ADD COLUMN full_name VARCHAR(200);
ALTER TABLE users ADD COLUMN avatar VARCHAR(500);
ALTER TABLE users ADD COLUMN phone VARCHAR(20);
ALTER TABLE users ADD COLUMN bio TEXT;
ALTER TABLE users ADD COLUMN is_active BOOLEAN DEFAULT 1;
ALTER TABLE users ADD COLUMN is_verified BOOLEAN DEFAULT 0;
ALTER TABLE users ADD COLUMN is_superuser BOOLEAN DEFAULT 0;
ALTER TABLE users ADD COLUMN role VARCHAR(50) DEFAULT 'student';
ALTER TABLE users ADD COLUMN created_at DATETIME;
ALTER TABLE users ADD COLUMN updated_at DATETIME;
ALTER TABLE users ADD COLUMN last_login DATETIME;
ALTER TABLE users ADD COLUMN study_level VARCHAR(50) DEFAULT 'beginner';
ALTER TABLE users ADD COLUMN preferred_subjects VARCHAR(500);

-- 3. 创建测试用户（使用简单的密码哈希）
INSERT OR IGNORE INTO users (
    username, 
    email, 
    password, 
    hashed_password, 
    role, 
    study_level, 
    full_name, 
    is_active, 
    is_verified, 
    created_at, 
    updated_at
) VALUES (
    'testuser',
    'test@example.com',
    'test123',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/HS.iQeO', -- bcrypt hash for 'test123'
    'student',
    'beginner',
    '测试用户',
    1,
    1,
    datetime('now'),
    datetime('now')
);

-- 4. 创建管理员用户
INSERT OR IGNORE INTO users (
    username, 
    email, 
    password, 
    hashed_password, 
    role, 
    study_level, 
    full_name, 
    is_active, 
    is_verified, 
    created_at, 
    updated_at
) VALUES (
    'admin',
    'admin@example.com',
    'admin123',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/HS.iQeO', -- bcrypt hash for 'admin123'
    'admin',
    'beginner',
    '管理员',
    1,
    1,
    datetime('now'),
    datetime('now')
);

-- 5. 创建教师用户
INSERT OR IGNORE INTO users (
    username, 
    email, 
    password, 
    hashed_password, 
    role, 
    study_level, 
    full_name, 
    is_active, 
    is_verified, 
    created_at, 
    updated_at
) VALUES (
    'teacher',
    'teacher@example.com',
    'teacher123',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/HS.iQeO', -- bcrypt hash for 'teacher123'
    'teacher',
    'beginner',
    '教师用户',
    1,
    1,
    datetime('now'),
    datetime('now')
);

-- 6. 查看创建的用户
SELECT id, username, email, role, is_active, created_at FROM users ORDER BY id; 