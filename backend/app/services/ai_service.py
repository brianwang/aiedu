import json
import logging
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.question import Question, QuestionCategory
from app.models.user import User, StudySession, WrongQuestion
from config import settings

logger = logging.getLogger(__name__)


class AIService:
    def __init__(self):
        self.openai_api_key = settings.openai_api_key

    async def generate_questions(self, subject: str, difficulty: int, count: int = 10) -> List[Dict]:
        """AI生成题目"""
        try:
            # 这里可以集成OpenAI API来生成题目
            # 目前返回模拟数据
            questions = []
            for i in range(count):
                question = {
                    "content": f"这是{subject}的第{i+1}道题目，难度等级为{difficulty}",
                    "question_type": "single_choice",
                    "options": ["选项A", "选项B", "选项C", "选项D"],
                    "answer": "选项A",
                    "explanation": "这是题目的详细解析",
                    "difficulty": difficulty
                }
                questions.append(question)
            return questions
        except Exception as e:
            logger.error(f"生成题目失败: {e}")
            return []

    async def recommend_questions(self, db: Session, user_id: int, subject: str = None, count: int = 10) -> List[Question]:
        """智能推荐题目"""
        try:
            # 获取用户的学习历史
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                return []

            # 获取用户的错题
            wrong_questions = db.query(WrongQuestion).filter(
                WrongQuestion.user_id == user_id,
                WrongQuestion.is_reviewed == False
            ).all()

            # 获取用户的学习水平
            study_level = user.study_level

            # 根据学习水平推荐题目
            difficulty_map = {
                "beginner": [1, 2],
                "intermediate": [2, 3, 4],
                "advanced": [3, 4, 5]
            }

            difficulties = difficulty_map.get(study_level, [1, 2, 3])

            # 构建查询
            query = db.query(Question)

            if subject:
                query = query.join(QuestionCategory).filter(
                    QuestionCategory.name == subject)

            query = query.filter(Question.difficulty.in_(difficulties))

            # 优先推荐错题
            if wrong_questions:
                wrong_question_ids = [wq.question_id for wq in wrong_questions]
                recommended = query.filter(Question.id.in_(
                    wrong_question_ids)).limit(count // 2).all()
                remaining_count = count - len(recommended)

                if remaining_count > 0:
                    # 推荐新题目
                    new_questions = query.filter(~Question.id.in_(
                        wrong_question_ids)).limit(remaining_count).all()
                    recommended.extend(new_questions)

                return recommended
            else:
                # 没有错题，推荐新题目
                return query.limit(count).all()

        except Exception as e:
            logger.error(f"推荐题目失败: {e}")
            return []

    async def create_study_plan(self, db: Session, user_id: int) -> Dict:
        """创建个性化学习计划"""
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                return {}

            # 分析用户的学习数据
            study_sessions = db.query(StudySession).filter(
                StudySession.user_id == user_id,
                StudySession.start_time >= datetime.utcnow() - timedelta(days=30)
            ).all()

            # 计算学习统计
            total_study_time = sum(
                session.duration_minutes for session in study_sessions)
            total_questions = sum(
                session.questions_answered for session in study_sessions)
            total_correct = sum(
                session.correct_answers for session in study_sessions)

            accuracy = (total_correct / total_questions *
                        100) if total_questions > 0 else 0

            # 获取错题统计
            wrong_questions = db.query(WrongQuestion).filter(
                WrongQuestion.user_id == user_id,
                WrongQuestion.is_reviewed == False
            ).all()

            # 创建学习计划
            study_plan = {
                "user_id": user_id,
                "study_level": user.study_level,
                "daily_goal": {
                    "questions": 20,
                    "study_time": 60,  # 分钟
                    "accuracy_target": 80
                },
                "weekly_goals": {
                    "total_questions": 140,
                    "total_study_time": 420,
                    "review_wrong_questions": len(wrong_questions)
                },
                "recommendations": {
                    "focus_subjects": self._get_focus_subjects(db, user_id),
                    "difficulty_adjustment": self._get_difficulty_adjustment(accuracy),
                    "study_schedule": self._get_study_schedule(user.study_level)
                },
                "progress_summary": {
                    "total_study_time": total_study_time,
                    "total_questions": total_questions,
                    "accuracy": round(accuracy, 2),
                    "wrong_questions_count": len(wrong_questions)
                }
            }

            return study_plan

        except Exception as e:
            logger.error(f"创建学习计划失败: {e}")
            return {}

    def _get_focus_subjects(self, db: Session, user_id: int) -> List[str]:
        """获取需要重点关注的学科"""
        # 分析用户在各学科的错题数量
        wrong_questions = db.query(WrongQuestion).filter(
            WrongQuestion.user_id == user_id
        ).join(Question).join(QuestionCategory).all()

        subject_errors = {}
        for wq in wrong_questions:
            subject = wq.question.category.name
            subject_errors[subject] = subject_errors.get(subject, 0) + 1

        # 返回错题最多的前3个学科
        sorted_subjects = sorted(
            subject_errors.items(), key=lambda x: x[1], reverse=True)
        return [subject for subject, _ in sorted_subjects[:3]]

    def _get_difficulty_adjustment(self, accuracy: float) -> str:
        """根据正确率调整难度建议"""
        if accuracy >= 90:
            return "increase"
        elif accuracy <= 60:
            return "decrease"
        else:
            return "maintain"

    def _get_study_schedule(self, study_level: str) -> Dict:
        """获取学习时间安排建议"""
        schedules = {
            "beginner": {
                "daily_study_time": 30,
                "sessions_per_day": 2,
                "break_time": 15
            },
            "intermediate": {
                "daily_study_time": 60,
                "sessions_per_day": 3,
                "break_time": 20
            },
            "advanced": {
                "daily_study_time": 90,
                "sessions_per_day": 4,
                "break_time": 25
            }
        }
        return schedules.get(study_level, schedules["beginner"])

    async def analyze_learning_pattern(self, db: Session, user_id: int) -> Dict:
        """分析学习模式"""
        try:
            # 获取学习会话数据
            sessions = db.query(StudySession).filter(
                StudySession.user_id == user_id,
                StudySession.start_time >= datetime.utcnow() - timedelta(days=30)
            ).all()

            if not sessions:
                return {"message": "暂无学习数据"}

            # 分析学习时间分布
            time_distribution = {}
            for session in sessions:
                hour = session.start_time.hour
                time_distribution[hour] = time_distribution.get(
                    hour, 0) + session.duration_minutes

            # 分析学科偏好
            subject_preference = {}
            for session in sessions:
                subject = session.subject
                subject_preference[subject] = subject_preference.get(
                    subject, 0) + session.duration_minutes

            # 计算学习效率
            total_time = sum(session.duration_minutes for session in sessions)
            total_questions = sum(
                session.questions_answered for session in sessions)
            efficiency = total_questions / total_time if total_time > 0 else 0

            return {
                "time_distribution": time_distribution,
                "subject_preference": subject_preference,
                "learning_efficiency": round(efficiency, 2),
                "total_study_sessions": len(sessions),
                "average_session_duration": round(total_time / len(sessions), 2)
            }

        except Exception as e:
            logger.error(f"分析学习模式失败: {e}")
            return {}
