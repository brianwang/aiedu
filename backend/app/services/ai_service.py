import json
import logging
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.question import Question, QuestionCategory
from app.models.user import User, StudySession, WrongQuestion
from config import settings
import os
import asyncio
from functools import wraps

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

logger = logging.getLogger(__name__)


def ai_fallback(func):
    """AI服务降级装饰器"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            logger.warning(f"AI服务调用失败，使用降级方案: {e}")
            # 调用对应的降级方法
            fallback_method_name = f"_generate_default_{func.__name__.replace('async_', '')}"
            if hasattr(args[0], fallback_method_name):
                fallback_method = getattr(args[0], fallback_method_name)
                if asyncio.iscoroutinefunction(fallback_method):
                    return await fallback_method(*args[1:], **kwargs)
                else:
                    return fallback_method(*args[1:], **kwargs)
            else:
                logger.error(f"未找到降级方法: {fallback_method_name}")
                raise e
    return wrapper


class AIService:
    def __init__(self):
        self.openai_api_key = settings.openai_api_key
        self.deepseek_api_key = getattr(settings, 'deepseek_api_key', None)
        self.deepseek_base_url = getattr(settings, 'deepseek_base_url', 'https://api.deepseek.com')
        self.deepseek_model = getattr(settings, 'deepseek_model', 'deepseek-chat')
        self._client = None
        self._ai_available = False
        
        # 初始化AI客户端
        self._init_ai_client()
    
    def _init_ai_client(self):
        """初始化AI客户端"""
        try:
            if OpenAI and (self.deepseek_api_key or self.openai_api_key):
                if self.deepseek_api_key:
                    self._client = OpenAI(api_key=self.deepseek_api_key, base_url=self.deepseek_base_url)
                    logger.info("DeepSeek AI客户端初始化成功")
                elif self.openai_api_key:
                    self._client = OpenAI(api_key=self.openai_api_key)
                    logger.info("OpenAI客户端初始化成功")
                self._ai_available = True
            else:
                logger.warning("未配置AI API Key，将使用本地模拟数据")
                self._ai_available = False
        except Exception as e:
            logger.error(f"AI客户端初始化失败: {e}")
            self._ai_available = False
    
    async def _call_ai_api(self, prompt: str, system_prompt: Optional[str] = None, max_retries: int = 3) -> Optional[str]:
        """调用AI API的通用方法"""
        if not self._ai_available or not self._client:
            return None
        
        for attempt in range(max_retries):
            try:
                messages = []
                if system_prompt:
                    messages.append({"role": "system", "content": system_prompt})
                messages.append({"role": "user", "content": prompt})
                
                response = self._client.chat.completions.create(
                    model=self.deepseek_model,
                    messages=messages,
                    stream=False,
                    timeout=30  # 30秒超时
                )
                
                content = response.choices[0].message.content
                if content:
                    logger.info(f"AI API调用成功 (尝试 {attempt + 1})")
                    return content
                    
            except Exception as e:
                logger.warning(f"AI API调用失败 (尝试 {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(1)  # 重试前等待1秒
                continue
        
        logger.error("AI API调用失败，已达到最大重试次数")
        return None

    @ai_fallback
    async def generate_questions(self, subject: str, difficulty: int, count: int = 10) -> List[Dict]:
        """AI生成题目，优先使用deepseek大模型"""
        prompt = f"""
        请为学科：{subject}，难度等级：{difficulty}，生成{count}道题目。
        
        要求：
        1. 题目类型包括：单选题、多选题、填空题、简答题
        2. 难度等级{difficulty}对应：1=基础，2=简单，3=中等，4=困难，5=专家
        3. 每道题目包含：content(题目内容)、question_type(题目类型)、options(选项，仅选择题)、answer(答案)、explanation(解析)、difficulty(难度)
        4. 返回JSON数组格式
        
        示例格式：
        [
            {{
                "content": "题目内容",
                "question_type": "single_choice",
                "options": ["A", "B", "C", "D"],
                "answer": "A",
                "explanation": "详细解析",
                "difficulty": {difficulty}
            }}
        ]
        """
        
        system_prompt = "你是一个专业的教育AI出题助手，请严格按照要求生成题目，确保题目质量和教育价值。"
        
        content = await self._call_ai_api(prompt, system_prompt)
        if content:
            try:
                questions = json.loads(content)
                if isinstance(questions, list) and len(questions) > 0:
                    return questions
            except json.JSONDecodeError as e:
                logger.warning(f"AI返回的JSON解析失败: {e}")
        
        # 降级为模拟数据
        return self._generate_default_questions(subject, difficulty, count)
    
    def _generate_default_questions(self, subject: str, difficulty: int, count: int) -> List[Dict]:
        """生成默认题目（降级方案）"""
        questions = []
        question_types = ["single_choice", "multiple_choice", "fill_blank", "short_answer"]
        
        for i in range(count):
            question_type = question_types[i % len(question_types)]
            question = {
                "content": f"这是{subject}的第{i+1}道题目，难度等级为{difficulty}。请根据题目要求作答。",
                "question_type": question_type,
                "options": ["选项A", "选项B", "选项C", "选项D"] if "choice" in question_type else [],
                "answer": "选项A" if question_type == "single_choice" else "正确答案",
                "explanation": f"这是第{i+1}道题目的详细解析，主要考察{subject}的相关知识点。",
                "difficulty": difficulty
            }
            questions.append(question)
        
        return questions

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
                WrongQuestion.is_reviewed.is_(False)
            ).all()

            # 获取用户的学习水平
            study_level = str(user.study_level) if user.study_level else "beginner"

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
                "study_level": str(user.study_level) if user.study_level else "beginner",
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
                    "difficulty_adjustment": self._get_difficulty_adjustment(float(accuracy)),
                    "study_schedule": self._get_study_schedule(str(user.study_level) if user.study_level else "beginner")
                },
                "progress_summary": {
                    "total_study_time": total_study_time,
                    "total_questions": total_questions,
                    "accuracy": round(float(accuracy), 2),
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

    @ai_fallback
    async def smart_grading(self, question_content: str, standard_answer: str, 
                           student_answer: str, question_type: str, max_score: int) -> Dict:
        """智能评分，使用deepseek大模型"""
        prompt = f"""
        请对以下题目进行专业的智能评分分析：
        
        【题目信息】
        题目内容：{question_content}
        题目类型：{question_type}
        满分：{max_score}分
        
        【答案对比】
        标准答案：{standard_answer}
        学生答案：{student_answer}
        
        【评分要求】
        请从以下维度进行详细评分：
        1. 内容准确性（40%）：答案内容的正确程度
        2. 逻辑完整性（25%）：解题思路和逻辑的完整性
        3. 表达规范性（20%）：语言表达和格式规范性
        4. 创新思维（15%）：解题方法的创新性和灵活性
        
        【输出格式】
        请返回JSON格式的详细评分结果，包含：
        {{
            "score": 得分（整数，0-{max_score}）,
            "accuracy_score": 内容准确性得分（0-100）,
            "logic_score": 逻辑完整性得分（0-100）,
            "expression_score": 表达规范性得分（0-100）,
            "creativity_score": 创新思维得分（0-100）,
            "overall_accuracy": 总体准确度百分比（0-100）,
            "detailed_feedback": {{
                "strengths": ["优点1", "优点2"],
                "weaknesses": ["不足1", "不足2"],
                "specific_errors": ["具体错误1", "具体错误2"],
                "improvement_suggestions": ["改进建议1", "改进建议2"]
            }},
            "learning_insights": {{
                "knowledge_gaps": ["知识盲点1", "知识盲点2"],
                "skill_development": ["技能提升建议1", "技能提升建议2"],
                "next_steps": ["下一步学习重点1", "下一步学习重点2"]
            }},
            "encouragement": "个性化鼓励话语"
        }}
        
        请确保评分客观公正，反馈具体详细，建议具有可操作性。
        """
        
        system_prompt = """你是一个专业的教育AI评分专家，具有丰富的教学经验。
        
        评分原则：
        1. 客观公正：基于答案内容进行客观评分，不受主观偏见影响
        2. 鼓励为主：在指出不足的同时，要充分肯定学生的优点和努力
        3. 具体详细：反馈要具体到具体的错误点和改进建议
        4. 教育价值：评分不仅要给出分数，更要帮助学生学习和成长
        5. 个性化：根据学生的答案特点，给出个性化的建议和鼓励
        
        请严格按照要求进行评分，确保输出格式正确。"""
        
        content = await self._call_ai_api(prompt, system_prompt)
        if content:
            try:
                result = json.loads(content)
                if isinstance(result, dict):
                    return result
            except json.JSONDecodeError as e:
                logger.warning(f"AI返回的JSON解析失败: {e}")
        
        # 降级为模拟评分
        return self._calculate_enhanced_similarity_grading(
            question_content, standard_answer, student_answer, 
            question_type, max_score
        )

    def _calculate_enhanced_similarity_grading(self, question_content: str, standard_answer: str, 
                                           student_answer: str, question_type: str, max_score: int) -> Dict:
        """增强的基于相似度的评分（降级方案）"""
        # 计算基础相似度
        similarity = self._calculate_similarity(student_answer, standard_answer)
        
        # 根据题目类型调整评分权重
        if question_type in ["single_choice", "multiple_choice"]:
            # 选择题：主要看答案正确性
            accuracy_score = similarity * 100
            logic_score = 80 if similarity > 0.8 else 60
            expression_score = 90  # 选择题表达相对简单
            creativity_score = 70  # 选择题创新空间有限
        elif question_type == "fill_blank":
            # 填空题：看答案准确性和完整性
            accuracy_score = similarity * 100
            logic_score = 75 if similarity > 0.7 else 50
            expression_score = 85 if len(student_answer.strip()) > 0 else 30
            creativity_score = 60
        elif question_type in ["short_answer", "essay"]:
            # 主观题：需要更全面的评估
            accuracy_score = similarity * 100
            logic_score = 80 if len(student_answer) > len(standard_answer) * 0.5 else 50
            expression_score = 70 if len(student_answer) > 10 else 40
            creativity_score = 75 if len(student_answer) > len(standard_answer) * 0.8 else 50
        else:
            # 默认评分
            accuracy_score = similarity * 100
            logic_score = 70
            expression_score = 75
            creativity_score = 65
        
        # 计算加权总分
        weighted_score = (
            accuracy_score * 0.4 + 
            logic_score * 0.25 + 
            expression_score * 0.2 + 
            creativity_score * 0.15
        )
        
        # 转换为题目满分
        final_score = int((weighted_score / 100) * max_score)
        
        # 生成详细反馈
        strengths = []
        weaknesses = []
        suggestions = []
        
        if accuracy_score > 80:
            strengths.append("答案内容基本正确")
        else:
            weaknesses.append("答案内容需要改进")
            suggestions.append("仔细检查答案的准确性")
        
        if logic_score > 70:
            strengths.append("解题思路清晰")
        else:
            weaknesses.append("解题逻辑需要完善")
            suggestions.append("加强逻辑思维训练")
        
        if expression_score > 70:
            strengths.append("表达较为规范")
        else:
            weaknesses.append("表达需要改进")
            suggestions.append("注意语言表达的规范性")
        
        if not strengths:
            strengths.append("认真完成了答题")
        
        if not weaknesses:
            weaknesses.append("可以进一步提升")
        
        if not suggestions:
            suggestions.append("继续保持学习热情")
        
        # 生成个性化鼓励
        if final_score >= max_score * 0.8:
            encouragement = "太棒了！你的表现非常出色，继续保持这种优秀的状态！"
        elif final_score >= max_score * 0.6:
            encouragement = "很好！你的答案有亮点，继续努力会有更好的表现！"
        else:
            encouragement = "不要灰心！每一次尝试都是进步，相信你很快就能掌握这个知识点！"
        
        return {
            "score": final_score,
            "accuracy_score": round(accuracy_score, 1),
            "logic_score": round(logic_score, 1),
            "expression_score": round(expression_score, 1),
            "creativity_score": round(creativity_score, 1),
            "overall_accuracy": round(similarity * 100, 2),
            "detailed_feedback": {
                "strengths": strengths,
                "weaknesses": weaknesses,
                "specific_errors": ["请检查答案的准确性"] if accuracy_score < 70 else [],
                "improvement_suggestions": suggestions
            },
            "learning_insights": {
                "knowledge_gaps": [f"建议加强{question_type}类型题目的练习"],
                "skill_development": ["提高解题技巧和表达能力"],
                "next_steps": ["多做类似题目巩固知识点"]
            },
            "encouragement": encouragement
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

    @ai_fallback
    async def recommend_learning_path(self, db: Session, user_id: int, target_skill: str) -> Dict:
        """推荐个性化学习路径，使用deepseek大模型"""
        try:
            # 获取用户学习数据
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                return {}
            
            study_sessions = db.query(StudySession).filter(
                StudySession.user_id == user_id
            ).all()
            
            total_study_time = sum(session.duration_minutes for session in study_sessions)
            total_questions = sum(session.questions_answered for session in study_sessions)
            total_correct = sum(session.correct_answers for session in study_sessions)
            accuracy = (total_correct / total_questions * 100) if total_questions > 0 else 0
            
            prompt = f"""
            请为用户推荐学习路径：
            目标技能：{target_skill}
            用户当前水平：{user.study_level or 'beginner'}
            总学习时间：{total_study_time}分钟
            总答题数：{total_questions}
            正确率：{accuracy:.2f}%
            
            请返回JSON格式的学习路径，包含：
            - path_name: 路径名称
            - description: 路径描述
            - stages: 学习阶段数组，每个阶段包含name, duration, goals, resources
            - estimated_time: 预计总时间（小时）
            - difficulty: 难度等级
            """
            
            response = self._client.chat.completions.create(
                model=self.deepseek_model,
                messages=[
                    {"role": "system", "content": "你是一个专业的教育AI学习路径规划师。"},
                    {"role": "user", "content": prompt}
                ],
                stream=False
            )
            
            import json as _json
            content = response.choices[0].message.content
            if content:
                try:
                    result = _json.loads(content)
                    if isinstance(result, dict):
                        return result
                except Exception:
                    pass  # 解析失败则降级为模拟路径
        
            # 未配置deepseek或解析失败，返回模拟学习路径
            return self._generate_default_learning_path(target_skill)
            
        except Exception as e:
            logger.error(f"推荐学习路径失败: {e}")
            return self._generate_default_learning_path(target_skill)
    
    def _generate_default_learning_path(self, target_skill: str) -> Dict:
        """生成默认学习路径（降级方案）"""
        return {
            "path_name": f"{target_skill}学习路径",
            "description": f"系统为您推荐的{target_skill}学习路径",
            "stages": [
                {
                    "name": "基础阶段",
                    "duration": "2周",
                    "goals": ["掌握基础概念", "完成基础练习"],
                    "resources": ["基础教材", "在线课程", "练习题"]
                },
                {
                    "name": "进阶阶段", 
                    "duration": "3周",
                    "goals": ["深入理解原理", "解决复杂问题"],
                    "resources": ["进阶教材", "实战项目", "讨论交流"]
                },
                {
                    "name": "应用阶段",
                    "duration": "2周", 
                    "goals": ["实际应用", "项目实践"],
                    "resources": ["项目实战", "案例分析", "总结反思"]
                }
            ],
            "estimated_time": 40,
            "difficulty": "intermediate"
        }

    @ai_fallback
    async def generate_exam(self, subject: str, difficulty: int, exam_type: str = "comprehensive", 
                           question_distribution: Dict[str, int] = None) -> Dict:
        """AI智能组卷，使用deepseek大模型"""
        if not question_distribution:
            question_distribution = {
                "single_choice": 10,
                "multiple_choice": 5,
                "fill_blank": 5,
                "short_answer": 3,
                "essay": 2
            }
        
        prompt = f"""
        请为{subject}学科生成一套{difficulty}星难度的{exam_type}试卷。
        
        题目分布要求：
        {json.dumps(question_distribution, ensure_ascii=False, indent=2)}
        
        请返回JSON格式的试卷，包含：
        - exam_info: 试卷信息（标题、说明、总分、时长）
        - questions: 题目数组，每题包含content, question_type, options, answer, explanation, difficulty, score
        - answer_sheet: 答案页
        - analysis: 试卷分析
        """
        
        system_prompt = "你是一个专业的教育AI组卷助手，请严格按照要求生成试卷。"
        
        content = await self._call_ai_api(prompt, system_prompt)
        if content:
            try:
                result = json.loads(content)
                if isinstance(result, dict):
                    return result
            except json.JSONDecodeError as e:
                logger.warning(f"AI返回的JSON解析失败: {e}")
        
        # 未配置deepseek或解析失败，返回模拟试卷
        return self._generate_default_exam(subject, difficulty, exam_type, question_distribution)
            
    def _generate_default_exam(self, subject: str, difficulty: int, exam_type: str, 
                              question_distribution: Dict[str, int]) -> Dict:
        """生成默认试卷（降级方案）"""
        total_questions = sum(question_distribution.values())
        total_score = total_questions * 10  # 每题10分
        
        questions = []
        question_id = 1
        
        for question_type, count in question_distribution.items():
            for i in range(count):
                question = {
                    "id": question_id,
                    "content": f"这是{subject}的第{question_id}道{question_type}题目，难度等级为{difficulty}",
                    "question_type": question_type,
                    "options": ["选项A", "选项B", "选项C", "选项D"] if question_type in ["single_choice", "multiple_choice"] else None,
                    "answer": "选项A" if question_type in ["single_choice", "multiple_choice"] else "标准答案",
                    "explanation": f"这是第{question_id}题的详细解析",
                    "difficulty": difficulty,
                    "score": 10
                }
                questions.append(question)
                question_id += 1
        
        return {
            "exam_info": {
                "title": f"{subject}{exam_type}试卷",
                "subject": subject,
                "difficulty": difficulty,
                "exam_type": exam_type,
                "total_questions": total_questions,
                "total_score": total_score,
                "duration": 120,  # 分钟
                "description": f"本试卷包含{total_questions}道题目，总分{total_score}分，考试时长120分钟。"
            },
            "questions": questions,
            "answer_sheet": {
                "title": f"{subject}{exam_type}试卷答案",
                "answers": [{"question_id": q["id"], "answer": q["answer"]} for q in questions]
            },
            "analysis": {
                "difficulty_distribution": f"难度{difficulty}星",
                "question_type_distribution": question_distribution,
                "estimated_completion_time": "90-120分钟",
                "target_audience": "适合该学科学习水平的学生"
            }
        }

    @ai_fallback
    async def generate_learning_report(self, user_id: int, db: Session) -> Dict:
        """生成学习分析报告"""
        # 获取用户学习数据
        learning_data = await self._get_user_learning_data(user_id, db)
        
        prompt = f"""
        基于以下学习数据，生成详细的学习分析报告：
        
        学习数据：
        {json.dumps(learning_data, ensure_ascii=False, indent=2)}
        
        请返回JSON格式的分析报告，包含：
        - overall_performance: 整体表现（总分、平均分、学习时长等）
        - subject_analysis: 各学科详细分析
        - learning_patterns: 学习模式分析
        - strengths_weaknesses: 优势劣势分析
        - recommendations: 个性化建议
        - improvement_plan: 改进计划
        - progress_trend: 进步趋势
        """
        
        system_prompt = "你是一个专业的教育数据分析师，请基于学习数据生成详细的分析报告。"
        
        content = await self._call_ai_api(prompt, system_prompt)
        if content:
            try:
                result = json.loads(content)
                if isinstance(result, dict):
                    return result
            except json.JSONDecodeError as e:
                logger.warning(f"AI返回的JSON解析失败: {e}")
        
        # 未配置deepseek或解析失败，返回模拟报告
        return await self._generate_default_learning_report(user_id, db)
    
    async def _get_user_learning_data(self, user_id: int, db: Session) -> Dict:
        """获取用户学习数据"""
        try:
            # 获取学习记录
            learning_records = db.query(StudySession).filter(
                StudySession.user_id == user_id
            ).all()
            
            # 获取考试记录
            exam_results = db.query(StudySession).filter(
                StudySession.user_id == user_id
            ).all()
            
            # 获取题目练习记录
            question_records = db.query(StudySession).filter(
                StudySession.user_id == user_id
            ).all()
            
            # 计算统计数据
            total_study_time = sum(session.duration_minutes for session in learning_records)
            total_questions = sum(session.questions_answered for session in question_records)
            correct_answers = sum(session.correct_answers for session in question_records)
            accuracy_rate = (correct_answers / total_questions * 100) if total_questions > 0 else 0
            
            # 按学科分组
            subject_stats = {}
            for record in question_records:
                subject = record.subject
                if subject not in subject_stats:
                    subject_stats[subject] = {
                        "total": 0,
                        "correct": 0,
                        "study_time": 0
                    }
                subject_stats[subject]["total"] += 1
                if record.correct_answers > 0: # Assuming correct_answers is the number of correct answers in a session
                    subject_stats[subject]["correct"] += record.correct_answers
            
            # 添加学习时间
            for record in learning_records:
                subject = record.subject
                if subject in subject_stats:
                    subject_stats[subject]["study_time"] += record.duration_minutes
            
            return {
                "user_id": user_id,
                "total_study_time": total_study_time,
                "total_questions": total_questions,
                "correct_answers": correct_answers,
                "accuracy_rate": round(accuracy_rate, 2),
                "subject_stats": subject_stats,
                "learning_records_count": len(learning_records),
                "exam_results_count": len(exam_results),
                "question_records_count": len(question_records)
            }
            
        except Exception as e:
            logger.error(f"获取用户学习数据失败: {e}")
            return {}
    
    async def _generate_default_learning_report(self, user_id: int, db: Session) -> Dict:
        """生成默认学习报告（降级方案）"""
        learning_data = await self._get_user_learning_data(user_id, db)
        
        # 计算效率分数
        efficiency_score = min(100, learning_data.get("accuracy_rate", 0) * 0.7 + 
                             min(learning_data.get("total_study_time", 0) / 100, 30))
        
        # 生成学科表现
        subject_performance = []
        for subject, stats in learning_data.get("subject_stats", {}).items():
            accuracy = (stats["correct"] / stats["total"] * 100) if stats["total"] > 0 else 0
            subject_performance.append({
                "name": subject,
                "score": round(accuracy, 1),
                "total_questions": stats["total"],
                "correct_questions": stats["correct"],
                "study_time": stats["study_time"]
            })
        
        # 生成建议
        suggestions = []
        if learning_data.get("accuracy_rate", 0) < 70:
            suggestions.append("建议加强基础知识的巩固，多做基础题目练习")
        if learning_data.get("total_study_time", 0) < 50:
            suggestions.append("建议增加学习时间，保持每天的学习习惯")
        if len(subject_performance) > 0:
            weak_subject = min(subject_performance, key=lambda x: x["score"])
            suggestions.append(f"建议重点加强{weak_subject['name']}的学习，当前正确率较低")
        
        if not suggestions:
            suggestions.append("学习表现良好，建议继续保持当前的学习节奏")
        
        return {
            "overall_performance": {
                "total_study_time": learning_data.get("total_study_time", 0),
                "total_questions": learning_data.get("total_questions", 0),
                "accuracy_rate": learning_data.get("accuracy_rate", 0),
                "efficiency_score": round(efficiency_score, 1),
                "learning_days": learning_data.get("learning_records_count", 0)
            },
            "subject_analysis": subject_performance,
            "learning_patterns": {
                "preferred_subjects": [s["name"] for s in sorted(subject_performance, key=lambda x: x["score"], reverse=True)[:3]],
                "study_consistency": "良好" if learning_data.get("learning_records_count", 0) > 10 else "需要改进",
                "accuracy_trend": "稳定" if learning_data.get("accuracy_rate", 0) > 70 else "波动"
            },
            "strengths_weaknesses": {
                "strengths": [s["name"] for s in subject_performance if s["score"] > 80],
                "weaknesses": [s["name"] for s in subject_performance if s["score"] < 60],
                "improvement_areas": [s["name"] for s in subject_performance if 60 <= s["score"] <= 80]
            },
            "recommendations": suggestions,
            "improvement_plan": {
                "short_term": "每天保持1-2小时的学习时间，重点练习薄弱学科",
                "medium_term": "制定每周学习计划，定期复习和总结",
                "long_term": "建立系统的知识体系，提高解题能力"
            },
            "progress_trend": {
                "trend": "上升" if learning_data.get("accuracy_rate", 0) > 70 else "稳定",
                "confidence": "高" if learning_data.get("total_questions", 0) > 50 else "中",
                "next_goal": f"将平均正确率提升到{min(90, learning_data.get('accuracy_rate', 0) + 10)}%"
            }
        }

    @ai_fallback
    async def analyze_wrong_question(self, question_content: str, user_answer: str, 
                                   correct_answer: str, subject: str) -> Dict:
        """AI错题分析讲解"""
        prompt = f"""
        请对以下错题进行深入分析和个性化讲解：
        
        【题目信息】
        题目：{question_content}
        学科：{subject}
        
        【答案对比】
        正确答案：{correct_answer}
        学生答案：{user_answer}
        
        【分析要求】
        请从以下维度进行详细分析：
        
        1. 错误诊断：
           - 错误类型识别（概念错误、计算错误、审题错误、表达错误等）
           - 错误原因分析（知识盲点、思维误区、粗心大意等）
           - 错误严重程度评估
        
        2. 解题指导：
           - 正确的解题思路和步骤
           - 关键知识点梳理
           - 解题技巧和方法
        
        3. 学习建议：
           - 针对性的学习重点
           - 类似题目的练习建议
           - 避免同类错误的方法
        
        4. 个性化鼓励：
           - 基于学生答案特点的鼓励
           - 学习信心建设
        
        【输出格式】
        请返回JSON格式的详细分析结果，包含：
        {{
            "error_analysis": {{
                "error_type": "错误类型",
                "error_severity": "错误严重程度（轻微/中等/严重）",
                "root_cause": "根本原因分析",
                "common_mistakes": ["常见错误1", "常见错误2"],
                "misconceptions": ["错误认知1", "错误认知2"]
            }},
            "correct_solution": {{
                "step_by_step": ["步骤1", "步骤2", "步骤3"],
                "key_concepts": ["关键概念1", "关键概念2"],
                "solution_tips": ["解题技巧1", "解题技巧2"],
                "detailed_explanation": "详细解题过程"
            }},
            "knowledge_points": {{
                "core_concepts": ["核心概念1", "核心概念2"],
                "related_topics": ["相关知识点1", "相关知识点2"],
                "prerequisites": ["前置知识1", "前置知识2"]
            }},
            "learning_guidance": {{
                "focus_areas": ["重点学习领域1", "重点学习领域2"],
                "practice_suggestions": ["练习建议1", "练习建议2"],
                "avoidance_strategies": ["避免错误策略1", "避免错误策略2"],
                "skill_development": ["技能提升建议1", "技能提升建议2"]
            }},
            "similar_questions": {{
                "question_types": ["类似题型1", "类似题型2"],
                "practice_recommendations": ["练习推荐1", "练习推荐2"],
                "difficulty_progression": "难度递进建议"
            }},
            "personalized_encouragement": {{
                "positive_aspects": ["积极方面1", "积极方面2"],
                "confidence_building": "信心建设话语",
                "motivation_message": "个性化激励信息"
            }},
            "difficulty_assessment": {{
                "question_difficulty": "题目难度等级",
                "student_readiness": "学生准备程度",
                "recommended_approach": "建议学习方法"
            }},
            "improvement_plan": {{
                "immediate_actions": ["立即行动1", "立即行动2"],
                "short_term_goals": ["短期目标1", "短期目标2"],
                "long_term_development": ["长期发展建议1", "长期发展建议2"]
            }}
        }}
        
        请确保分析深入透彻，建议具体可行，鼓励积极正面。
        """
        
        system_prompt = """你是一个专业的教育AI导师，具有丰富的教学经验和心理学背景。
        
        分析原则：
        1. 诊断精准：准确识别错误类型和根本原因
        2. 指导具体：提供可操作的解题步骤和学习建议
        3. 鼓励为主：在指出问题的同时，充分肯定学生的努力和进步
        4. 个性化：根据学生的具体错误，给出针对性的建议
        5. 系统性：从知识点、解题技巧、学习策略等多角度进行分析
        6. 发展性：不仅解决当前问题，更要帮助学生建立长期学习能力
        
        请严格按照要求进行分析，确保输出格式正确，内容具有教育价值。"""
        
        content = await self._call_ai_api(prompt, system_prompt)
        if content:
            try:
                result = json.loads(content)
                if isinstance(result, dict):
                    return result
            except json.JSONDecodeError as e:
                logger.warning(f"AI返回的JSON解析失败: {e}")
        
        # 降级为模拟分析
        return self._generate_enhanced_wrong_analysis(question_content, user_answer, correct_answer, subject)
    
    def _generate_enhanced_wrong_analysis(self, question_content: str, user_answer: str, 
                                       correct_answer: str, subject: str) -> Dict:
        """生成增强的错题分析（降级方案）"""
        # 智能错误类型判断
        error_type, error_severity = self._analyze_error_type(user_answer, correct_answer)
        
        # 生成详细分析
        analysis = {
            "error_analysis": {
                "error_type": error_type,
                "error_severity": error_severity,
                "root_cause": f"学生在{subject}学科中出现了{error_type}，主要原因是{self._get_error_cause(error_type)}",
                "common_mistakes": self._get_common_mistakes(error_type, subject),
                "misconceptions": self._get_misconceptions(error_type, subject)
            },
            "correct_solution": {
                "step_by_step": [
                    "仔细审题，理解题目要求",
                    "分析题目涉及的知识点",
                    "制定解题计划",
                    "按照正确的解题思路进行解答",
                    "检查答案的合理性"
                ],
                "key_concepts": [f"{subject}基础知识", "解题技巧", "逻辑思维"],
                "solution_tips": ["画图辅助理解", "分步骤解题", "检查计算过程"],
                "detailed_explanation": f"正确答案是：{correct_answer}。这道题主要考察{subject}的相关知识点，需要学生掌握基本概念和解题方法。"
            },
            "knowledge_points": {
                "core_concepts": [f"{subject}核心概念", "基本定理", "解题方法"],
                "related_topics": [f"{subject}基础知识", "相关公式", "应用技巧"],
                "prerequisites": ["基础数学知识", "逻辑思维能力", "阅读理解能力"]
            },
            "learning_guidance": {
                "focus_areas": [f"加强{subject}基础知识", "提高解题技巧", "培养逻辑思维"],
                "practice_suggestions": ["多做基础题目", "总结解题方法", "建立知识体系"],
                "avoidance_strategies": ["仔细审题", "分步骤解题", "及时检查"],
                "skill_development": ["提高计算能力", "增强理解能力", "培养分析能力"]
            },
            "similar_questions": {
                "question_types": [f"{subject}基础题", f"{subject}应用题", f"{subject}综合题"],
                "practice_recommendations": [f"练习{subject}相关题目", "重点复习相关知识点", "多做同类型题目巩固"],
                "difficulty_progression": "从基础题目开始，逐步提升难度"
            },
            "personalized_encouragement": {
                "positive_aspects": ["认真思考了问题", "尝试了不同的解题方法"],
                "confidence_building": "错误是学习的一部分，每一次尝试都是进步",
                "motivation_message": "不要灰心！通过分析错误，你已经向正确答案迈进了一步。"
            },
            "difficulty_assessment": {
                "question_difficulty": "中等",
                "student_readiness": "需要加强基础",
                "recommended_approach": "从基础概念开始，逐步深入"
            },
            "improvement_plan": {
                "immediate_actions": ["重新学习相关知识点", "多做类似题目练习"],
                "short_term_goals": ["掌握基本概念", "提高解题准确率"],
                "long_term_development": ["建立系统的知识体系", "培养独立解题能力"]
            }
        }
        
        return analysis
    
    def _analyze_error_type(self, user_answer: str, correct_answer: str) -> tuple:
        """分析错误类型和严重程度"""
        if not user_answer or user_answer.strip() == "":
            return "未作答", "严重"
        elif len(user_answer) < len(correct_answer) * 0.3:
            return "答案不完整", "严重"
        elif len(user_answer) < len(correct_answer) * 0.7:
            return "答案不完整", "中等"
        elif user_answer.lower() == correct_answer.lower():
            return "答案正确", "无"
        else:
            # 计算相似度
            similarity = self._calculate_similarity(user_answer, correct_answer)
            if similarity > 0.8:
                return "表达错误", "轻微"
            elif similarity > 0.5:
                return "部分错误", "中等"
            else:
                return "答案错误", "严重"
    
    def _get_error_cause(self, error_type: str) -> str:
        """获取错误原因"""
        causes = {
            "未作答": "对题目理解不够或缺乏解题思路",
            "答案不完整": "解题思路不完整或时间管理不当",
            "表达错误": "语言表达能力需要提升",
            "部分错误": "对知识点理解不够深入",
            "答案错误": "对相关概念理解有误或计算错误"
        }
        return causes.get(error_type, "对知识点理解不够深入")
    
    def _get_common_mistakes(self, error_type: str, subject: str) -> List[str]:
        """获取常见错误"""
        mistakes = {
            "未作答": ["题目理解不清", "缺乏解题思路", "时间管理不当"],
            "答案不完整": ["解题步骤遗漏", "计算过程不完整", "答案表达不充分"],
            "表达错误": ["语言表达不规范", "格式要求不明确", "逻辑表达不清"],
            "部分错误": ["概念理解不准确", "计算过程有误", "审题不够仔细"],
            "答案错误": ["基本概念错误", "解题方法错误", "计算错误"]
        }
        return mistakes.get(error_type, ["概念理解不清", "计算错误", "审题不仔细", "知识点遗漏"])
    
    def _get_misconceptions(self, error_type: str, subject: str) -> List[str]:
        """获取错误认知"""
        misconceptions = {
            "未作答": [f"认为{subject}题目太难", "缺乏解题信心", "不知道从哪里开始"],
            "答案不完整": ["认为部分答案就够了", "时间不够就放弃", "不知道如何完整表达"],
            "表达错误": ["认为答案对就行", "不重视表达规范", "不知道如何清晰表达"],
            "部分错误": [f"对{subject}概念理解有偏差", "解题方法掌握不牢", "粗心大意"],
            "答案错误": [f"对{subject}基本概念理解错误", "解题思路完全错误", "计算能力不足"]
        }
        return misconceptions.get(error_type, [f"对{subject}知识点理解不够深入", "解题技巧需要提升"])

    @ai_fallback
    async def generate_learning_motivation(self, user_id: int, db: Session) -> Dict:
        """生成学习激励信息"""
        # 获取用户学习数据
        learning_data = await self._get_user_learning_data(user_id, db)
        
        prompt = f"""
        基于以下学习数据，生成个性化的学习激励信息：
        
        学习数据：
        {json.dumps(learning_data, ensure_ascii=False, indent=2)}
        
        请返回JSON格式的激励信息，包含：
        - motivation_message: 激励话语
        - achievement_highlight: 成就亮点
        - next_goal: 下一个目标
        - encouragement_tips: 鼓励建议
        - reward_suggestion: 奖励建议
        - progress_celebration: 进步庆祝
        """
        
        system_prompt = "你是一个专业的教育激励专家，请根据学习数据生成积极正面的激励信息。"
        
        content = await self._call_ai_api(prompt, system_prompt)
        if content:
            try:
                result = json.loads(content)
                if isinstance(result, dict):
                    return result
            except json.JSONDecodeError as e:
                logger.warning(f"AI返回的JSON解析失败: {e}")
        
        # 未配置deepseek或解析失败，返回模拟激励
        return await self._generate_default_motivation(user_id, db)
    
    async def _generate_default_motivation(self, user_id: int, db: Session) -> Dict:
        """生成默认学习激励（降级方案）"""
        learning_data = await self._get_user_learning_data(user_id, db)
        
        accuracy_rate = learning_data.get("accuracy_rate", 0)
        total_study_time = learning_data.get("total_study_time", 0)
        total_questions = learning_data.get("total_questions", 0)
        
        # 根据表现生成激励信息
        if accuracy_rate >= 90:
            motivation_level = "优秀"
            motivation_message = "太棒了！你的学习表现非常出色，继续保持这种优秀的状态！"
        elif accuracy_rate >= 80:
            motivation_level = "良好"
            motivation_message = "很好！你的学习表现不错，再努力一点就能达到优秀水平！"
        elif accuracy_rate >= 70:
            motivation_level = "进步"
            motivation_message = "有进步！继续加油，相信你很快就能取得更好的成绩！"
        else:
            motivation_level = "鼓励"
            motivation_message = "不要灰心！每一次努力都是进步，坚持就是胜利！"
        
        # 生成成就亮点
        achievements = []
        if total_questions > 100:
            achievements.append("完成题目数量超过100道")
        if total_study_time > 50:
            achievements.append("累计学习时间超过50小时")
        if accuracy_rate > 80:
            achievements.append("正确率保持在80%以上")
        if learning_data.get("learning_records_count", 0) > 20:
            achievements.append("坚持学习超过20天")
        
        if not achievements:
            achievements.append("开始学习之旅，这是最棒的开始！")
        
        # 生成下一个目标
        next_goals = []
        if accuracy_rate < 90:
            next_goals.append(f"将正确率提升到{min(95, accuracy_rate + 10)}%")
        if total_questions < 200:
            next_goals.append("完成200道题目")
        if total_study_time < 100:
            next_goals.append("累计学习时间达到100小时")
        
        return {
            "motivation_message": motivation_message,
            "motivation_level": motivation_level,
            "achievement_highlight": {
                "achievements": achievements,
                "total_achievements": len(achievements)
            },
            "next_goal": {
                "goals": next_goals,
                "primary_goal": next_goals[0] if next_goals else "保持当前的学习状态"
            },
            "encouragement_tips": [
                "每天保持学习习惯，积少成多",
                "遇到困难不要怕，这是成长的机会",
                "相信自己，你比想象中更优秀",
                "学习是一个过程，享受其中的乐趣"
            ],
            "reward_suggestion": {
                "immediate": "完成今天的任务，给自己一个小奖励",
                "short_term": "达到本周目标，可以做一些喜欢的事情",
                "long_term": "坚持学习一个月，奖励自己一个特别的礼物"
            },
            "progress_celebration": {
                "message": f"恭喜你！已经完成了{total_questions}道题目，学习时间{total_study_time}小时",
                "milestone": f"正确率{accuracy_rate}%，这是一个值得庆祝的成绩！",
                "celebration_ideas": [
                    "和朋友分享你的学习成果",
                    "记录下这个美好的时刻",
                    "给自己一个鼓励的拥抱"
                ]
            },
            "learning_stats": {
                "current_accuracy": accuracy_rate,
                "total_questions": total_questions,
                "study_time": total_study_time,
                "learning_days": learning_data.get("learning_records_count", 0)
            }
        }

    @ai_fallback
    async def identify_learning_style(self, user_id: int, db: Session) -> Dict:
        """识别学习风格"""
        # 获取用户学习数据
        learning_data = await self._get_user_learning_data(user_id, db)
        
        prompt = f"""
        基于以下学习数据，分析用户的学习风格和偏好：
        
        学习数据：
        {json.dumps(learning_data, ensure_ascii=False, indent=2)}
        
        请返回JSON格式的学习风格分析，包含：
        - learning_style: 学习风格类型（视觉型、听觉型、动觉型等）
        - study_preferences: 学习偏好
        - optimal_study_methods: 最佳学习方法
        - learning_environment: 理想学习环境
        - time_preferences: 时间偏好
        - difficulty_preferences: 难度偏好
        - feedback_preferences: 反馈偏好
        """
        
        system_prompt = "你是一个专业的教育心理学家，请基于学习数据识别用户的学习风格。"
        
        content = await self._call_ai_api(prompt, system_prompt)
        if content:
            try:
                result = json.loads(content)
                if isinstance(result, dict):
                    return result
            except json.JSONDecodeError as e:
                logger.warning(f"AI返回的JSON解析失败: {e}")
        
        # 未配置deepseek或解析失败，返回模拟分析
        return await self._generate_default_learning_style(user_id, db)
    
    async def _generate_default_learning_style(self, user_id: int, db: Session) -> Dict:
        """生成默认学习风格分析（降级方案）"""
        learning_data = await self._get_user_learning_data(user_id, db)
        
        # 基于学习数据推断学习风格
        total_study_time = learning_data.get("total_study_time", 0)
        accuracy_rate = learning_data.get("accuracy_rate", 0)
        learning_days = learning_data.get("learning_records_count", 0)
        
        # 学习风格判断逻辑
        if learning_days > 30 and total_study_time > 100:
            learning_style = "持续型学习者"
            style_description = "你是一个有毅力的学习者，能够持续投入时间进行学习"
        elif accuracy_rate > 85:
            learning_style = "高效型学习者"
            style_description = "你的学习效率很高，能够快速掌握知识点"
        elif total_study_time > 50:
            learning_style = "投入型学习者"
            style_description = "你愿意投入大量时间进行学习，有很强的学习动力"
        else:
            learning_style = "探索型学习者"
            style_description = "你正在探索适合自己的学习方式，需要更多指导"
        
        # 学习偏好分析
        study_preferences = []
        if accuracy_rate > 80:
            study_preferences.append("喜欢挑战性题目")
        if learning_days > 20:
            study_preferences.append("习惯规律性学习")
        if total_study_time > 30:
            study_preferences.append("愿意投入时间深入理解")
        
        if not study_preferences:
            study_preferences.append("正在培养学习习惯")
        
        # 最佳学习方法
        optimal_methods = []
        if accuracy_rate > 75:
            optimal_methods.append("实践练习法")
            optimal_methods.append("错题分析法")
        if learning_days > 15:
            optimal_methods.append("定期复习法")
        optimal_methods.append("目标导向法")
        
        return {
            "learning_style": {
                "type": learning_style,
                "description": style_description,
                "confidence": "高" if learning_days > 10 else "中"
            },
            "study_preferences": {
                "preferences": study_preferences,
                "strength_areas": [s for s in study_preferences if "喜欢" in s or "习惯" in s],
                "development_areas": [s for s in study_preferences if "正在" in s]
            },
            "optimal_study_methods": {
                "methods": optimal_methods,
                "recommended_approach": "结合多种方法，找到最适合的学习节奏",
                "effectiveness_rating": "高" if accuracy_rate > 80 else "中"
            },
            "learning_environment": {
                "preferred_setting": "安静专注的环境" if accuracy_rate > 70 else "需要更多指导的环境",
                "optimal_duration": "1-2小时集中学习" if total_study_time > 30 else "短时间多次学习",
                "break_pattern": "每45分钟休息5分钟" if learning_days > 10 else "根据注意力调整"
            },
            "time_preferences": {
                "best_study_time": "上午或晚上" if learning_days > 15 else "需要探索最佳时间",
                "study_frequency": "每天学习" if learning_days > 20 else "每周3-4次",
                "session_length": "1-2小时" if total_study_time > 50 else "30-60分钟"
            },
            "difficulty_preferences": {
                "preferred_level": "中等难度" if 70 <= accuracy_rate <= 90 else "基础难度",
                "challenge_tolerance": "高" if accuracy_rate > 85 else "中",
                "comfort_zone": f"正确率{max(60, accuracy_rate - 10)}%-{min(95, accuracy_rate + 10)}%"
            },
            "feedback_preferences": {
                "immediate_feedback": "需要" if accuracy_rate < 80 else "偶尔需要",
                "detailed_explanation": "希望获得详细解析" if accuracy_rate < 85 else "重点解析即可",
                "progress_tracking": "希望看到学习进度" if learning_days > 5 else "需要建立进度意识"
            },
            "personalized_recommendations": {
                "short_term": "保持当前的学习节奏，继续巩固基础知识",
                "medium_term": "尝试增加学习难度，挑战更高水平的题目",
                "long_term": "建立系统的学习体系，形成自己的学习方法论"
            },
            "learning_metrics": {
                "study_consistency": learning_days,
                "time_investment": total_study_time,
                "accuracy_performance": accuracy_rate,
                "overall_progress": "良好" if accuracy_rate > 70 and learning_days > 10 else "需要改进"
            }
        }
