import logging
from typing import Dict, List, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, desc, case
from app.models.user import User
from app.models.question import Question
from app.models.exam import Exam, ExamResult
from app.models.learning import LearningProgress, LearningTask, UserProfile, Achievement
from app.services.ai_service import AIService
from datetime import datetime, timedelta
import json

logger = logging.getLogger(__name__)


class LearningReportService:
    def __init__(self, db: Session):
        self.db = db
        self.ai_service = AIService()
    
    async def generate_daily_report(self, user_id: int) -> Dict[str, Any]:
        """生成每日学习报告"""
        try:
            # 获取用户基本信息
            user = self.db.query(User).filter(User.id == user_id).first()
            if not user:
                raise ValueError("用户不存在")
            
            # 获取今日学习数据
            today = datetime.now().date()
            today_start = datetime.combine(today, datetime.min.time())
            today_end = datetime.combine(today, datetime.max.time())
            
            # 今日学习时长
            today_study_time = self.db.query(func.sum(LearningProgress.duration_minutes)).filter(
                LearningProgress.user_id == user_id,
                LearningProgress.created_at >= today_start,
                LearningProgress.created_at <= today_end
            ).scalar() or 0
            
            # 今日答题数量
            today_questions = self.db.query(func.count(ExamResult.id)).filter(
                ExamResult.user_id == user_id,
                ExamResult.created_at >= today_start,
                ExamResult.created_at <= today_end
            ).scalar() or 0
            
            # 今日平均分数
            today_avg_score = self.db.query(func.avg(ExamResult.score)).filter(
                ExamResult.user_id == user_id,
                ExamResult.created_at >= today_start,
                ExamResult.created_at <= today_end,
                ExamResult.status == "completed"
            ).scalar() or 0
            
            # 获取本周学习趋势
            week_trends = self._get_weekly_trends(user_id)
            
            # 获取学科表现
            subject_performance = self._get_subject_performance(user_id)
            
            # 获取学习建议
            learning_suggestions = await self._generate_learning_suggestions(user_id, today_avg_score)
            
            # 生成成长曲线数据
            growth_curve = self._generate_growth_curve(user_id)
            
            report = {
                "date": today.strftime("%Y-%m-%d"),
                "user_name": user.username,
                "today_summary": {
                    "study_time_minutes": today_study_time,
                    "study_time_hours": round(today_study_time / 60, 1),
                    "questions_answered": today_questions,
                    "average_score": round(today_avg_score, 1),
                    "completion_rate": self._calculate_completion_rate(user_id, today_start, today_end)
                },
                "weekly_trends": week_trends,
                "subject_performance": subject_performance,
                "learning_suggestions": learning_suggestions,
                "growth_curve": growth_curve,
                "achievements": self._get_recent_achievements(user_id),
                "next_day_tasks": await self._generate_next_day_tasks(user_id)
            }
            
            logger.info(f"为用户 {user_id} 生成每日学习报告成功")
            return report
            
        except Exception as e:
            logger.error(f"生成每日学习报告失败: {str(e)}")
            return self._generate_default_report(user_id)
    
    def _get_weekly_trends(self, user_id: int) -> Dict[str, Any]:
        """获取本周学习趋势"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        
        # 每日学习时长
        daily_study_time = self.db.query(
            func.date(LearningProgress.created_at).label('date'),
            func.sum(LearningProgress.duration_minutes).label('duration')
        ).filter(
            LearningProgress.user_id == user_id,
            LearningProgress.created_at >= start_date,
            LearningProgress.created_at <= end_date
        ).group_by(func.date(LearningProgress.created_at)).all()
        
        # 每日答题数量
        daily_questions = self.db.query(
            func.date(ExamResult.created_at).label('date'),
            func.count(ExamResult.id).label('count')
        ).filter(
            ExamResult.user_id == user_id,
            ExamResult.created_at >= start_date,
            ExamResult.created_at <= end_date
        ).group_by(func.date(ExamResult.created_at)).all()
        
        # 构建趋势数据
        trends = []
        for i in range(7):
            date = (end_date - timedelta(days=i)).strftime("%Y-%m-%d")
            
            study_data = next((d for d in daily_study_time if d.date.strftime("%Y-%m-%d") == date), None)
            question_data = next((q for q in daily_questions if q.date.strftime("%Y-%m-%d") == date), None)
            
            trends.append({
                "date": date,
                "study_time": study_data.duration if study_data else 0,
                "questions": question_data.count if question_data else 0
            })
        
        return {
            "daily_data": trends[::-1],  # 按日期正序
            "total_study_time": sum(t["study_time"] for t in trends),
            "total_questions": sum(t["questions"] for t in trends),
            "avg_daily_study_time": round(sum(t["study_time"] for t in trends) / 7, 1),
            "avg_daily_questions": round(sum(t["questions"] for t in trends) / 7, 1)
        }
    
    def _get_subject_performance(self, user_id: int) -> List[Dict[str, Any]]:
        """获取各学科表现"""
        # 获取用户在各学科的答题情况
        subject_stats = self.db.query(
            Question.subject,
            func.count(ExamResult.id).label('total_questions'),
            func.avg(ExamResult.score).label('avg_score'),
            func.sum(case((ExamResult.score >= 60, 1), else_=0)).label('passed_questions')
        ).join(ExamResult, Question.id == ExamResult.question_id).filter(
            ExamResult.user_id == user_id,
            ExamResult.status == "completed"
        ).group_by(Question.subject).all()
        
        performance = []
        for stat in subject_stats:
            pass_rate = round((stat.passed_questions / stat.total_questions * 100) if stat.total_questions > 0 else 0, 1)
            performance.append({
                "subject": stat.subject,
                "total_questions": stat.total_questions,
                "average_score": round(stat.avg_score, 1),
                "pass_rate": pass_rate,
                "performance_level": self._get_performance_level(stat.avg_score)
            })
        
        return performance
    
    def _get_performance_level(self, avg_score: float) -> str:
        """获取表现等级"""
        if avg_score >= 90:
            return "优秀"
        elif avg_score >= 80:
            return "良好"
        elif avg_score >= 70:
            return "中等"
        elif avg_score >= 60:
            return "及格"
        else:
            return "需努力"
    
    async def _generate_learning_suggestions(self, user_id: int, today_avg_score: float) -> List[str]:
        """生成学习建议"""
        try:
            # 获取用户画像
            profile = self.db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
            
            # 分析学习数据
            suggestions = []
            
            # 基于今日表现的建议
            if today_avg_score < 60:
                suggestions.append("今日答题正确率较低，建议复习基础知识，巩固薄弱环节")
            elif today_avg_score < 80:
                suggestions.append("今日表现良好，建议继续保持，可以尝试挑战更高难度的题目")
            else:
                suggestions.append("今日表现优秀！建议保持学习热情，可以探索更深层的知识点")
            
            # 基于学习时长的建议
            today_study_time = self.db.query(func.sum(LearningProgress.duration_minutes)).filter(
                LearningProgress.user_id == user_id,
                LearningProgress.created_at >= datetime.now().date()
            ).scalar() or 0
            
            if today_study_time < 30:
                suggestions.append("今日学习时间较短，建议增加学习时长，保持学习连续性")
            elif today_study_time > 180:
                suggestions.append("今日学习时间充足，注意适当休息，保持学习效率")
            
            # 基于学科表现的建议
            weak_subjects = self._get_weak_subjects(user_id)
            if weak_subjects:
                suggestions.append(f"建议重点加强{', '.join(weak_subjects)}等薄弱学科的学习")
            
            # 使用AI生成个性化建议
            if self.ai_service._ai_available:
                ai_suggestions = await self._get_ai_suggestions(user_id, profile, today_avg_score)
                suggestions.extend(ai_suggestions)
            
            return suggestions[:5]  # 返回前5条建议
            
        except Exception as e:
            logger.error(f"生成学习建议失败: {str(e)}")
            return ["建议保持规律的学习习惯，每天坚持练习", "多关注错题分析，理解解题思路"]
    
    def _get_weak_subjects(self, user_id: int) -> List[str]:
        """获取薄弱学科"""
        weak_subjects = self.db.query(Question.subject).join(ExamResult, Question.id == ExamResult.question_id).filter(
            ExamResult.user_id == user_id,
            ExamResult.status == "completed",
            ExamResult.score < 60
        ).group_by(Question.subject).having(
            func.count(ExamResult.id) >= 3
        ).all()
        
        return [subject.subject for subject in weak_subjects]
    
    async def _get_ai_suggestions(self, user_id: int, profile: UserProfile, today_avg_score: float) -> List[str]:
        """使用AI生成个性化建议"""
        try:
            prompt = f"""
