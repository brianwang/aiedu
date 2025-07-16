from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from typing import List, Optional, Dict
from database import get_db
from app.models.exam import Exam
from app.models.question import Question, ExamQuestion
from app.models.user import User
from app.services.auth_service import get_current_user
from app.services.ai_service import AIService
from app.schemas.exam import ExamCreate, Exam as ExamSchema
from sqlalchemy import or_
from pydantic import BaseModel

router = APIRouter(prefix="/exam", tags=["考试系统"])

# 初始化AI服务
ai_service = AIService()


class ExamGenerateRequest(BaseModel):
    subject: str
    difficulty: int
    exam_type: Optional[str] = "comprehensive"
    question_distribution: Optional[Dict[str, int]] = None
    skill: Optional[str] = None
    tags: Optional[List[str]] = None


@router.post("/generate", response_model=ExamSchema, summary="AI智能组卷")
async def generate_exam(
    req: ExamGenerateRequest = Body(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """AI智能组卷"""
    try:
        # 调用AI服务生成试卷
        exam_data = await ai_service.generate_exam(
            subject=req.subject,
            difficulty=req.difficulty,
            exam_type=req.exam_type,
            question_distribution=req.question_distribution or {
                "single_choice": 20,
                "multiple_choice": 10,
                "fill_blank": 5,
                "short_answer": 3
            },
            skill=req.skill,
            tags=req.tags
        )
        
        # 创建考试记录
        exam = Exam(
            title=exam_data.get("title", f"{req.subject}考试"),
            description=exam_data.get("description", f"{req.subject}综合测试"),
            subject=req.subject,
            difficulty=req.difficulty,
            exam_type=req.exam_type,
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
                    difficulty=question_data.get("difficulty", req.difficulty)
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
        return {"id": exam.id}
        
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
    q: Optional[str] = None,
    page: int = 1,
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取考试列表，支持分页、搜索"""
    query = db.query(Exam)
    if subject:
        query = query.filter(Exam.subject == subject)
    if difficulty:
        query = query.filter(Exam.difficulty == difficulty)
    if q:
        query = query.filter(or_(Exam.title.ilike(f"%{q}%"), Exam.subject.ilike(f"%{q}%")))
    query = query.filter(Exam.created_by == current_user.id)
    total = query.count()
    exams = query.order_by(Exam.created_at.desc()).offset((page-1)*limit).limit(limit).all()
    # 查询成绩
    exam_ids = [e.id for e in exams]
    from app.models.exam import ExamResult
    results = db.query(ExamResult).filter(ExamResult.exam_id.in_(exam_ids), ExamResult.student_id == current_user.id).all()
    result_map = {r.exam_id: r.score for r in results}
    items = []
    for e in exams:
        items.append({
            "id": e.id,
            "title": e.title,
            "subject": e.subject,
            "difficulty": e.difficulty,
            "total_score": e.total_score,
            "created_at": e.created_at.strftime("%Y-%m-%d %H:%M"),
            "score": result_map.get(e.id)
        })
    return {"items": items, "total": total}


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


@router.delete("/{exam_id}", summary="删除试卷")
async def delete_exam(
    exam_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    exam = db.query(Exam).filter(Exam.id == exam_id, Exam.created_by == current_user.id).first()
    if not exam:
        raise HTTPException(status_code=404, detail="试卷不存在或无权限")
    db.delete(exam)
    db.commit()
    return {"success": True}


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
