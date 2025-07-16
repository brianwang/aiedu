from fastapi import APIRouter, Depends, HTTPException, Form, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional, Dict
from pydantic import BaseModel
from app.services.ai_service import AIService
from app.services.auth_service import get_current_user
from app.models.user import User
from database import get_db
from config import settings
import json
import logging

router = APIRouter(prefix="/ai", tags=["AI智能服务"])

ai_service = AIService()

# 权限检查函数


def require_role(allowed_roles: List[str]):
    """检查用户角色权限"""
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=403,
                detail=f"权限不足，需要角色: {', '.join(allowed_roles)}"
            )
        return current_user
    return role_checker


# 请求模型
class QuestionGenerationRequest(BaseModel):
    subject: str
    difficulty: int
    count: int = 10
    question_types: Optional[List[str]] = None


class SmartGradingRequest(BaseModel):
    question_content: str
    standard_answer: str
    student_answer: str
    question_type: str
    max_score: int
    student_level: str = "intermediate"


class RealTimeQARequest(BaseModel):
    question: str
    context: str = ""
    user_level: str = "intermediate"


class SpeechToTextRequest(BaseModel):
    language: str = "zh-CN"


class TextToSpeechRequest(BaseModel):
    text: str
    voice: str = "zh-CN-XiaoxiaoNeural"


# AI功能API端点

@router.post("/generate-questions")
async def generate_questions(
    request: QuestionGenerationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """AI生成题目"""
    try:
        questions = await ai_service.generate_questions(
            subject=request.subject,
            difficulty=request.difficulty,
            count=request.count,
            question_types=request.question_types or []
        )
        return {
            "success": True,
            "data": questions,
            "message": f"成功生成{len(questions)}道题目"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成题目失败: {str(e)}")


@router.post("/smart-grading")
async def smart_grading(
    request: SmartGradingRequest,
    current_user: User = Depends(get_current_user)
):
    """智能评分"""
    try:
        result = await ai_service.smart_grading(
            question_content=request.question_content,
            standard_answer=request.standard_answer,
            student_answer=request.student_answer,
            question_type=request.question_type,
            max_score=request.max_score,
            student_level=request.student_level
        )
        return {
            "success": True,
            "data": result,
            "message": "智能评分完成"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"智能评分失败: {str(e)}")


@router.post("/real-time-qa")
async def real_time_qa(
    request: RealTimeQARequest,
    current_user: User = Depends(get_current_user)
):
    """实时AI问答"""
    try:
        result = await ai_service.real_time_qa(
            question=request.question,
            context=request.context,
            user_level=request.user_level
        )
        return {
            "success": True,
            "data": result,
            "message": "AI回答完成"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI问答失败: {str(e)}")


@router.post("/speech-to-text")
async def speech_to_text(
    audio_file: UploadFile = File(...),
    language: str = Form("zh-CN"),
    current_user: User = Depends(get_current_user)
):
    """语音转文字"""
    try:
        audio_data = await audio_file.read()
        result = await ai_service.speech_to_text(audio_data, language)
        return {
            "success": True,
            "data": result,
            "message": "语音识别完成"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"语音识别失败: {str(e)}")


@router.post("/text-to-speech")
async def text_to_speech(
    request: TextToSpeechRequest,
    current_user: User = Depends(get_current_user)
):
    """文字转语音"""
    try:
        audio_data = await ai_service.text_to_speech(request.text, request.voice)
        return {
            "success": True,
            "data": {
                "audio_data": audio_data.hex() if audio_data else "",
                "text": request.text,
                "voice": request.voice
            },
            "message": "文字转语音完成"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文字转语音失败: {str(e)}")


@router.get("/recommendations")
async def get_recommendations(
    subject: Optional[str] = None,
    count: int = 10,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取智能推荐题目"""
    try:
        user_id = getattr(current_user, 'id', None)
        if user_id is None:
            raise HTTPException(status_code=400, detail="用户ID无效")
        questions = await ai_service.recommend_questions(db, user_id, subject or "", count)
        return {
            "success": True,
            "data": questions,
            "message": f"为您推荐了{len(questions)}道题目"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取推荐失败: {str(e)}")


@router.get("/learning-report")
async def get_learning_report(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取学习分析报告"""
    try:
        user_id = getattr(current_user, 'id', None)
        if user_id is None:
            raise HTTPException(status_code=400, detail="用户ID无效")
        report = await ai_service.generate_learning_report(user_id, db)
        return {
            "success": True,
            "data": report,
            "message": "学习报告生成完成"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成学习报告失败: {str(e)}")


@router.get("/learning-motivation")
async def get_learning_motivation(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取学习激励信息"""
    try:
        user_id = getattr(current_user, 'id', None)
        if user_id is None:
            raise HTTPException(status_code=400, detail="用户ID无效")
        motivation = await ai_service.generate_learning_motivation(user_id, db)
        return {
            "success": True,
            "data": motivation,
            "message": "学习激励生成完成"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成学习激励失败: {str(e)}")


@router.get("/learning-style")
async def get_learning_style(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取学习风格分析"""
    try:
        user_id = getattr(current_user, 'id', None)
        if user_id is None:
            raise HTTPException(status_code=400, detail="用户ID无效")
        style = await ai_service.identify_learning_style(user_id, db)
        return {
            "success": True,
            "data": style,
            "message": "学习风格分析完成"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"学习风格分析失败: {str(e)}")


@router.post("/analyze-wrong-question")
async def analyze_wrong_question(
    question_content: str,
    user_answer: str,
    correct_answer: str,
    subject: str,
    current_user: User = Depends(get_current_user)
):
    """错题分析讲解"""
    try:
        analysis = await ai_service.analyze_wrong_question(
            question_content, user_answer, correct_answer, subject
        )
        return {
            "success": True,
            "data": analysis,
            "message": "错题分析完成"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"错题分析失败: {str(e)}")


@router.get("/ai-status")
async def get_ai_status():
    """获取AI服务状态"""
    try:
        status = {
            "ai_available": ai_service._ai_available,
            "clients_count": len(ai_service._clients),
            "cache_enabled": settings.ai_cache_enabled,
            "cache_size": len(ai_service._cache),
            "available_models": list(ai_service._clients.keys()) if ai_service._clients else []
        }
        return {
            "success": True,
            "data": status,
            "message": "AI服务状态正常" if ai_service._ai_available else "AI服务不可用"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取AI状态失败: {str(e)}")
    """获取AI服务状态"""
    try:
        status = {
            "ai_available": ai_service._ai_available,
            "clients_count": len(ai_service._clients),
            "cache_enabled": ai_service._cache is not None,
            "cache_size": len(ai_service._cache) if ai_service._cache else 0
        }
        return {
            "success": True,
            "data": status,
            "message": "AI服务状态正常"
        }
    except Exception as e:
        return {
            "success": False,
            "data": {"ai_available": False},
            "message": f"AI服务状态异常: {str(e)}"
        }


# 保留原有的其他端点...
