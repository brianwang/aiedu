from datetime import datetime
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc
import random

from app.models.question import (
    Question, QuestionCategory, UserAnswer, PracticeSession, 
    PracticeSessionQuestion, KnowledgePoint, QuestionDifficulty, QuestionSource
)
from app.models.user import User
from app.schemas.question import QuestionCreate, QuestionUpdate


class QuestionBankService:
    """题库服务类"""
    
    @staticmethod
    def get_questions_by_category(
        db: Session, 
        category_id: int, 
        difficulty: Optional[str] = None,
        limit: int = 20,
        exclude_answered: bool = False,
        user_id: Optional[int] = None
    ) -> List[Question]:
        """根据分类获取题目"""
        query = db.query(Question).filter(
            Question.category_id == category_id,
            Question.is_active == True
        )
        
        if difficulty:
            query = query.filter(Question.difficulty == difficulty)
            
        if exclude_answered and user_id:
            # 排除已答过的题目
            answered_questions = db.query(UserAnswer.question_id).filter(
                UserAnswer.user_id == user_id
            ).subquery()
            query = query.filter(~Question.id.in_(answered_questions))
            
        return query.limit(limit).all()
    
    @staticmethod
    def get_random_questions(
        db: Session,
        category_id: Optional[int] = None,
        difficulty: Optional[str] = None,
        count: int = 10,
        user_id: Optional[int] = None
    ) -> List[Question]:
        """获取随机题目"""
        query = db.query(Question).filter(Question.is_active == True)
        
        if category_id:
            query = query.filter(Question.category_id == category_id)
            
        if difficulty:
            query = query.filter(Question.difficulty == difficulty)
            
        if user_id:
            # 优先选择用户未答过的题目
            answered_questions = db.query(UserAnswer.question_id).filter(
                UserAnswer.user_id == user_id
            ).subquery()
            query = query.filter(~Question.id.in_(answered_questions))
        
        questions = query.all()
        
        # 如果题目不够，补充已答过的题目
        if len(questions) < count and user_id:
            remaining_count = count - len(questions)
            answered_questions = db.query(Question).join(UserAnswer).filter(
                UserAnswer.user_id == user_id,
                Question.is_active == True
            )
            if category_id:
                answered_questions = answered_questions.filter(Question.category_id == category_id)
            if difficulty:
                answered_questions = answered_questions.filter(Question.difficulty == difficulty)
                
            additional_questions = answered_questions.limit(remaining_count).all()
            questions.extend(additional_questions)
        
        return random.sample(questions, min(count, len(questions)))
    
    @staticmethod
    def get_ai_recommended_questions(
        db: Session,
        user_id: int,
        count: int = 10
    ) -> List[Question]:
        """获取AI推荐的题目"""
        # 获取用户答题历史
        user_answers = db.query(UserAnswer).filter(
            UserAnswer.user_id == user_id
        ).all()
        
        # 分析用户薄弱知识点
        weak_points = QuestionBankService._analyze_weak_points(db, user_answers)
        
        # 根据薄弱知识点推荐题目
        recommended_questions = []
        for point in weak_points:
            questions = db.query(Question).filter(
                Question.is_active == True,
                Question.tags.contains([point])
            ).limit(count // len(weak_points)).all()
            recommended_questions.extend(questions)
        
        # 如果推荐题目不够，补充随机题目
        if len(recommended_questions) < count:
            remaining = count - len(recommended_questions)
            random_questions = QuestionBankService.get_random_questions(
                db, count=remaining, user_id=user_id
            )
            recommended_questions.extend(random_questions)
        
        return recommended_questions[:count]
    
    @staticmethod
    def _analyze_weak_points(db: Session, user_answers: List[UserAnswer]) -> List[str]:
        """分析用户薄弱知识点"""
        # 统计错误率高的知识点
        point_errors = {}
        for answer in user_answers:
            if not answer.is_correct and answer.question.tags:
                for tag in answer.question.tags:
                    if tag not in point_errors:
                        point_errors[tag] = {'correct': 0, 'incorrect': 0}
                    point_errors[tag]['incorrect'] += 1
        
        # 计算错误率并返回薄弱知识点
        weak_points = []
        for point, stats in point_errors.items():
            total = stats['correct'] + stats['incorrect']
            if total >= 3 and stats['incorrect'] / total > 0.5:  # 错误率超过50%
                weak_points.append(point)
        
        return weak_points[:5]  # 返回前5个薄弱知识点
    
    @staticmethod
    def create_practice_session(
        db: Session,
        user_id: int,
        session_type: str,
        category_id: Optional[int] = None,
        question_count: int = 10
    ) -> PracticeSession:
        """创建练习会话"""
        # 根据会话类型获取题目
        if session_type == "random":
            questions = QuestionBankService.get_random_questions(
                db, category_id=category_id, count=question_count, user_id=user_id
            )
        elif session_type == "ai_recommended":
            questions = QuestionBankService.get_ai_recommended_questions(
                db, user_id, count=question_count
            )
        else:
            questions = QuestionBankService.get_questions_by_category(
                db, category_id, limit=question_count, user_id=user_id
            )
        
        # 创建练习会话
        session = PracticeSession(
            user_id=user_id,
            session_type=session_type,
            category_id=category_id,
            question_count=len(questions),
            started_at=datetime.utcnow()
        )
        db.add(session)
        db.flush()  # 获取session.id
        
        # 创建会话题目关联
        for i, question in enumerate(questions):
            session_question = PracticeSessionQuestion(
                session_id=session.id,
                question_id=question.id,
                sequence=i + 1
            )
            db.add(session_question)
        
        db.commit()
        db.refresh(session)
        return session
    
    @staticmethod
    def submit_answer(
        db: Session,
        session_id: int,
        question_id: int,
        user_answer: str,
        time_spent: int,
        confidence_level: int = 50
    ) -> Dict[str, Any]:
        """提交答案"""
        # 获取题目
        question = db.query(Question).filter(Question.id == question_id).first()
        if not question:
            raise ValueError("题目不存在")
        
        # 判断答案是否正确
        is_correct = QuestionBankService._check_answer(question, user_answer)
        
        # 更新会话题目
        session_question = db.query(PracticeSessionQuestion).filter(
            PracticeSessionQuestion.session_id == session_id,
            PracticeSessionQuestion.question_id == question_id
        ).first()
        
        if session_question:
            session_question.user_answer = user_answer
            session_question.is_correct = is_correct
            session_question.time_spent = time_spent
            session_question.answered_at = datetime.utcnow()
        
        # 记录用户答题历史
        user_answer_record = UserAnswer(
            user_id=session_question.session.user_id,
            question_id=question_id,
            answer=user_answer,
            is_correct=is_correct,
            time_spent=time_spent,
            confidence_level=confidence_level
        )
        db.add(user_answer_record)
        
        # 更新题目统计
        question.usage_count += 1
        if is_correct:
            # 更新正确率
            total_answers = db.query(UserAnswer).filter(
                UserAnswer.question_id == question_id
            ).count()
            correct_answers = db.query(UserAnswer).filter(
                UserAnswer.question_id == question_id,
                UserAnswer.is_correct == True
            ).count()
            question.success_rate = correct_answers / total_answers if total_answers > 0 else 0
        
        db.commit()
        
        return {
            "is_correct": is_correct,
            "correct_answer": question.answer,
            "explanation": question.explanation,
            "question": question
        }
    
    @staticmethod
    def _check_answer(question: Question, user_answer: str) -> bool:
        """检查答案是否正确"""
        if question.question_type == QuestionType.SINGLE_CHOICE:
            return user_answer.strip().upper() == question.answer.strip().upper()
        elif question.question_type == QuestionType.MULTIPLE_CHOICE:
            user_choices = set(user_answer.strip().upper().split(','))
            correct_choices = set(question.answer.strip().upper().split(','))
            return user_choices == correct_choices
        else:
            # 对于填空题和简答题，进行模糊匹配
            return user_answer.strip().lower() in question.answer.strip().lower()
    
    @staticmethod
    def complete_practice_session(
        db: Session,
        session_id: int
    ) -> PracticeSession:
        """完成练习会话"""
        session = db.query(PracticeSession).filter(
            PracticeSession.id == session_id
        ).first()
        
        if not session:
            raise ValueError("练习会话不存在")
        
        # 计算正确数量和准确率
        session_questions = db.query(PracticeSessionQuestion).filter(
            PracticeSessionQuestion.session_id == session_id,
            PracticeSessionQuestion.is_correct.isnot(None)
        ).all()
        
        correct_count = sum(1 for sq in session_questions if sq.is_correct)
        total_time = sum(sq.time_spent for sq in session_questions)
        
        session.correct_count = correct_count
        session.total_time = total_time
        session.accuracy_rate = correct_count / len(session_questions) if session_questions else 0
        session.completed_at = datetime.utcnow()
        session.is_completed = True
        
        db.commit()
        db.refresh(session)
        return session
    
    @staticmethod
    def get_user_statistics(
        db: Session,
        user_id: int
    ) -> Dict[str, Any]:
        """获取用户练习统计"""
        # 总答题数
        total_answers = db.query(UserAnswer).filter(
            UserAnswer.user_id == user_id
        ).count()
        
        # 正确答题数
        correct_answers = db.query(UserAnswer).filter(
            UserAnswer.user_id == user_id,
            UserAnswer.is_correct == True
        ).count()
        
        # 总练习时间
        total_time = db.query(func.sum(UserAnswer.time_spent)).filter(
            UserAnswer.user_id == user_id
        ).scalar() or 0
        
        # 练习会话数
        session_count = db.query(PracticeSession).filter(
            PracticeSession.user_id == user_id,
            PracticeSession.is_completed == True
        ).count()
        
        # 按分类统计
        category_stats = db.query(
            QuestionCategory.name,
            func.count(UserAnswer.id).label('total'),
            func.sum(func.case([(UserAnswer.is_correct == True, 1)], else_=0)).label('correct')
        ).join(Question).join(UserAnswer).filter(
            UserAnswer.user_id == user_id
        ).group_by(QuestionCategory.id, QuestionCategory.name).all()
        
        return {
            "total_answers": total_answers,
            "correct_answers": correct_answers,
            "accuracy_rate": correct_answers / total_answers if total_answers > 0 else 0,
            "total_time_minutes": total_time // 60,
            "session_count": session_count,
            "category_stats": [
                {
                    "category": stat.name,
                    "total": stat.total,
                    "correct": stat.correct,
                    "accuracy": stat.correct / stat.total if stat.total > 0 else 0
                }
                for stat in category_stats
            ]
        } 