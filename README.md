# AI智能教育平台

一个基于AI的智能教育平台，提供个性化学习体验、智能题库、学习分析等功能。

## 🚀 快速启动

### 方法一：使用启动脚本（推荐）

**Windows用户：**
```bash
start.bat
```

**Linux/Mac用户：**
```bash
chmod +x start.sh
./start.sh
```

### 方法二：手动启动

#### 1. 启动后端服务

```bash
cd backend

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 启动服务
python main.py
```

#### 2. 启动前端服务

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

## 📱 访问地址

- **前端应用**: http://localhost:5173
- **后端API**: http://localhost:8111
- **API文档**: http://localhost:8111/docs

## 🔧 环境要求

- Python 3.8+
- Node.js 16+
- npm 或 pnpm

## 🛠️ 项目结构

```
aiedu/
├── backend/                 # 后端服务 (FastAPI)
│   ├── app/
│   │   ├── api/            # API路由
│   │   ├── models/         # 数据模型
│   │   ├── services/       # 业务逻辑
│   │   └── schemas/        # 数据验证
│   ├── database/           # 数据库配置
│   └── main.py            # 应用入口
├── frontend/               # 前端应用 (Vue 3 + TypeScript)
│   ├── src/
│   │   ├── api/           # API调用
│   │   ├── components/    # Vue组件
│   │   ├── views/         # 页面视图
│   │   └── stores/        # 状态管理
│   └── package.json
└── README.md
```

## 🎯 主要功能

### 用户系统
- 多角色用户管理（学生、教师、管理员）
- JWT身份认证
- 用户注册和登录

### 智能题库
- 题目分类管理
- 难度分级
- 智能推荐算法
- AI生成题目

### 学习分析
- 学习进度跟踪
- 能力评估
- 学习风格分析
- 个性化学习计划

### AI功能
- 智能评分
- 学习动机激励
- 难度分析
- 学习模式识别

## 🔍 问题排查

### 1. 登录失败 (404错误)

**问题原因：**
- 前后端端口不匹配
- API路径配置错误
- 代理设置问题

**解决方案：**
1. 确保后端运行在8111端口
2. 检查前端API调用路径是否包含`/api/v1`前缀
3. 验证Vite代理配置正确

### 2. 数据库连接失败

**解决方案：**
```bash
cd backend
python -c "from database import engine; print('数据库连接正常')"
```

### 3. 前端依赖安装失败

**解决方案：**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### 4. Python依赖安装失败

**解决方案：**
```bash
cd backend
pip install --upgrade pip
pip install -r requirements.txt
```

## 📝 API文档

启动后端服务后，访问 http://localhost:8111/docs 查看完整的API文档。

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 📞 联系方式

如有问题或建议，请提交 Issue 或联系开发团队。
