from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional, Dict
from database import get_db
from app.models.exam import Exam
from app.models.question import Question, ExamQuestion
from app.models.user import User
from app.services.auth_service import get_current_user
from app.services.ai_service import AIService
from app.schemas.exam import ExamCreate, Exam as ExamSchema

router = APIRouter(prefix="/exam", tags=["考试系统"])

# 初始化AI服务
ai_service = AIService()


@router.post("/generate", response_model=ExamSchema, summary="AI智能组卷")
async def generate_exam(
    subject: str,
    difficulty: int,
    exam_type: str = "comprehensive",
    question_distribution: Optional[Dict[str, int]] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """AI智能组卷"""
    try:
        # 调用AI服务生成试卷
        exam_data = await ai_service.generate_exam(
            subject=subject,
            difficulty=difficulty,
            exam_type=exam_type,
            question_distribution=question_distribution or {
                "single_choice": 20,
                "multiple_choice": 10,
                "fill_blank": 5,
                "short_answer": 3
            }
        )
        
        # 创建考试记录
        exam = Exam(
            title=exam_data.get("title", f"{subject}考试"),
            description=exam_data.get("description", f"{subject}综合测试"),
            subject=subject,
            difficulty=difficulty,
            exam_type=exam_type,
            total_score=exam_data.get("total_score", 100),
            time_limit=exam_data.get("time_limit", 120),
            created_by=getattr(current_user, 'id', None),
            ai_generated=True
        )
        db.add(exam)
        db.flush()  # 获取exam.id
        
        # 添加试题到考试
        for i, question_data in enumerate(exam_data.get("questions", [])):
            # 查找或创建题目
            question = db.query(Question).filter(
                Question.content == question_data.get("content")
            ).first()
            
            if not question:
                # 创建新题目
                question = Question(
                    content=question_data.get("content"),
                    question_type=question_data.get("question_type"),
                    options=question_data.get("options", []),
                    answer=question_data.get("answer"),
                    explanation=question_data.get("explanation"),
                    difficulty=question_data.get("difficulty", difficulty)
                )
                db.add(question)
                db.flush()
            
            # 创建考试题目关联
            exam_question = ExamQuestion(
                exam_id=exam.id,
                question_id=question.id,
                score=question_data.get("score", 5),
                sequence=i + 1
            )
            db.add(exam_question)
        
        db.commit()
        db.refresh(exam)
        
        return exam
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"生成试卷失败: {str(e)}"
        )


@router.get("/list", response_model=List[ExamSchema], summary="获取考试列表")
async def get_exam_list(
    subject: Optional[str] = None,
    difficulty: Optional[int] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取考试列表"""
    query = db.query(Exam)
    
    if subject:
        query = query.filter(Exam.subject == subject)
    if difficulty:
        query = query.filter(Exam.difficulty == difficulty)
    
    exams = query.order_by(Exam.created_at.desc()).all()
    return exams


@router.get("/{exam_id}", response_model=ExamSchema, summary="获取考试详情")
async def get_exam_detail(
    exam_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取考试详情"""
    exam = db.query(Exam).filter(Exam.id == exam_id).first()
    if not exam:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="考试不存在"
        )
    return exam


@router.get("/{exam_id}/questions", summary="获取考试题目")
async def get_exam_questions(
    exam_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取考试题目列表"""
    exam_questions = db.query(ExamQuestion).filter(
        ExamQuestion.exam_id == exam_id
    ).order_by(ExamQuestion.sequence).all()
    
    questions = []
    for eq in exam_questions:
        question = db.query(Question).filter(Question.id == eq.question_id).first()
        if question:
            questions.append({
                "id": question.id,
                "content": question.content,
                "question_type": question.question_type,
                "options": question.options,
                "score": eq.score,
                "sequence": eq.sequence
            })
    
    return questions
