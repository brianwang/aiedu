from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from typing import List, Dict, Any
from database import get_db
from app.models.user import User
from app.models.question import Question
from app.models.exam import Exam, ExamResult
from app.models.learning import LearningProgress, LearningTask, Achievement
from app.services.auth_service import get_current_user
from datetime import datetime, timedelta
import json

router = APIRouter(prefix="/dashboard", tags=["仪表板"])


@router.get("/home-stats", summary="获取首页统计数据")
async def get_home_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取首页实时统计数据"""
    try:
        # 获取题目总数
        total_questions = db.query(func.count(Question.id)).scalar() or 0
        
        # 获取用户完成的考试数
        completed_exams = db.query(func.count(ExamResult.id)).filter(
            ExamResult.user_id == current_user.id,
            ExamResult.status == "completed"
        ).scalar() or 0
        
        # 获取用户学习时长（小时）
        study_hours = db.query(func.sum(LearningProgress.duration_minutes)).filter(
            LearningProgress.user_id == current_user.id
        ).scalar() or 0
        study_hours = round(study_hours / 60, 1)  # 转换为小时
        
        # 计算平均正确率
        avg_accuracy = db.query(func.avg(ExamResult.score)).filter(
            ExamResult.user_id == current_user.id,
            ExamResult.status == "completed"
        ).scalar() or 0
        avg_accuracy = round(avg_accuracy, 1)
        
        return {
            "totalQuestions": total_questions,
            "completedExams": completed_exams,
            "studyHours": study_hours,
            "accuracy": avg_accuracy
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取统计数据失败: {str(e)}"
        )


@router.get("/recent-activity", summary="获取最近活动")
async def get_recent_activity(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取用户最近的学习活动"""
    try:
        # 获取最近的考试结果
        recent_exams = db.query(ExamResult).filter(
            ExamResult.user_id == current_user.id
        ).order_by(ExamResult.created_at.desc()).limit(5).all()
        
        # 获取最近的学习任务
        recent_tasks = db.query(LearningTask).filter(
            LearningTask.user_id == current_user.id
        ).order_by(LearningTask.created_at.desc()).limit(5).all()
        
        activities = []
        
        # 添加考试活动
        for exam in recent_exams:
            activities.append({
                "id": exam.id,
                "type": "exam",
                "title": exam.exam.title if exam.exam else "考试",
                "score": exam.score,
                "date": exam.created_at.strftime("%Y-%m-%d"),
                "status": exam.status
            })
        
        # 添加任务活动
        for task in recent_tasks:
            activities.append({
                "id": task.id,
                "type": "task",
                "title": task.title,
                "score": None,
                "date": task.created_at.strftime("%Y-%m-%d"),
                "status": task.status
            })
        
        # 按日期排序
        activities.sort(key=lambda x: x["date"], reverse=True)
        
        return activities[:10]  # 返回最近10个活动
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取最近活动失败: {str(e)}"
        )


@router.get("/subject-progress", summary="获取学科进度")
async def get_subject_progress(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取各学科的学习进度"""
    try:
        # 获取题目按学科分类的统计
        subject_stats = db.query(
            Question.subject,
            func.count(Question.id).label('total_questions')
        ).group_by(Question.subject).all()
        
        # 获取用户在各学科的答题情况
        user_progress = db.query(
            Question.subject,
            func.count(ExamResult.id).label('answered_questions'),
            func.avg(ExamResult.score).label('avg_score')
        ).join(ExamResult, Question.id == ExamResult.question_id).filter(
            ExamResult.user_id == current_user.id,
            ExamResult.status == "completed"
        ).group_by(Question.subject).all()
        
        subjects = []
        subject_icons = {
            "数学": "📊",
            "英语": "🔤", 
            "物理": "⚛️",
            "化学": "🧪",
            "生物": "🧬",
            "语文": "📝",
            "历史": "📚",
            "地理": "🌍",
            "政治": "🏛️"
        }
        
        for subject_stat in subject_stats:
            subject_name = subject_stat.subject
            total_questions = subject_stat.total_questions
            
            # 查找用户进度
            user_stat = next((p for p in user_progress if p.subject == subject_name), None)
            answered_questions = user_stat.answered_questions if user_stat else 0
            avg_score = user_stat.avg_score if user_stat else 0
            
            # 计算进度百分比
            progress = round((answered_questions / total_questions * 100) if total_questions > 0 else 0, 1)
            
            # 确定难度
            if progress < 30:
                difficulty = "hard"
            elif progress < 70:
                difficulty = "medium"
            else:
                difficulty = "easy"
            
            subjects.append({
                "name": subject_name,
                "questions": total_questions,
                "icon": subject_icons.get(subject_name, "📖"),
                "difficulty": difficulty,
                "progress": progress,
                "answered": answered_questions,
                "avgScore": round(avg_score, 1)
            })
        
        return subjects
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取学科进度失败: {str(e)}"
        )


@router.get("/achievements", summary="获取用户成就")
async def get_user_achievements(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取用户成就统计"""
    try:
        achievements = db.query(Achievement).filter(
            Achievement.user_id == current_user.id
        ).all()
        
        return {
            "total": len(achievements),
            "recent": achievements[-5:] if len(achievements) > 5 else achievements,
            "list": achievements
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取成就失败: {str(e)}"
        )


@router.get("/learning-trends", summary="获取学习趋势")
async def get_learning_trends(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取用户学习趋势数据"""
    try:
        # 获取最近30天的学习数据
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        
        daily_progress = db.query(
            func.date(LearningProgress.created_at).label('date'),
            func.sum(LearningProgress.duration_minutes).label('duration'),
            func.count(LearningProgress.id).label('sessions')
        ).filter(
            LearningProgress.user_id == current_user.id,
            LearningProgress.created_at >= start_date,
            LearningProgress.created_at <= end_date
        ).group_by(func.date(LearningProgress.created_at)).all()
        
        # 获取每日答题数据
        daily_exams = db.query(
            func.date(ExamResult.created_at).label('date'),
            func.count(ExamResult.id).label('questions'),
            func.avg(ExamResult.score).label('avg_score')
        ).filter(
            ExamResult.user_id == current_user.id,
            ExamResult.created_at >= start_date,
            ExamResult.created_at <= end_date
        ).group_by(func.date(ExamResult.created_at)).all()
        
        # 构建趋势数据
        trends = []
        for i in range(30):
            date = (end_date - timedelta(days=i)).strftime("%Y-%m-%d")
            
            # 查找当日学习进度
            progress_data = next((p for p in daily_progress if p.date.strftime("%Y-%m-%d") == date), None)
            duration = progress_data.duration if progress_data else 0
            sessions = progress_data.sessions if progress_data else 0
            
            # 查找当日答题数据
            exam_data = next((e for e in daily_exams if e.date.strftime("%Y-%m-%d") == date), None)
            questions = exam_data.questions if exam_data else 0
            avg_score = exam_data.avg_score if exam_data else 0
            
            trends.append({
                "date": date,
                "duration": duration,
                "sessions": sessions,
                "questions": questions,
                "avgScore": round(avg_score, 1) if avg_score else 0
            })
        
        return trends[::-1]  # 按日期正序返回
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取学习趋势失败: {str(e)}"
        ) 