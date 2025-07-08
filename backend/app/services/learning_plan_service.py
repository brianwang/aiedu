import logging
from datetime import date, datetime, timedelta
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.models.learning import UserProfile, LearningGoal, LearningPlan, LearningTask
from app.schemas.learning import (
    LearningPlanCreate, LearningTaskCreate, LearningPlanGenerationRequest,
    LearningPlanGenerationResponse, PlanType, TaskType
)
from app.services.ai_service import AIService

logger = logging.getLogger(__name__)


class LearningPlanService:
    def __init__(self, db: Session):
        self.db = db
        self.ai_service = AIService()
    
    async def generate_learning_plan(self, request: LearningPlanGenerationRequest) -> LearningPlanGenerationResponse:
        """生成个性化学习计划"""
        try:
            logger.info(f"开始为用户 {request.user_id} 生成学习计划")
            
            # 1. 分析用户画像
            user_analysis = self._analyze_user_profile(request.profile)
            
            # 2. 制定学习路径
            learning_path = self._design_learning_path(request.goals, user_analysis)
            
            # 3. 生成具体计划
            short_term_plan = await self._generate_short_term_plan(request.user_id, learning_path, request.profile)
            medium_term_plan = await self._generate_medium_term_plan(request.user_id, learning_path, request.profile)
            long_term_plan = await self._generate_long_term_plan(request.user_id, learning_path, request.profile)
            
            # 4. 生成学习任务
            tasks = await self._generate_learning_tasks(short_term_plan.id, learning_path, request.profile)
            
            # 5. 计算预计完成时间和置信度
            estimated_time = self._calculate_estimated_completion_time(learning_path, request.profile)
            confidence_score = self._calculate_confidence_score(request.profile, request.goals)
            
            logger.info(f"用户 {request.user_id} 的学习计划生成完成")
            
            return LearningPlanGenerationResponse(
                short_term_plan=short_term_plan,
                medium_term_plan=medium_term_plan,
                long_term_plan=long_term_plan,
                tasks=tasks,
                estimated_completion_time=estimated_time,
                confidence_score=confidence_score
            )
            
        except Exception as e:
            logger.error(f"生成学习计划失败: {str(e)}")
            raise
    
    def _analyze_user_profile(self, profile: UserProfile) -> Dict[str, Any]:
        """分析用户画像，确定学习策略"""
        analysis = {
            "learning_intensity": "moderate",
            "preferred_duration": 45,
            "difficulty_curve": "progressive",
            "review_frequency": "weekly"
        }
        
        # 根据年龄调整学习策略
        if profile.age:
            if profile.age < 18:
                analysis["learning_intensity"] = "gentle"
                analysis["preferred_duration"] = 30
            elif profile.age > 40:
                analysis["learning_intensity"] = "steady"
                analysis["preferred_duration"] = 60
        
        # 根据学习风格调整
        if profile.learning_style:
            if profile.learning_style == "visual":
                analysis["content_type"] = "visual_heavy"
            elif profile.learning_style == "auditory":
                analysis["content_type"] = "audio_heavy"
            elif profile.learning_style == "kinesthetic":
                analysis["content_type"] = "hands_on"
        
        # 根据难度偏好调整
        if profile.difficulty_preference:
            if profile.difficulty_preference == "challenging":
                analysis["difficulty_curve"] = "steep"
            elif profile.difficulty_preference == "comfortable":
                analysis["difficulty_curve"] = "gentle"
        
        # 根据每日学习时间调整
        if profile.daily_study_time:
            if profile.daily_study_time < 30:
                analysis["learning_intensity"] = "light"
            elif profile.daily_study_time > 120:
                analysis["learning_intensity"] = "intensive"
        
        return analysis
    
    def _design_learning_path(self, goals: List[LearningGoal], user_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """设计学习路径"""
        learning_path = {
            "phases": [],
            "milestones": [],
            "skill_progression": {}
        }
        
        for goal in goals:
            # 根据目标水平设计学习阶段
            if goal.target_level == "beginner":
                phases = self._design_beginner_path(goal, user_analysis)
            elif goal.target_level == "intermediate":
                phases = self._design_intermediate_path(goal, user_analysis)
            elif goal.target_level == "advanced":
                phases = self._design_advanced_path(goal, user_analysis)
            else:
                phases = self._design_expert_path(goal, user_analysis)
            
            learning_path["phases"].extend(phases)
            
            # 设计里程碑
            milestones = self._design_milestones(goal, phases)
            learning_path["milestones"].extend(milestones)
            
            # 技能进阶路径
            learning_path["skill_progression"][goal.subject] = {
                "current_level": "beginner",
                "target_level": goal.target_level,
                "estimated_months": goal.target_timeframe or 6
            }
        
        return learning_path
    
    def _design_beginner_path(self, goal: LearningGoal, user_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """设计初学者学习路径"""
        return [
            {
                "name": "基础入门",
                "duration_weeks": 2,
                "focus": "基本概念和工具",
                "tasks": [
                    {"type": "study", "title": "了解基本概念", "duration": 30},
                    {"type": "practice", "title": "环境搭建", "duration": 45},
                    {"type": "assessment", "title": "基础知识测试", "duration": 20}
                ]
            },
            {
                "name": "核心技能",
                "duration_weeks": 4,
                "focus": "核心技能掌握",
                "tasks": [
                    {"type": "study", "title": "深入学习核心概念", "duration": 45},
                    {"type": "practice", "title": "项目练习", "duration": 60},
                    {"type": "review", "title": "阶段性复习", "duration": 30}
                ]
            }
        ]
    
    def _design_intermediate_path(self, goal: LearningGoal, user_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """设计中级学习路径"""
        return [
            {
                "name": "技能提升",
                "duration_weeks": 6,
                "focus": "进阶技能和最佳实践",
                "tasks": [
                    {"type": "study", "title": "进阶概念学习", "duration": 60},
                    {"type": "practice", "title": "复杂项目实践", "duration": 90},
                    {"type": "review", "title": "代码审查和优化", "duration": 45}
                ]
            },
            {
                "name": "实战应用",
                "duration_weeks": 8,
                "focus": "实际项目应用",
                "tasks": [
                    {"type": "practice", "title": "完整项目开发", "duration": 120},
                    {"type": "assessment", "title": "技能评估", "duration": 60}
                ]
            }
        ]
    
    def _design_advanced_path(self, goal: LearningGoal, user_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """设计高级学习路径"""
        return [
            {
                "name": "高级技能",
                "duration_weeks": 8,
                "focus": "高级特性和架构设计",
                "tasks": [
                    {"type": "study", "title": "高级概念研究", "duration": 90},
                    {"type": "practice", "title": "架构设计实践", "duration": 120},
                    {"type": "review", "title": "性能优化", "duration": 60}
                ]
            }
        ]
    
    def _design_expert_path(self, goal: LearningGoal, user_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """设计专家级学习路径"""
        return [
            {
                "name": "专家级技能",
                "duration_weeks": 12,
                "focus": "前沿技术和创新",
                "tasks": [
                    {"type": "study", "title": "前沿技术研究", "duration": 120},
                    {"type": "practice", "title": "创新项目开发", "duration": 180},
                    {"type": "assessment", "title": "专家级评估", "duration": 90}
                ]
            }
        ]
    
    def _design_milestones(self, goal: LearningGoal, phases: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """设计学习里程碑"""
        milestones = []
        current_week = 0
        
        for i, phase in enumerate(phases):
            current_week += phase["duration_weeks"]
            milestones.append({
                "week": current_week,
                "title": f"完成{phase['name']}",
                "description": f"掌握{phase['focus']}",
                "reward_points": (i + 1) * 100
            })
        
        return milestones
    
    async def _generate_short_term_plan(self, user_id: int, learning_path: Dict[str, Any], profile: UserProfile) -> LearningPlan:
        """生成短期学习计划（1-4周）"""
        # 获取前2个阶段作为短期计划
        short_term_phases = learning_path["phases"][:2]
        total_weeks = sum(phase["duration_weeks"] for phase in short_term_phases)
        
        start_date = date.today()
        end_date = start_date + timedelta(weeks=total_weeks)
        
        plan_data = LearningPlanCreate(
            plan_type=PlanType.SHORT_TERM,
            title="短期学习计划",
            description=f"为期{total_weeks}周的短期学习计划，专注于基础技能掌握",
            start_date=start_date,
            end_date=end_date
        )
        
        plan = LearningPlan(
            user_id=user_id,
            **plan_data.dict()
        )
        
        self.db.add(plan)
        self.db.commit()
        self.db.refresh(plan)
        
        return plan
    
    async def _generate_medium_term_plan(self, user_id: int, learning_path: Dict[str, Any], profile: UserProfile) -> LearningPlan:
        """生成中期学习计划（1-6个月）"""
        # 获取所有阶段作为中期计划
        total_weeks = sum(phase["duration_weeks"] for phase in learning_path["phases"])
        
        start_date = date.today()
        end_date = start_date + timedelta(weeks=total_weeks)
        
        plan_data = LearningPlanCreate(
            plan_type=PlanType.MEDIUM_TERM,
            title="中期学习计划",
            description=f"为期{total_weeks}周的中期学习计划，全面提升技能水平",
            start_date=start_date,
            end_date=end_date
        )
        
        plan = LearningPlan(
            user_id=user_id,
            **plan_data.dict()
        )
        
        self.db.add(plan)
        self.db.commit()
        self.db.refresh(plan)
        
        return plan
    
    async def _generate_long_term_plan(self, user_id: int, learning_path: Dict[str, Any], profile: UserProfile) -> LearningPlan:
        """生成长期学习计划（6个月-2年）"""
        # 长期计划包含职业发展建议
        start_date = date.today()
        end_date = start_date + timedelta(days=365)  # 1年
        
        plan_data = LearningPlanCreate(
            plan_type=PlanType.LONG_TERM,
            title="长期学习计划",
            description="为期1年的长期学习计划，包含职业发展规划和持续学习策略",
            start_date=start_date,
            end_date=end_date
        )
        
        plan = LearningPlan(
            user_id=user_id,
            **plan_data.dict()
        )
        
        self.db.add(plan)
        self.db.commit()
        self.db.refresh(plan)
        
        return plan
    
    async def _generate_learning_tasks(self, plan_id: int, learning_path: Dict[str, Any], profile: UserProfile) -> List[LearningTask]:
        """生成学习任务"""
        tasks = []
        current_date = date.today()
        
        for phase in learning_path["phases"]:
            for task_info in phase["tasks"]:
                # 计算任务截止日期
                due_date = current_date + timedelta(days=7)  # 默认一周后
                
                task_data = LearningTaskCreate(
                    plan_id=plan_id,
                    title=task_info["title"],
                    description=f"学习任务：{task_info['title']}",
                    task_type=TaskType(task_info["type"]),
                    difficulty=2,  # 默认中等难度
                    estimated_time=task_info["duration"],
                    due_date=due_date
                )
                
                task = LearningTask(
                    **task_data.dict()
                )
                
                self.db.add(task)
                tasks.append(task)
        
        self.db.commit()
        
        # 刷新所有任务以获取ID
        for task in tasks:
            self.db.refresh(task)
        
        return tasks
    
    def _calculate_estimated_completion_time(self, learning_path: Dict[str, Any], profile: UserProfile) -> int:
        """计算预计完成时间（天）"""
        total_weeks = sum(phase["duration_weeks"] for phase in learning_path["phases"])
        
        # 根据用户每日学习时间调整
        if profile.daily_study_time:
            if profile.daily_study_time < 30:
                total_weeks *= 1.5  # 学习时间少，需要更长时间
            elif profile.daily_study_time > 120:
                total_weeks *= 0.8  # 学习时间多，可以更快完成
        
        return total_weeks * 7  # 转换为天数
    
    def _calculate_confidence_score(self, profile: UserProfile, goals: List[LearningGoal]) -> float:
        """计算AI置信度"""
        confidence = 0.8  # 基础置信度
        
        # 根据用户画像完整性调整
        profile_completeness = 0
        if profile.age:
            profile_completeness += 0.2
        if profile.learning_style:
            profile_completeness += 0.2
        if profile.daily_study_time:
            profile_completeness += 0.2
        if profile.weekly_study_days:
            profile_completeness += 0.2
        if profile.learning_environment:
            profile_completeness += 0.2
        
        confidence *= profile_completeness
        
        # 根据目标明确性调整
        for goal in goals:
            if goal.target_level and goal.target_timeframe:
                confidence += 0.05
        
        return min(confidence, 1.0)  # 确保不超过1.0
    
    def get_user_learning_plans(self, user_id: int) -> List[LearningPlan]:
        """获取用户的学习计划"""
        return self.db.query(LearningPlan).filter(LearningPlan.user_id == user_id).all()
    
    def get_plan_tasks(self, plan_id: int) -> List[LearningTask]:
        """获取计划的学习任务"""
        return self.db.query(LearningTask).filter(LearningTask.plan_id == plan_id).all()
    
    def update_task_status(self, task_id: int, status: str) -> LearningTask:
        """更新任务状态"""
        task = self.db.query(LearningTask).filter(LearningTask.id == task_id).first()
        if task:
            task.status = status
            if status == "completed":
                task.completed_at = datetime.now()
            self.db.commit()
            self.db.refresh(task)
        return task 