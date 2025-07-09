from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from database import get_db
from app.models.user import User
from app.services.auth_service import get_current_user
from app.services.question_bank_service import QuestionBankService
from app.schemas.question import QuestionResponse, QuestionCategoryResponse

router = APIRouter(prefix="/question-bank", tags=["question-bank"])


@router.get("/categories", response_model=List[QuestionCategoryResponse])
async def get_question_categories(
    db: Session = Depends(get_db)
):
    """获取题目分类列表"""
    from app.models.question import QuestionCategory
    categories = db.query(QuestionCategory).filter(
        QuestionCategory.is_active == True
    ).all()
    return categories


@router.get("/categories/{category_id}/questions", response_model=List[QuestionResponse])
async def get_questions_by_category(
    category_id: int,
    difficulty: Optional[str] = None,
    limit: int = 20,
    exclude_answered: bool = False,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """根据分类获取题目"""
    user_id = getattr(current_user, 'id', None)
    questions = QuestionBankService.get_questions_by_category(
        db=db,
        category_id=category_id,
        difficulty=difficulty,
        limit=limit,
        exclude_answered=exclude_answered,
        user_id=user_id
    )
    return questions


@router.get("/random", response_model=List[QuestionResponse])
async def get_random_questions(
    category_id: Optional[int] = None,
    difficulty: Optional[str] = None,
    count: int = 10,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取随机题目"""
    user_id = getattr(current_user, 'id', None)
    questions = QuestionBankService.get_random_questions(
        db=db,
        category_id=category_id,
        difficulty=difficulty,
        count=count,
        user_id=user_id
    )
    return questions


@router.get("/ai-recommended", response_model=List[QuestionResponse])
async def get_ai_recommended_questions(
    count: int = 10,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取AI推荐题目"""
    user_id = getattr(current_user, 'id', None)
    questions = QuestionBankService.get_ai_recommended_questions(
        db=db,
        user_id=user_id,
        count=count
    )
    return questions


@router.post("/practice-sessions")
async def create_practice_session(
    session_type: str,  # random, category, ai_recommended
    category_id: Optional[int] = None,
    question_count: int = 10,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """创建练习会话"""
    try:
        user_id = getattr(current_user, 'id', None)
        session = QuestionBankService.create_practice_session(
            db=db,
            user_id=user_id,
            session_type=session_type,
            category_id=category_id,
            question_count=question_count
        )
        return {
            "session_id": session.id,
            "question_count": session.question_count,
            "started_at": session.started_at
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/practice-sessions/{session_id}/submit")
async def submit_answer(
    session_id: int,
    question_id: int,
    answer: str,
    time_spent: int,
    confidence_level: int = 50,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """提交答案"""
    try:
        result = QuestionBankService.submit_answer(
            db=db,
            session_id=session_id,
            question_id=question_id,
            user_answer=answer,
            time_spent=time_spent,
            confidence_level=confidence_level
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/practice-sessions/{session_id}/complete")
async def complete_practice_session(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """完成练习会话"""
    try:
        session = QuestionBankService.complete_practice_session(
            db=db,
            session_id=session_id
        )
        return {
            "session_id": session.id,
            "correct_count": session.correct_count,
            "total_questions": session.question_count,
            "accuracy_rate": session.accuracy_rate,
            "total_time": session.total_time,
            "completed_at": session.completed_at
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/statistics")
async def get_user_statistics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取用户练习统计"""
    user_id = getattr(current_user, 'id', None)
    stats = QuestionBankService.get_user_statistics(
        db=db,
        user_id=user_id
    )
    return stats


@router.get("/practice-sessions")
async def get_user_practice_sessions(
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取用户练习会话历史"""
    from app.models.question import PracticeSession
    
    user_id = getattr(current_user, 'id', None)
    sessions = db.query(PracticeSession).filter(
        PracticeSession.user_id == user_id,
        PracticeSession.is_completed == True
    ).order_by(PracticeSession.completed_at.desc()).limit(limit).all()
    
    return [
        {
            "id": session.id,
            "session_type": session.session_type,
            "question_count": session.question_count,
            "correct_count": session.correct_count,
            "accuracy_rate": session.accuracy_rate,
            "total_time": session.total_time,
            "started_at": session.started_at,
            "completed_at": session.completed_at
        }
        for session in sessions
    ] 