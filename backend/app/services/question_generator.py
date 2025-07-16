import asyncio
import logging
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models.question import Question
from app.models.user import User
from app.models.learning import UserProfile, LearningProgress
from app.services.ai_service import AIService
from datetime import datetime, timedelta
import json

logger = logging.getLogger(__name__)


class QuestionGenerator:
    def __init__(self, db: Session):
        self.db = db
        self.ai_service = AIService()
    
    async def generate_questions_for_user(self, user_id: int, subject: str, count: int = 10) -> List[Dict]:
        """为用户生成个性化题目"""
        try:
            # 获取用户画像和学习历史
            user_profile = self.db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
            learning_history = self.db.query(LearningProgress).filter(
                LearningProgress.user_id == user_id
            ).order_by(LearningProgress.created_at.desc()).limit(50).all()
            
            # 分析用户学习偏好和薄弱点
            user_analysis = self._analyze_user_learning_pattern(user_profile, learning_history)
            
            # 生成题目
            questions = await self._generate_questions_by_ai(subject, user_analysis, count)
            
            # 保存到数据库
            saved_questions = []
            for q_data in questions:
                question = Question(
                    title=q_data["title"],
                    content=q_data["content"],
                    answer=q_data["answer"],
                    explanation=q_data["explanation"],
                    subject=subject,
                    difficulty=q_data["difficulty"],
                    question_type=q_data["type"],
                    options=json.dumps(q_data.get("options", []), ensure_ascii=False),
                    tags=json.dumps(q_data.get("tags", []), ensure_ascii=False),
                    created_by=user_id
                )
                self.db.add(question)
                saved_questions.append(question)
            
            self.db.commit()
            logger.info(f"为用户 {user_id} 生成了 {len(saved_questions)} 道 {subject} 题目")
            
            return [{"id": q.id, "title": q.title, "difficulty": q.difficulty} for q in saved_questions]
            
        except Exception as e:
            logger.error(f"生成题目失败: {str(e)}")
            self.db.rollback()
            return []
    
    def _analyze_user_learning_pattern(self, user_profile: UserProfile, learning_history: List[LearningProgress]) -> Dict:
        """分析用户学习模式"""
        analysis = {
            "learning_style": "visual",  # 默认视觉型
            "preferred_difficulty": "medium",
            "weak_areas": [],
            "strong_areas": [],
            "study_frequency": "regular"
        }
        
        if user_profile:
            analysis["learning_style"] = user_profile.learning_style or "visual"
            analysis["preferred_difficulty"] = user_profile.preferred_difficulty or "medium"
        
        # 分析学习历史
        if learning_history:
            # 分析学习频率
            recent_sessions = [h for h in learning_history if h.created_at > datetime.now() - timedelta(days=7)]
            if len(recent_sessions) >= 5:
                analysis["study_frequency"] = "high"
            elif len(recent_sessions) >= 2:
                analysis["study_frequency"] = "regular"
            else:
                analysis["study_frequency"] = "low"
        
        return analysis
    
    async def _generate_questions_by_ai(self, subject: str, user_analysis: Dict, count: int) -> List[Dict]:
        """使用AI生成题目"""
        try:
            # 构建AI提示词
            prompt = self._build_question_generation_prompt(subject, user_analysis, count)
            
            # 调用AI服务
            response = await self.ai_service._call_ai_api(prompt)
            
            # 解析AI响应
            if response:
                questions = self._parse_ai_response(response, count)
            else:
                questions = self._generate_mock_questions(subject, count)
            
            return questions
            
        except Exception as e:
            logger.error(f"AI生成题目失败: {str(e)}")
            # 返回模拟数据
            return self._generate_mock_questions(subject, count)
    
    def _build_question_generation_prompt(self, subject: str, user_analysis: Dict, count: int) -> str:
        """构建题目生成提示词"""
        prompt = f"""
请为{subject}科目生成{count}道高质量的题目，要求：

1. 用户学习风格：{user_analysis['learning_style']}
2. 偏好难度：{user_analysis['preferred_difficulty']}
3. 学习频率：{user_analysis['study_frequency']}

题目要求：
- 包含选择题、填空题、简答题等多种类型
- 难度分布合理，符合用户水平
- 内容贴近实际应用
- 提供详细解析

请以JSON格式返回，格式如下：
{{
    "questions": [
        {{
            "title": "题目标题",
            "content": "题目内容",
            "type": "choice|fill|essay",
            "options": ["A", "B", "C", "D"],
            "answer": "正确答案",
            "explanation": "详细解析",
            "difficulty": 1-5,
            "tags": ["知识点标签"]
        }}
    ]
}}
"""
        return prompt
    
    def _parse_ai_response(self, response: str, count: int) -> List[Dict]:
        """解析AI响应"""
        try:
            # 尝试解析JSON
            data = json.loads(response)
            if "questions" in data:
                return data["questions"][:count]
        except:
            pass
        
        # 如果解析失败，返回模拟数据
        return self._generate_mock_questions("通用", count)
    
    def _generate_mock_questions(self, subject: str, count: int) -> List[Dict]:
        """生成模拟题目数据"""
        questions = []
        question_types = ["choice", "fill", "essay"]
        
        for i in range(count):
            q_type = question_types[i % len(question_types)]
            
            if q_type == "choice":
                question = {
                    "title": f"{subject}选择题 {i+1}",
                    "content": f"这是一道关于{subject}的选择题，请选择正确答案。",
                    "type": "choice",
                    "options": ["选项A", "选项B", "选项C", "选项D"],
                    "answer": "选项A",
                    "explanation": "这是正确答案的详细解析。",
                    "difficulty": 3,
                    "tags": [subject, "基础"]
                }
            elif q_type == "fill":
                question = {
                    "title": f"{subject}填空题 {i+1}",
                    "content": f"请填写{subject}相关的正确答案。",
                    "type": "fill",
                    "options": [],
                    "answer": "正确答案",
                    "explanation": "填空题的解析说明。",
                    "difficulty": 2,
                    "tags": [subject, "基础"]
                }
            else:
                question = {
                    "title": f"{subject}简答题 {i+1}",
                    "content": f"请详细回答关于{subject}的问题。",
                    "type": "essay",
                    "options": [],
                    "answer": "标准答案",
                    "explanation": "简答题的详细解析。",
                    "difficulty": 4,
                    "tags": [subject, "综合"]
                }
            
            questions.append(question)
        
        return questions
    
    async def generate_questions_by_tags_and_skills(self, tags: list, skills: list, count_per_skill: int = 5, difficulty: int = 3) -> int:
        """遍历所有标签和技能点，批量生成题目并写入 skill 字段"""
        total_generated = 0
        for tag in tags:
            for skill in skills:
                try:
                    questions = await self.ai_service.generate_questions_with_skill(
                        subject=tag,
                        skill=skill,
                        difficulty=difficulty,
                        count=count_per_skill
                    )
                    for q_data in questions:
                        question = Question(
                            content=q_data.get("content"),
                            question_type=q_data.get("question_type"),
                            options=q_data.get("options"),
                            answer=q_data.get("answer"),
                            explanation=q_data.get("explanation"),
                            difficulty=q_data.get("difficulty", difficulty),
                            tags=q_data.get("tags"),
                            skill=q_data.get("skill"),
                            source="ai_generated",
                            is_active=True
                        )
                        self.db.add(question)
                        total_generated += 1
                    self.db.commit()
                except Exception as e:
                    logger.error(f"生成题目失败: tag={tag}, skill={skill}, 错误: {e}")
                    self.db.rollback()
        logger.info(f"批量生成题目完成，共生成 {total_generated} 道题目")
        return total_generated

    async def generate_daily_questions(self) -> dict:
        """为所有标签和技能点批量生成每日题目"""
        # 示例：假设标签和技能点列表可从数据库或配置获取
        tags = ["数学", "英语", "编程基础"]
        skills = ["四则运算", "阅读理解", "循环结构", "条件判断"]
        total_generated = await self.generate_questions_by_tags_and_skills(tags, skills, count_per_skill=5, difficulty=3)
        return {"total_generated": total_generated, "tags": tags, "skills": skills}
    
    async def generate_subject_questions(self, subject: str, difficulty: str = "medium", count: int = 20) -> List[Dict]:
        """为特定学科生成题目"""
        try:
            # 构建学科特定的提示词
            prompt = f"""
请为{subject}科目生成{count}道{difficulty}难度的题目，要求：

1. 题目类型多样化（选择题、填空题、简答题）
2. 内容覆盖{subject}的核心知识点
3. 难度适中，适合{difficulty}水平的学生
4. 提供详细的解析和答案

请以JSON格式返回题目数据。
"""
            
            # 调用AI生成
            response = await self.ai_service._call_ai_api(prompt)
            if response:
                questions = self._parse_ai_response(response, count)
            else:
                questions = self._generate_mock_questions(subject, count)
            
            # 保存到数据库
            saved_questions = []
            for q_data in questions:
                question = Question(
                    title=q_data["title"],
                    content=q_data["content"],
                    answer=q_data["answer"],
                    explanation=q_data["explanation"],
                    subject=subject,
                    difficulty=q_data["difficulty"],
                    question_type=q_data["type"],
                    options=json.dumps(q_data.get("options", []), ensure_ascii=False),
                    tags=json.dumps(q_data.get("tags", []), ensure_ascii=False)
                )
                self.db.add(question)
                saved_questions.append(question)
            
            self.db.commit()
            logger.info(f"为{subject}学科生成了{len(saved_questions)}道题目")
            
            return [{"id": q.id, "title": q.title, "difficulty": q.difficulty} for q in saved_questions]
            
        except Exception as e:
            logger.error(f"生成{subject}题目失败: {str(e)}")
            self.db.rollback()
            return [] 