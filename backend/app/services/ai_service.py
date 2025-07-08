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

    async def smart_grading(self, question_content: str, standard_answer: str, 
                           student_answer: str, question_type: str, max_score: int) -> Dict:
        """智能评分"""
        try:
            # 这里可以集成OpenAI API进行智能评分
            # 目前返回模拟评分结果
            
            # 简单的答案相似度计算
            similarity = self._calculate_similarity(standard_answer, student_answer)
            
            # 根据相似度和题目类型计算分数
            base_score = similarity * max_score
            
            # 根据题目类型调整评分标准
            if question_type == "single_choice":
                score = max_score if similarity > 0.9 else 0
                correctness = 1.0 if similarity > 0.9 else 0.0
            elif question_type == "multiple_choice":
                score = base_score * 0.8
                correctness = similarity
            elif question_type == "fill_blank":
                score = base_score * 0.9
                correctness = similarity
            else:  # short_answer, essay
                score = base_score * 0.7
                correctness = similarity
            
            # 计算其他维度
            logic_completeness = min(1.0, similarity + 0.2)
            expression_standard = min(1.0, similarity + 0.1)
            creativity = min(1.0, (1 - similarity) * 0.5 + 0.3)
            
            # 生成评价
            if score >= max_score * 0.9:
                overall_evaluation = "优秀"
                suggestions = ["答案完全正确，逻辑清晰", "继续保持这种学习状态"]
            elif score >= max_score * 0.7:
                overall_evaluation = "良好"
                suggestions = ["答案基本正确，可以进一步完善", "注意细节的准确性"]
            elif score >= max_score * 0.6:
                overall_evaluation = "中等"
                suggestions = ["答案部分正确，需要加强理解", "建议复习相关知识点"]
            else:
                overall_evaluation = "需要改进"
                suggestions = ["答案有较大偏差，建议重新学习", "可以寻求老师或同学的帮助"]
            
            return {
                "score": round(score, 1),
                "correctness": round(correctness, 2),
                "logic_completeness": round(logic_completeness, 2),
                "expression_standard": round(expression_standard, 2),
                "creativity": round(creativity, 2),
                "overall_evaluation": overall_evaluation,
                "suggestions": suggestions
            }
            
        except Exception as e:
            logger.error(f"智能评分失败: {e}")
            return {
                "score": 0,
                "correctness": 0,
                "logic_completeness": 0,
                "expression_standard": 0,
                "creativity": 0,
                "overall_evaluation": "评分失败",
                "suggestions": ["系统暂时无法评分，请稍后重试"]
            }

    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """计算文本相似度（简化版本）"""
        if not text1 or not text2:
            return 0.0
        
        # 简单的字符匹配相似度
        set1 = set(text1.lower())
        set2 = set(text2.lower())
        
        if not set1 or not set2:
            return 0.0
        
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        
        return intersection / union if union > 0 else 0.0

    async def assess_learning_ability(self, study_time: int, questions_completed: int,
                                    accuracy: float, subjects: List[str], 
                                    wrong_questions_distribution: Dict[str, int]) -> Dict:
        """学习能力评估"""
        try:
            # 计算各项能力分数
            knowledge_mastery = min(10, (accuracy / 100) * 10)
            problem_solving = min(10, (questions_completed / 100) * 8 + 2)
            concentration = min(10, (study_time / 600) * 6 + 4)  # 假设10小时为满分
            knowledge_transfer = min(10, len(subjects) * 2 + 2)
            learning_efficiency = min(10, (questions_completed / study_time * 60) * 5 + 5)
            
            # 计算综合能力
            overall_score = (knowledge_mastery + problem_solving + concentration + 
                           knowledge_transfer + learning_efficiency) / 5
            
            # 确定能力等级
            if overall_score >= 8:
                overall_level = "专家级"
                improvement_suggestions = [
                    "您的能力已经达到很高水平，可以尝试更具挑战性的内容",
                    "建议参与竞赛或项目实践来进一步提升",
                    "可以尝试教授他人来巩固知识"
                ]
            elif overall_score >= 6:
                overall_level = "高级"
                improvement_suggestions = [
                    "继续加强薄弱学科的学习",
                    "尝试更高难度的题目",
                    "建立系统的知识体系"
                ]
            elif overall_score >= 4:
                overall_level = "中级"
                improvement_suggestions = [
                    "加强基础知识的学习",
                    "提高解题技巧和效率",
                    "建立良好的学习习惯"
                ]
            else:
                overall_level = "初级"
                improvement_suggestions = [
                    "从基础题目开始，逐步提升",
                    "建立学习计划，保持学习规律",
                    "寻求老师或同学的帮助"
                ]
            
            return {
                "knowledge_mastery": round(knowledge_mastery, 1),
                "problem_solving": round(problem_solving, 1),
                "concentration": round(concentration, 1),
                "knowledge_transfer": round(knowledge_transfer, 1),
                "learning_efficiency": round(learning_efficiency, 1),
                "overall_level": overall_level,
                "improvement_suggestions": improvement_suggestions
            }
            
        except Exception as e:
            logger.error(f"能力评估失败: {e}")
            return {
                "knowledge_mastery": 0,
                "problem_solving": 0,
                "concentration": 0,
                "knowledge_transfer": 0,
                "learning_efficiency": 0,
                "overall_level": "无法评估",
                "improvement_suggestions": ["系统暂时无法评估，请稍后重试"]
            }

    async def analyze_learning_style(self, time_distribution: Dict[str, int],
                                   question_type_preference: Dict[str, int],
                                   learning_mode: str, review_frequency: int,
                                   wrong_question_handling: str) -> Dict:
        """学习风格分析"""
        try:
            # 分析时间分布偏好
            peak_hours = sorted(time_distribution.items(), key=lambda x: x[1], reverse=True)[:3]
            is_morning_person = any(int(hour) < 12 for hour, _ in peak_hours)
            is_night_person = any(int(hour) >= 20 for hour, _ in peak_hours)
            
            # 分析题目类型偏好
            preferred_type = max(question_type_preference.items(), key=lambda x: x[1])[0]
            
            # 确定学习风格类型
            if preferred_type == "single_choice" and learning_mode == "continuous":
                style_type = "逻辑型学习者"
                characteristics = [
                    "偏好结构化的学习内容",
                    "善于逻辑推理和分析",
                    "喜欢系统性的学习方法"
                ]
                learning_suggestions = [
                    "使用思维导图整理知识",
                    "建立知识体系框架",
                    "多做逻辑推理题"
                ]
                study_methods = [
                    "系统学习法",
                    "逻辑分析法",
                    "框架构建法"
                ]
            elif preferred_type == "multiple_choice" and review_frequency > 3:
                style_type = "复习型学习者"
                characteristics = [
                    "重视知识的巩固和复习",
                    "学习态度认真负责",
                    "善于总结和归纳"
                ]
                learning_suggestions = [
                    "制定复习计划",
                    "使用错题本",
                    "定期回顾学习内容"
                ]
                study_methods = [
                    "间隔重复法",
                    "错题复习法",
                    "总结归纳法"
                ]
            elif is_morning_person and learning_mode == "distributed":
                style_type = "晨型学习者"
                characteristics = [
                    "早晨学习效率最高",
                    "喜欢分散学习",
                    "注意力集中时间较长"
                ]
                learning_suggestions = [
                    "充分利用早晨时间",
                    "合理安排学习间隔",
                    "保持规律作息"
                ]
                study_methods = [
                    "晨间学习法",
                    "分散学习法",
                    "番茄工作法"
                ]
            else:
                style_type = "综合型学习者"
                characteristics = [
                    "学习方式灵活多样",
                    "适应能力强",
                    "学习兴趣广泛"
                ]
                learning_suggestions = [
                    "尝试不同的学习方法",
                    "保持学习的新鲜感",
                    "发挥个人优势"
                ]
                study_methods = [
                    "多样化学习法",
                    "兴趣驱动法",
                    "个性化学习法"
                ]
            
            return {
                "style_type": style_type,
                "characteristics": characteristics,
                "learning_suggestions": learning_suggestions,
                "study_methods": study_methods
            }
            
        except Exception as e:
            logger.error(f"学习风格分析失败: {e}")
            return {
                "style_type": "无法分析",
                "characteristics": ["数据不足，无法分析学习风格"],
                "learning_suggestions": ["建议收集更多学习数据"],
                "study_methods": ["通用学习法"]
            }

    async def get_motivation_plan(self, learning_status: str, learning_difficulties: List[str],
                                learning_goals: List[str], learning_achievements: List[str],
                                personal_characteristics: List[str]) -> Dict:
        """获取学习动机激励方案"""
        try:
            # 根据学习状态生成激励策略
            if learning_status == "struggling":
                achievement_recognition = [
                    "即使遇到困难，您仍然在坚持学习，这很了不起",
                    "每一次尝试都是进步，不要害怕犯错",
                    "学习是一个过程，慢一点没关系"
                ]
                goal_setting = [
                    "设定小目标，逐步实现",
                    "将大目标分解为可执行的小任务",
                    "建立学习里程碑，记录进步"
                ]
                challenge_incentives = [
                    "从简单题目开始，建立信心",
                    "找到学习的乐趣，让学习变得有趣",
                    "与同学一起学习，互相鼓励"
                ]
                emotional_support = [
                    "学习困难是正常的，每个人都会遇到",
                    "相信自己有能力克服困难",
                    "寻求帮助是聪明的表现"
                ]
                encouragement_message = "记住，每一个伟大的成就都始于一个小小的开始。您已经在正确的道路上了！"
                
            elif learning_status == "steady":
                achievement_recognition = [
                    "您的学习态度非常认真",
                    "稳定的学习进度值得表扬",
                    "您的坚持是成功的关键"
                ]
                goal_setting = [
                    "设定更具挑战性的目标",
                    "尝试新的学习方法",
                    "探索更深入的知识领域"
                ]
                challenge_incentives = [
                    "尝试更高难度的题目",
                    "参与学习竞赛或项目",
                    "挑战自己的学习极限"
                ]
                emotional_support = [
                    "保持这种积极的学习状态",
                    "您的努力一定会得到回报",
                    "继续前进，成功就在前方"
                ]
                encouragement_message = "您的学习状态很好！继续保持这种节奏，成功就在不远处。"
                
            else:  # excellent
                achievement_recognition = [
                    "您的表现非常优秀！",
                    "您的学习能力令人印象深刻",
                    "您已经达到了很高的水平"
                ]
                goal_setting = [
                    "设定更具挑战性的目标",
                    "尝试跨学科学习",
                    "参与高级学习项目"
                ]
                challenge_incentives = [
                    "尝试最难的题目",
                    "参与学术竞赛",
                    "指导其他同学学习"
                ]
                emotional_support = [
                    "您的优秀表现值得骄傲",
                    "继续保持这种高水平",
                    "您已经成为学习的榜样"
                ]
                encouragement_message = "您已经达到了很高的水平！继续保持这种优秀的表现，您将成为真正的学习专家！"
            
            return {
                "achievement_recognition": achievement_recognition,
                "goal_setting": goal_setting,
                "challenge_incentives": challenge_incentives,
                "emotional_support": emotional_support,
                "encouragement_message": encouragement_message
            }
            
        except Exception as e:
            logger.error(f"生成激励方案失败: {e}")
            return {
                "achievement_recognition": ["您在学习中表现很好"],
                "goal_setting": ["继续设定学习目标"],
                "challenge_incentives": ["尝试新的挑战"],
                "emotional_support": ["相信自己"],
                "encouragement_message": "继续努力，您一定会成功！"
            }
