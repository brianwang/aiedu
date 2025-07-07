from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.services.ai_service import AIService
from app.services.auth_service import get_current_user
from app.models.user import User
from database import get_db

router = APIRouter(prefix="/ai", tags=["AI智能服务"])

ai_service = AIService()


@router.get("/recommendations")
async def get_recommended_questions(
    subject: Optional[str] = None,
    count: int = 10,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取智能推荐的题目"""
    try:
        questions = await ai_service.recommend_questions(
            db=db,
            user_id=current_user.id,
            subject=subject,
            count=count
        )

        return {
            "success": True,
            "data": [
                {
                    "id": q.id,
                    "content": q.content,
                    "question_type": q.question_type,
                    "options": q.options,
                    "difficulty": q.difficulty,
                    "category": q.category.name if q.category else None
                }
                for q in questions
            ],
            "message": f"为您推荐了 {len(questions)} 道题目"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取推荐题目失败: {str(e)}")


@router.get("/study-plan")
async def get_study_plan(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取个性化学习计划"""
    try:
        study_plan = await ai_service.create_study_plan(db=db, user_id=current_user.id)

        if not study_plan:
            raise HTTPException(status_code=404, detail="无法生成学习计划")

        return {
            "success": True,
            "data": study_plan,
            "message": "学习计划生成成功"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成学习计划失败: {str(e)}")


@router.get("/learning-pattern")
async def get_learning_pattern(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取学习模式分析"""
    try:
        pattern = await ai_service.analyze_learning_pattern(db=db, user_id=current_user.id)

        return {
            "success": True,
            "data": pattern,
            "message": "学习模式分析完成"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"分析学习模式失败: {str(e)}")


@router.post("/generate-questions")
async def generate_questions(
    subject: str,
    difficulty: int,
    count: int = 10,
    current_user: User = Depends(get_current_user)
):
    """AI生成题目（仅教师和管理员可用）"""
    if current_user.role not in ["teacher", "admin"]:
        raise HTTPException(status_code=403, detail="权限不足")

    try:
        questions = await ai_service.generate_questions(
            subject=subject,
            difficulty=difficulty,
            count=count
        )

        return {
            "success": True,
            "data": questions,
            "message": f"成功生成 {len(questions)} 道题目"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成题目失败: {str(e)}")


@router.get("/difficulty-analysis")
async def get_difficulty_analysis(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取难度分析建议"""
    try:
        # 获取用户的学习数据
        from app.models.user import StudySession, WrongQuestion

        study_sessions = db.query(StudySession).filter(
            StudySession.user_id == current_user.id
        ).all()

        wrong_questions = db.query(WrongQuestion).filter(
            WrongQuestion.user_id == current_user.id
        ).all()

        # 计算正确率
        total_questions = sum(
            session.questions_answered for session in study_sessions)
        total_correct = sum(
            session.correct_answers for session in study_sessions)
        accuracy = (total_correct / total_questions *
                    100) if total_questions > 0 else 0

        # 生成建议
        if accuracy >= 90:
            suggestion = "您的表现非常优秀！建议尝试更高难度的题目来挑战自己。"
            recommended_difficulty = "increase"
        elif accuracy >= 75:
            suggestion = "您的学习效果良好，可以适当增加题目难度。"
            recommended_difficulty = "maintain"
        elif accuracy >= 60:
            suggestion = "您的学习进度正常，建议保持当前难度继续练习。"
            recommended_difficulty = "maintain"
        else:
            suggestion = "建议从基础题目开始，逐步提升难度。"
            recommended_difficulty = "decrease"

        return {
            "success": True,
            "data": {
                "accuracy": round(accuracy, 2),
                "total_questions": total_questions,
                "wrong_questions_count": len(wrong_questions),
                "suggestion": suggestion,
                "recommended_difficulty": recommended_difficulty
            },
            "message": "难度分析完成"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"分析失败: {str(e)}")
