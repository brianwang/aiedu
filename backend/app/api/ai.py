from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from typing import List, Optional, Dict
from pydantic import BaseModel
from app.services.ai_service import AIService
from app.services.auth_service import get_current_user
from app.models.user import User
from database import get_db
import json
import logging

router = APIRouter(prefix="/ai", tags=["AI智能服务"])

ai_service = AIService()

# 请求模型
class SmartGradingRequest(BaseModel):
    question_content: str
    standard_answer: str
    student_answer: str
    question_type: str
    max_score: int

class AbilityAssessmentRequest(BaseModel):
    study_time: int
    questions_completed: int
    accuracy: float
    subjects: List[str]
    wrong_questions_distribution: Dict[str, int]

class LearningStyleRequest(BaseModel):
    time_distribution: Dict[str, int]
    question_type_preference: Dict[str, int]
    learning_mode: str
    review_frequency: int
    wrong_question_handling: str

class MotivationRequest(BaseModel):
    learning_status: str
    learning_difficulties: List[str]
    learning_goals: List[str]
    learning_achievements: List[str]
    personal_characteristics: List[str]

class LearningPathRequest(BaseModel):
    target_skill: str

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


@router.post("/smart-grading")
async def smart_grading(
    request: SmartGradingRequest,
    current_user: User = Depends(get_current_user)
):
    """智能评分（仅教师和管理员可用）"""
    if current_user.role not in ["teacher", "admin"]:
        raise HTTPException(status_code=403, detail="权限不足")

    try:
        # 这里可以集成OpenAI API进行智能评分
        # 目前返回模拟评分结果
        grading_result = await ai_service.smart_grading(
            question_content=request.question_content,
            standard_answer=request.standard_answer,
            student_answer=request.student_answer,
            question_type=request.question_type,
            max_score=request.max_score
        )

        return {
            "success": True,
            "data": grading_result,
            "message": "智能评分完成"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"智能评分失败: {str(e)}")


@router.post("/ability-assessment")
async def assess_learning_ability(
    request: AbilityAssessmentRequest,
    current_user: User = Depends(get_current_user)
):
    """学习能力评估"""
    try:
        assessment_result = await ai_service.assess_learning_ability(
            study_time=request.study_time,
            questions_completed=request.questions_completed,
            accuracy=request.accuracy,
            subjects=request.subjects,
            wrong_questions_distribution=request.wrong_questions_distribution
        )

        return {
            "success": True,
            "data": assessment_result,
            "message": "能力评估完成"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"能力评估失败: {str(e)}")


@router.post("/learning-style")
async def analyze_learning_style(
    request: LearningStyleRequest,
    current_user: User = Depends(get_current_user)
):
    """学习风格分析"""
    try:
        style_result = await ai_service.analyze_learning_style(
            time_distribution=request.time_distribution,
            question_type_preference=request.question_type_preference,
            learning_mode=request.learning_mode,
            review_frequency=request.review_frequency,
            wrong_question_handling=request.wrong_question_handling
        )

        return {
            "success": True,
            "data": style_result,
            "message": "学习风格分析完成"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"学习风格分析失败: {str(e)}")