基于以下用户信息生成2-3条个性化的学习建议：

用户学习风格：{profile.learning_style if profile else '未知'}
今日平均分数：{today_avg_score}
学习目标：{profile.learning_goals if profile else '未设置'}

请提供具体、可操作的学习建议，每条建议不超过50字。
"""
            
            response = await self.ai_service._call_ai_api(prompt)
            if response:
                # 简单解析AI响应
                suggestions = [s.strip() for s in response.split('\n') if s.strip() and len(s.strip()) > 10]
                return suggestions[:3]
            
        except Exception as e:
            logger.error(f"AI生成建议失败: {str(e)}")
        
        return []
    
    def _generate_growth_curve(self, user_id: int) -> Dict[str, Any]:
        """生成成长曲线数据"""
        # 获取最近30天的学习数据
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        
        # 每日学习进度
        daily_progress = self.db.query(
            func.date(LearningProgress.created_at).label('date'),
            func.sum(LearningProgress.duration_minutes).label('duration'),
            func.count(ExamResult.id).label('questions'),
            func.avg(ExamResult.score).label('avg_score')
        ).outerjoin(ExamResult, LearningProgress.user_id == ExamResult.user_id).filter(
            LearningProgress.user_id == user_id,
            LearningProgress.created_at >= start_date,
            LearningProgress.created_at <= end_date
        ).group_by(func.date(LearningProgress.created_at)).all()
        
        # 构建成长曲线
        growth_data = []
        cumulative_study_time = 0
        cumulative_questions = 0
        
        for progress in daily_progress:
            cumulative_study_time += progress.duration or 0
            cumulative_questions += progress.questions or 0
            
            growth_data.append({
                "date": progress.date.strftime("%Y-%m-%d"),
                "daily_study_time": progress.duration or 0,
                "daily_questions": progress.questions or 0,
                "daily_avg_score": round(progress.avg_score, 1) if progress.avg_score else 0,
                "cumulative_study_time": cumulative_study_time,
                "cumulative_questions": cumulative_questions
            })
        
        return {
            "daily_data": growth_data,
            "total_study_time": cumulative_study_time,
            "total_questions": cumulative_questions,
            "growth_rate": self._calculate_growth_rate(growth_data)
        }
    
    def _calculate_growth_rate(self, growth_data: List[Dict]) -> Dict[str, float]:
        """计算成长率"""
        if len(growth_data) < 7:
            return {"study_time": 0, "questions": 0}
        
        # 计算最近7天与前7天的对比
        recent_7_days = growth_data[-7:]
        previous_7_days = growth_data[-14:-7] if len(growth_data) >= 14 else growth_data[:7]
        
        recent_study_time = sum(d["daily_study_time"] for d in recent_7_days)
        previous_study_time = sum(d["daily_study_time"] for d in previous_7_days)
        
        recent_questions = sum(d["daily_questions"] for d in recent_7_days)
        previous_questions = sum(d["daily_questions"] for d in previous_7_days)
        
        study_time_growth = ((recent_study_time - previous_study_time) / previous_study_time * 100) if previous_study_time > 0 else 0
        questions_growth = ((recent_questions - previous_questions) / previous_questions * 100) if previous_questions > 0 else 0
        
        return {
            "study_time": round(study_time_growth, 1),
            "questions": round(questions_growth, 1)
        }
    
    def _get_recent_achievements(self, user_id: int) -> List[Dict]:
        """获取最近成就"""
        achievements = self.db.query(Achievement).filter(
            Achievement.user_id == user_id
        ).order_by(Achievement.created_at.desc()).limit(5).all()
        
        return [
            {
                "id": achievement.id,
                "title": achievement.title,
                "description": achievement.description,
                "achieved_at": achievement.created_at.strftime("%Y-%m-%d")
            }
            for achievement in achievements
        ]
    
    async def _generate_next_day_tasks(self, user_id: int) -> List[Dict]:
        """生成明日学习任务"""
        try:
            # 获取用户画像和学习目标
            profile = self.db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
            
            # 基于薄弱学科生成任务
            weak_subjects = self._get_weak_subjects(user_id)
            tasks = []
            
            for subject in weak_subjects[:3]:  # 最多3个学科
                tasks.append({
                    "subject": subject,
                    "task_type": "practice",
                    "title": f"复习{subject}基础知识",
                    "description": f"完成{subject}相关练习，巩固薄弱环节",
                    "estimated_time": 30,
                    "priority": "high"
                })
            
            # 添加通用学习任务
            tasks.append({
                "subject": "综合",
                "task_type": "review",
                "title": "错题复习",
                "description": "复习本周的错题，理解解题思路",
                "estimated_time": 20,
                "priority": "medium"
            })
            
            return tasks
            
        except Exception as e:
            logger.error(f"生成明日任务失败: {str(e)}")
            return []
    
    def _calculate_completion_rate(self, user_id: int, start_time: datetime, end_time: datetime) -> float:
        """计算任务完成率"""
        total_tasks = self.db.query(func.count(LearningTask.id)).filter(
            LearningTask.user_id == user_id,
            LearningTask.created_at >= start_time,
            LearningTask.created_at <= end_time
        ).scalar() or 0
        
        completed_tasks = self.db.query(func.count(LearningTask.id)).filter(
            LearningTask.user_id == user_id,
            LearningTask.created_at >= start_time,
            LearningTask.created_at <= end_time,
            LearningTask.status == "completed"
        ).scalar() or 0
        
        return round((completed_tasks / total_tasks * 100) if total_tasks > 0 else 0, 1)
    
    def _generate_default_report(self, user_id: int) -> Dict[str, Any]:
        """生成默认报告"""
        return {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "user_name": "用户",
            "today_summary": {
                "study_time_minutes": 0,
                "study_time_hours": 0,
                "questions_answered": 0,
                "average_score": 0,
                "completion_rate": 0
            },
            "weekly_trends": {
                "daily_data": [],
                "total_study_time": 0,
                "total_questions": 0,
                "avg_daily_study_time": 0,
                "avg_daily_questions": 0
            },
            "subject_performance": [],
            "learning_suggestions": ["建议开始学习，建立良好的学习习惯"],
            "growth_curve": {
                "daily_data": [],
                "total_study_time": 0,
                "total_questions": 0,
                "growth_rate": {"study_time": 0, "questions": 0}
            },
            "achievements": [],
            "next_day_tasks": []
        } 