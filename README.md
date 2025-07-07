# AI智能教育平台

一个基于人工智能的智能学习和学习规划平台，为学生提供个性化的学习体验。

## 🚀 功能特性

### 核心功能

* **智能题库系统** - 支持多种题型，智能难度调节
* **个性化学习规划** - 基于学习数据分析制定学习计划
* **智能考试系统** - 自动组卷、智能评分
* **学习进度跟踪** - 实时监控学习效果
* **错题本系统** - 智能错题收集和复习提醒

### 高级功能

* **AI智能推荐** - 基于学习行为推荐适合的题目
* **学习数据分析** - 详细的学习报告和统计
* **多角色支持** - 学生、教师、管理员不同权限
* **实时通知** - 学习提醒和进度通知

## 🛠️ 技术栈

### 后端

* **FastAPI** - 高性能Python Web框架
* **SQLAlchemy** - ORM数据库操作
* **Alembic** - 数据库迁移管理
* **JWT** - 用户认证
* **SQLite** - 数据库（可扩展至PostgreSQL/MySQL）

### 前端

* **Vue 3** - 渐进式JavaScript框架
* **TypeScript** - 类型安全的JavaScript
* **Vue Router** - 前端路由
* **Pinia** - 状态管理
* **Naive UI** - 现代化UI组件库
* **Vite** - 快速构建工具

## 📦 安装指南

### 环境要求

* Python 3.8+
* Node.js 16+
* pnpm (推荐) 或 npm

### 后端安装

```bash
cd backend
pip install -r requirements.txt
python main.py
```

### 前端安装

```bash
cd frontend
pnpm install
pnpm dev
```

### 数据库初始化

```bash
cd backend
alembic upgrade head
```

## 🎯 使用指南

### 学生用户

1. 注册/登录账户
2. 选择学科和难度
3. 开始练习或参加考试
4. 查看学习进度和错题本
5. 获取个性化学习建议

### 教师用户

1. 创建和管理题库
2. 设计考试试卷
3. 查看学生成绩统计
4. 分析学习数据

### 管理员

1. 用户管理
2. 系统配置
3. 数据备份
4. 权限管理

## 📁 项目结构

```
aiedu-2/
├── backend/                 # 后端代码
│   ├── app/
│   │   ├── api/            # API路由
│   │   ├── models/         # 数据模型
│   │   ├── schemas/        # 数据验证
│   │   ├── services/       # 业务逻辑
│   │   └── utils/          # 工具函数
│   ├── alembic/            # 数据库迁移
│   └── main.py             # 应用入口
├── frontend/               # 前端代码
│   ├── src/
│   │   ├── api/           # API调用
│   │   ├── components/    # 组件
│   │   ├── views/         # 页面
│   │   ├── stores/        # 状态管理
│   │   └── router/        # 路由配置
│   └── package.json
└── prompts.txt            # AI提示词
```

## 🔧 开发指南

### 添加新功能

1. 在后端 `app/models/` 中定义数据模型
2. 在 `app/schemas/` 中定义数据验证
3. 在 `app/services/` 中实现业务逻辑
4. 在 `app/api/` 中定义API接口
5. 在前端 `src/views/` 中创建页面
6. 在 `src/api/` 中添加API调用

### 数据库迁移

```bash
# 创建迁移文件
alembic revision --autogenerate -m "描述"

# 执行迁移
alembic upgrade head
```

## 🚀 部署

### 生产环境部署

1. 配置环境变量
2. 使用生产级数据库（PostgreSQL/MySQL）
3. 配置反向代理（Nginx）
4. 使用进程管理器（PM2/Supervisor）

### Docker部署

```bash
# 构建镜像
docker build -t aiedu-platform .

# 运行容器
docker run -p 8000:8000 aiedu-platform
```

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 📄 许可证

MIT License

## 📞 联系方式

* 项目维护者：\[您的姓名]
* 邮箱：\[您的邮箱]
* 项目地址：\[GitHub地址]

***

**版本**: 1.0.0\
**最后更新**: 2025年7月
