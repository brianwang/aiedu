# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an AI Education Platform (智能学习和学习规划项目) with a FastAPI backend and Vue.js frontend, featuring a question bank system, intelligent learning planning, and exam functionality.

## Architecture

**Backend (Python + FastAPI)**
- `backend/main.py`: FastAPI application entry point
- `backend/app/`: Core application logic
  - `api/`: REST API endpoints (auth, exam, question)
  - `models/`: SQLAlchemy database models (User, Exam, Question)
  - `schemas/`: Pydantic request/response schemas
  - `services/`: Business logic layer
  - `utils/`: Shared utilities (JWT handling)
- `backend/database/`: SQLAlchemy database configuration (SQLite)
- `backend/alembic/`: Database migration management

**Frontend (Vue.js 3 + TypeScript)**
- `frontend/src/`: Vue application source
  - `api/`: HTTP client functions for backend communication
  - `views/`: Page components (Home, Login, Exam, QuestionBank, etc.)
  - `stores/`: Pinia state management (auth store)
  - `router/`: Vue Router configuration with auth guards
  - `composables/`: Reusable composition functions

## Common Commands

**Backend Development:**
```bash
cd backend
pip install -r requirements.txt
python main.py  # Run development server on port 8000
```

**Frontend Development:**
```bash
cd frontend
npm install  # or pnpm install
npm run dev  # Run development server with Vite
npm run build  # Build for production
npm run preview  # Preview production build
```

**Database Management:**
```bash
cd backend
alembic upgrade head  # Apply migrations
alembic revision --autogenerate -m "description"  # Create new migration
```

## Key Technical Details

- **Database**: SQLite with SQLAlchemy ORM and Alembic migrations
- **Authentication**: JWT-based with bcrypt password hashing
- **CORS**: Configured to allow all origins for development
- **API Proxy**: Frontend proxies `/api/*` requests to `http://127.0.0.1:8000`
- **State Management**: Pinia for Vue.js state management
- **UI Library**: Naive UI components
- **Route Protection**: Vue Router guards check authentication state

## Database Models

- **User**: Authentication and profile (id, email, username, password hashes)
- **Exam**: Exam definitions with timing and creator relationships  
- **ExamResult**: Student exam submissions with JSON answers and scoring
- **Question**: Question bank with categories and difficulty levels

## Authentication Flow

Frontend stores JWT tokens and uses auth guards to protect routes. Backend validates tokens using python-jose library with HS256 algorithm.