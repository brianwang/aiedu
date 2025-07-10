import asyncio
import logging
from typing import Dict, List, Any
from sqlalchemy.orm import Session
from database import get_db
from app.models.user import User
from app.services.question_generator import QuestionGenerator
from app.services.learning_report_service import LearningReportService
from datetime import datetime, timedelta
import schedule
import time
import threading

logger = logging.getLogger(__name__)


class SchedulerService:
    def __init__(self):
        self.running = False
        self.scheduler_thread = None
    
    def start(self):
        """启动定时任务服务"""
        if self.running:
            logger.warning("定时任务服务已在运行")
            return
        
        self.running = True
        
        # 设置定时任务
        schedule.every().day.at("06:00").do(self._daily_question_generation)
        schedule.every().day.at("20:00").do(self._daily_report_generation)
        schedule.every().hour.do(self._hourly_cleanup)
        
        # 启动调度器线程
        self.scheduler_thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self.scheduler_thread.start()
        
        logger.info("定时任务服务启动成功")
    
    def stop(self):
        """停止定时任务服务"""
        self.running = False
        if self.scheduler_thread:
            self.scheduler_thread.join(timeout=5)
        logger.info("定时任务服务已停止")
    
    def _run_scheduler(self):
        """运行调度器"""
        while self.running:
            try:
                schedule.run_pending()
                time.sleep(60)  # 每分钟检查一次
            except Exception as e:
                logger.error(f"调度器运行错误: {str(e)}")
                time.sleep(60)
    
    def _daily_question_generation(self):
        """每日题目生成任务"""
        try:
            logger.info("开始执行每日题目生成任务")
            
            # 创建数据库会话
            db = next(get_db())
            
            # 创建题目生成器
            generator = QuestionGenerator(db)
            
            # 异步执行题目生成
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                result = loop.run_until_complete(generator.generate_daily_questions())
                logger.info(f"每日题目生成完成: {result}")
            finally:
                loop.close()
                db.close()
                
        except Exception as e:
            logger.error(f"每日题目生成任务失败: {str(e)}")
    
    def _daily_report_generation(self):
        """每日学习报告生成任务"""
        try:
            logger.info("开始执行每日学习报告生成任务")
            
            # 创建数据库会话
            db = next(get_db())
            
            # 获取所有活跃用户
            users = db.query(User).filter(User.is_active == True).all()
            
            # 创建报告服务
            report_service = LearningReportService(db)
            
            # 异步执行报告生成
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                for user in users:
                    try:
                        report = loop.run_until_complete(report_service.generate_daily_report(user.id))
                        logger.info(f"为用户 {user.username} 生成每日报告成功")
                        
                        # 这里可以添加报告存储或发送逻辑
                        self._store_daily_report(user.id, report)
                        
                    except Exception as e:
                        logger.error(f"为用户 {user.username} 生成报告失败: {str(e)}")
                        continue
                        
            finally:
                loop.close()
                db.close()
                
            logger.info("每日学习报告生成任务完成")
            
        except Exception as e:
            logger.error(f"每日学习报告生成任务失败: {str(e)}")
    
    def _hourly_cleanup(self):
        """每小时清理任务"""
        try:
            logger.info("开始执行每小时清理任务")
            
            # 创建数据库会话
            db = next(get_db())
            
            try:
                # 清理过期的缓存数据
                self._cleanup_expired_cache(db)
                
                # 清理过期的学习记录
                self._cleanup_old_learning_records(db)
                
                # 更新用户活跃状态
                self._update_user_activity_status(db)
                
            finally:
                db.close()
                
            logger.info("每小时清理任务完成")
            
        except Exception as e:
            logger.error(f"每小时清理任务失败: {str(e)}")
    
    def _store_daily_report(self, user_id: int, report: Dict[str, Any]):
        """存储每日报告"""
        try:
            # 这里可以实现报告存储逻辑
            # 例如：存储到数据库、发送邮件、推送到消息队列等
            
            # 示例：存储到文件系统
            import json
            import os
            
            reports_dir = "reports/daily"
            os.makedirs(reports_dir, exist_ok=True)
            
            filename = f"{reports_dir}/user_{user_id}_{report['date']}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            
            logger.info(f"每日报告已存储: {filename}")
            
        except Exception as e:
            logger.error(f"存储每日报告失败: {str(e)}")
    
    def _cleanup_expired_cache(self, db: Session):
        """清理过期缓存"""
        try:
            # 这里可以清理AI服务缓存、用户会话缓存等
            # 示例：清理超过24小时的缓存数据
            
            from app.services.ai_service import AIService
            ai_service = AIService()
            
            # 清理AI服务缓存
            current_time = datetime.now().timestamp()
            expired_keys = []
            
            for key, (data, timestamp) in ai_service._cache.items():
                if current_time - timestamp > 86400:  # 24小时
                    expired_keys.append(key)
            
            for key in expired_keys:
                del ai_service._cache[key]
            
            if expired_keys:
                logger.info(f"清理了 {len(expired_keys)} 个过期缓存")
                
        except Exception as e:
            logger.error(f"清理过期缓存失败: {str(e)}")
    
    def _cleanup_old_learning_records(self, db: Session):
        """清理旧的学习记录"""
        try:
            from app.models.learning import LearningProgress
            
            # 删除超过90天的学习记录
            cutoff_date = datetime.now() - timedelta(days=90)
            
            deleted_count = db.query(LearningProgress).filter(
                LearningProgress.created_at < cutoff_date
            ).delete()
            
            db.commit()
            
            if deleted_count > 0:
                logger.info(f"清理了 {deleted_count} 条旧学习记录")
                
        except Exception as e:
            logger.error(f"清理旧学习记录失败: {str(e)}")
            db.rollback()
    
    def _update_user_activity_status(self, db: Session):
        """更新用户活跃状态"""
        try:
            # 将超过30天未登录的用户标记为非活跃
            cutoff_date = datetime.now() - timedelta(days=30)
            
            inactive_users = db.query(User).filter(
                User.last_login < cutoff_date,
                User.is_active == True
            ).all()
            
            for user in inactive_users:
                user.is_active = False
            
            db.commit()
            
            if inactive_users:
                logger.info(f"将 {len(inactive_users)} 个用户标记为非活跃")
                
        except Exception as e:
            logger.error(f"更新用户活跃状态失败: {str(e)}")
            db.rollback()
    
    def run_manual_task(self, task_name: str, **kwargs) -> Dict[str, Any]:
        """手动执行任务"""
        try:
            logger.info(f"手动执行任务: {task_name}")
            
            if task_name == "generate_questions":
                return self._manual_question_generation(**kwargs)
            elif task_name == "generate_reports":
                return self._manual_report_generation(**kwargs)
            elif task_name == "cleanup":
                return self._manual_cleanup(**kwargs)
            else:
                return {"success": False, "error": f"未知任务: {task_name}"}
                
        except Exception as e:
            logger.error(f"手动执行任务失败: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def _manual_question_generation(self, subject: str = None, user_id: int = None) -> Dict[str, Any]:
        """手动生成题目"""
        try:
            db = next(get_db())
            generator = QuestionGenerator(db)
            
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                if subject and user_id:
                    # 为特定用户和学科生成题目
                    questions = loop.run_until_complete(
                        generator.generate_questions_for_user(user_id, subject, 10)
                    )
                    result = {"generated": len(questions), "subject": subject, "user_id": user_id}
                elif subject:
                    # 为特定学科生成题目
                    questions = loop.run_until_complete(
                        generator.generate_subject_questions(subject, "medium", 20)
                    )
                    result = {"generated": len(questions), "subject": subject}
                else:
                    # 为所有用户生成每日题目
                    result = loop.run_until_complete(generator.generate_daily_questions())
                
            finally:
                loop.close()
                db.close()
            
            return {"success": True, "result": result}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _manual_report_generation(self, user_id: int = None) -> Dict[str, Any]:
        """手动生成报告"""
        try:
            db = next(get_db())
            report_service = LearningReportService(db)
            
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                if user_id:
                    # 为特定用户生成报告
                    report = loop.run_until_complete(report_service.generate_daily_report(user_id))
                    result = {"user_id": user_id, "report": report}
                else:
                    # 为所有用户生成报告
                    users = db.query(User).filter(User.is_active == True).all()
                    reports = []
                    
                    for user in users:
                        try:
                            report = loop.run_until_complete(report_service.generate_daily_report(user.id))
                            reports.append({"user_id": user.id, "username": user.username})
                        except Exception as e:
                            logger.error(f"为用户 {user.username} 生成报告失败: {str(e)}")
                    
                    result = {"total_users": len(users), "successful_reports": len(reports)}
                
            finally:
                loop.close()
                db.close()
            
            return {"success": True, "result": result}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _manual_cleanup(self) -> Dict[str, Any]:
        """手动清理"""
        try:
            db = next(get_db())
            
            try:
                self._cleanup_expired_cache(db)
                self._cleanup_old_learning_records(db)
                self._update_user_activity_status(db)
                
                result = {"message": "清理任务完成"}
                
            finally:
                db.close()
            
            return {"success": True, "result": result}
            
        except Exception as e:
            return {"success": False, "error": str(e)}


# 全局调度器实例
scheduler = SchedulerService() 