@router.post("/motivation")
async def get_motivation_plan(
    request: MotivationRequest,
    current_user: User = Depends(get_current_user)
):
    """获取学习动机激励方案"""
    try:
        motivation_plan = await ai_service.get_motivation_plan(
            learning_status=request.learning_status,
            learning_difficulties=request.learning_difficulties,
            learning_goals=request.learning_goals,
            learning_achievements=request.learning_achievements,
            personal_characteristics=request.personal_characteristics
        )

        return {
            "success": True,
            "data": motivation_plan,
            "message": "激励方案生成完成"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成激励方案失败: {str(e)}")


@router.get("/user-ability-assessment")
async def get_user_ability_assessment(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取用户的能力评估（基于学习数据）"""
    try:
        # 获取用户的学习数据
        from app.models.user import StudySession, WrongQuestion
        from app.models.question import Question, QuestionCategory

        # 获取学习会话数据
        study_sessions = db.query(StudySession).filter(
            StudySession.user_id == current_user.id
        ).all()

        # 获取错题数据
        wrong_questions = db.query(WrongQuestion).filter(
            WrongQuestion.user_id == current_user.id
        ).join(Question).join(QuestionCategory).all()

        # 计算基础数据
        total_study_time = sum(session.duration_minutes for session in study_sessions)
        total_questions = sum(session.questions_answered for session in study_sessions)
        total_correct = sum(session.correct_answers for session in study_sessions)
        accuracy = (total_correct / total_questions * 100) if total_questions > 0 else 0

        # 分析学科分布
        subjects = list(set(session.subject for session in study_sessions if session.subject))
        
        # 分析错题分布
        wrong_questions_distribution = {}
        for wq in wrong_questions:
            subject = wq.question.category.name if wq.question.category else "未知"
            wrong_questions_distribution[subject] = wrong_questions_distribution.get(subject, 0) + 1

        # 调用能力评估
        assessment_result = await ai_service.assess_learning_ability(
            study_time=total_study_time,
            questions_completed=total_questions,
            accuracy=accuracy,
            subjects=subjects,
            wrong_questions_distribution=wrong_questions_distribution
        )

        return {
            "success": True,
            "data": assessment_result,
            "message": "能力评估完成"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"能力评估失败: {str(e)}")


@router.get("/user-learning-style")
async def get_user_learning_style(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取用户的学习风格分析（基于学习数据）"""
    try:
        # 获取用户的学习数据
        from app.models.user import StudySession, WrongQuestion

        # 获取学习会话数据
        study_sessions = db.query(StudySession).filter(
            StudySession.user_id == current_user.id
        ).all()

        # 分析时间分布
        time_distribution = {}
        for session in study_sessions:
            hour = session.start_time.hour
            time_distribution[str(hour)] = time_distribution.get(str(hour), 0) + session.duration_minutes

        # 分析题目类型偏好（这里简化处理）
        question_type_preference = {
            "single_choice": 40,
            "multiple_choice": 30,
            "fill_blank": 20,
            "short_answer": 10
        }

        # 分析学习模式
        learning_mode = "continuous" if len(study_sessions) > 10 else "distributed"
        
        # 分析复习频率
        review_frequency = len(study_sessions) // 7 if len(study_sessions) > 0 else 0
        
        # 分析错题处理方式
        wrong_questions = db.query(WrongQuestion).filter(
            WrongQuestion.user_id == current_user.id
        ).all()
        wrong_question_handling = "review_frequently" if len(wrong_questions) > 0 else "ignore"

        # 调用学习风格分析
        style_result = await ai_service.analyze_learning_style(
            time_distribution=time_distribution,
            question_type_preference=question_type_preference,
            learning_mode=learning_mode,
            review_frequency=review_frequency,
            wrong_question_handling=wrong_question_handling
        )

        return {
            "success": True,
            "data": style_result,
            "message": "学习风格分析完成"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"学习风格分析失败: {str(e)}")


@router.post("/learning-path")
async def recommend_learning_path(
    request: LearningPathRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """推荐个性化学习路径"""
    try:
        learning_path = await ai_service.recommend_learning_path(
            db=db,
            user_id=current_user.id,
            target_skill=request.target_skill
        )

        if not learning_path:
            raise HTTPException(status_code=404, detail="无法生成学习路径")

        return {
            "success": True,
            "data": learning_path,
            "message": "学习路径推荐成功"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"推荐学习路径失败: {str(e)}")


@router.post("/generate-exam")
async def generate_exam(
    subject: str = Form(...),
    difficulty: int = Form(..., ge=1, le=5),
    exam_type: str = Form("comprehensive"),
    question_distribution: Optional[str] = Form(None),
    current_user: User = Depends(get_current_user)
):
    """AI智能组卷"""
    try:
        # 检查用户权限
        if current_user.role != "teacher":
            raise HTTPException(status_code=403, detail="只有教师可以生成试卷")
        
        # 解析题目分布
        distribution = None
        if question_distribution:
            try:
                distribution = json.loads(question_distribution)
            except json.JSONDecodeError:
                raise HTTPException(status_code=400, detail="题目分布格式错误")
        
        # 生成试卷
        ai_service = AIService()
        exam_data = await ai_service.generate_exam(
            subject=subject,
            difficulty=difficulty,
            exam_type=exam_type,
            question_distribution=distribution
        )
        
        return {
            "success": True,
            "message": "试卷生成成功",
            "data": exam_data
        }
        
    except Exception as e:
        logger.error(f"生成试卷失败: {e}")
        raise HTTPException(status_code=500, detail=f"生成试卷失败: {str(e)}")


@router.get("/learning-report")
async def generate_learning_report(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """生成学习分析报告"""
    try:
        ai_service = AIService()
        report = await ai_service.generate_learning_report(current_user.id, db)
        
        return {
            "success": True,
            "message": "学习分析报告生成成功",
            "data": report
        }
        
    except Exception as e:
        logger.error(f"生成学习报告失败: {e}")
        raise HTTPException(status_code=500, detail=f"生成学习报告失败: {str(e)}")


@router.post("/analyze-wrong-question")
async def analyze_wrong_question(
    question_content: str = Form(...),
    user_answer: str = Form(...),
    correct_answer: str = Form(...),
    subject: str = Form(...),
    current_user: User = Depends(get_current_user)
):
    """AI错题分析讲解"""
    try:
        ai_service = AIService()
        analysis = await ai_service.analyze_wrong_question(
            question_content=question_content,
            user_answer=user_answer,
            correct_answer=correct_answer,
            subject=subject
        )
        
        return {
            "success": True,
            "message": "错题分析完成",
            "data": analysis
        }
        
    except Exception as e:
        logger.error(f"错题分析失败: {e}")
        raise HTTPException(status_code=500, detail=f"错题分析失败: {str(e)}")


@router.get("/learning-motivation")
async def generate_learning_motivation(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """生成学习激励信息"""
    try:
        ai_service = AIService()
        motivation = await ai_service.generate_learning_motivation(current_user.id, db)
        
        return {
            "success": True,
            "message": "学习激励生成成功",
            "data": motivation
        }
        
    except Exception as e:
        logger.error(f"生成学习激励失败: {e}")
        raise HTTPException(status_code=500, detail=f"生成学习激励失败: {str(e)}")


@router.get("/learning-style")
async def identify_learning_style(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """识别学习风格"""
    try:
        ai_service = AIService()
        style_analysis = await ai_service.identify_learning_style(current_user.id, db)
        
        return {
            "success": True,
            "message": "学习风格识别完成",
            "data": style_analysis
        }
        
    except Exception as e:
        logger.error(f"学习风格识别失败: {e}")
        raise HTTPException(status_code=500, detail=f"学习风格识别失败: {str(e)}")
