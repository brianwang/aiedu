-- AI学习计划系统数据库表结构

-- 用户画像表
CREATE TABLE IF NOT EXISTS user_profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    age INTEGER,
    learning_style VARCHAR(50), -- visual, auditory, kinesthetic
    difficulty_preference VARCHAR(50), -- progressive, challenging, comfortable
    daily_study_time INTEGER, -- 分钟
    weekly_study_days INTEGER,
    learning_environment VARCHAR(50), -- online, offline, hybrid
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 学习目标表
CREATE TABLE IF NOT EXISTS learning_goals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    subject VARCHAR(100) NOT NULL,
    skill_area VARCHAR(100),
    target_level VARCHAR(50), -- beginner, intermediate, advanced, expert
    target_timeframe INTEGER, -- 月
    priority INTEGER DEFAULT 1,
    status VARCHAR(20) DEFAULT 'active', -- active, completed, paused
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 学习计划表
CREATE TABLE IF NOT EXISTS learning_plans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    plan_type VARCHAR(20) NOT NULL, -- short_term, medium_term, long_term
    title VARCHAR(200) NOT NULL,
    description TEXT,
    start_date DATE,
    end_date DATE,
    status VARCHAR(20) DEFAULT 'active', -- active, completed, paused
    ai_generated BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 学习任务表
CREATE TABLE IF NOT EXISTS learning_tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    plan_id INTEGER NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    task_type VARCHAR(50), -- study, practice, review, assessment
    difficulty INTEGER DEFAULT 1, -- 1-5
    estimated_time INTEGER, -- 分钟
    due_date DATE,
    status VARCHAR(20) DEFAULT 'pending', -- pending, in_progress, completed, overdue
    completed_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (plan_id) REFERENCES learning_plans(id) ON DELETE CASCADE
);

-- 学习提醒表
CREATE TABLE IF NOT EXISTS learning_reminders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    task_id INTEGER,
    reminder_time DATETIME NOT NULL,
    reminder_type VARCHAR(20) DEFAULT 'push', -- email, sms, push
    status VARCHAR(20) DEFAULT 'pending', -- pending, sent, completed
    sent_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (task_id) REFERENCES learning_tasks(id) ON DELETE CASCADE
);

-- 成就系统表
CREATE TABLE IF NOT EXISTS achievements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    achievement_type VARCHAR(50) NOT NULL, -- daily_streak, milestone, skill_mastery
    title VARCHAR(100) NOT NULL,
    description TEXT,
    points INTEGER DEFAULT 0,
    earned_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 学习进度表
CREATE TABLE IF NOT EXISTS learning_progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    task_id INTEGER,
    study_time INTEGER DEFAULT 0, -- 实际学习时间（分钟）
    completion_rate FLOAT DEFAULT 0.0, -- 完成率 0-1
    notes TEXT,
    recorded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (task_id) REFERENCES learning_tasks(id) ON DELETE CASCADE
);

-- 技能点表
CREATE TABLE IF NOT EXISTS skill_point (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name VARCHAR(64) NOT NULL UNIQUE,
  description TEXT
);

INSERT OR IGNORE INTO skill_point (name, description) VALUES
  ('阅读理解', '提升阅读理解能力'),
  ('算法', '基础算法技能'),
  ('英语单词', '英语词汇记忆'),
  ('写作', '写作表达能力'),
  ('数学思维', '数学逻辑与推理能力');

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_user_profiles_user_id ON user_profiles(user_id);
CREATE INDEX IF NOT EXISTS idx_learning_goals_user_id ON learning_goals(user_id);
CREATE INDEX IF NOT EXISTS idx_learning_plans_user_id ON learning_plans(user_id);
CREATE INDEX IF NOT EXISTS idx_learning_tasks_plan_id ON learning_tasks(plan_id);
CREATE INDEX IF NOT EXISTS idx_learning_reminders_user_id ON learning_reminders(user_id);
CREATE INDEX IF NOT EXISTS idx_achievements_user_id ON achievements(user_id);
CREATE INDEX IF NOT EXISTS idx_learning_progress_user_id ON learning_progress(user_id); 