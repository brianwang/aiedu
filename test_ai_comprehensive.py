#!/usr/bin/env python3
"""
AI智能教育平台 - 全面功能测试脚本
测试所有AI相关接口的功能、异常处理和降级方案
"""

import asyncio
import json
import requests
import time
from typing import Dict, List, Optional
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AITestSuite:
    def __init__(self, base_url: str = "http://localhost:8111"):
        self.base_url = base_url
        self.session = requests.Session()
        self.token = None
        self.test_results = []
        
    def log_test(self, test_name: str, success: bool, message: str = "", data: Dict = None):
        """记录测试结果"""
        result = {
            "test_name": test_name,
            "success": success,
            "message": message,
            "data": data,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        logger.info(f"{status} {test_name}: {message}")
        
        if data and not success:
            logger.error(f"错误详情: {json.dumps(data, ensure_ascii=False, indent=2)}")

    async def login(self, username: str = "teststudent", password: str = "teststudent"):
        """登录获取token"""
        try:
            response = self.session.post(
                f"{self.base_url}/api/v1/auth/login",
                json={"username": username, "password": password}
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    self.token = data["data"]["access_token"]
                    self.session.headers.update({"Authorization": f"Bearer {self.token}"})
                    self.log_test("用户登录", True, f"成功登录用户: {username}")
                    return True
                else:
                    self.log_test("用户登录", False, f"登录失败: {data.get('message', '未知错误')}")
                    return False
            else:
                self.log_test("用户登录", False, f"HTTP错误: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("用户登录", False, f"登录异常: {str(e)}")
            return False

    async def test_ai_recommendations(self):
        """测试AI题目推荐功能"""
        try:
            response = self.session.get(f"{self.base_url}/api/v1/ai/recommendations?count=5")
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    questions = data.get("data", [])
                    self.log_test("AI题目推荐", True, f"成功推荐{len(questions)}道题目")
                    return True
                else:
                    self.log_test("AI题目推荐", False, f"推荐失败: {data.get('message', '未知错误')}")
                    return False
            else:
                self.log_test("AI题目推荐", False, f"HTTP错误: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("AI题目推荐", False, f"推荐异常: {str(e)}")
            return False

    async def test_study_plan(self):
        """测试学习计划生成功能"""
        try:
            response = self.session.get(f"{self.base_url}/api/v1/ai/study-plan")
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    plan = data.get("data", {})
                    self.log_test("学习计划生成", True, "成功生成个性化学习计划")
                    return True
                else:
                    self.log_test("学习计划生成", False, f"生成失败: {data.get('message', '未知错误')}")
                    return False
            else:
                self.log_test("学习计划生成", False, f"HTTP错误: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("学习计划生成", False, f"生成异常: {str(e)}")
            return False

    async def test_learning_pattern(self):
        """测试学习模式分析功能"""
        try:
            response = self.session.get(f"{self.base_url}/api/v1/ai/learning-pattern")
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    pattern = data.get("data", {})
                    self.log_test("学习模式分析", True, "成功分析学习模式")
                    return True
                else:
                    self.log_test("学习模式分析", False, f"分析失败: {data.get('message', '未知错误')}")
                    return False
            else:
                self.log_test("学习模式分析", False, f"HTTP错误: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("学习模式分析", False, f"分析异常: {str(e)}")
            return False

    async def test_difficulty_analysis(self):
        """测试难度分析功能"""
        try:
            response = self.session.get(f"{self.base_url}/api/v1/ai/difficulty-analysis")
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    analysis = data.get("data", {})
                    self.log_test("难度分析", True, f"正确率: {analysis.get('accuracy', 0)}%")
                    return True
                else:
                    self.log_test("难度分析", False, f"分析失败: {data.get('message', '未知错误')}")
                    return False
            else:
                self.log_test("难度分析", False, f"HTTP错误: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("难度分析", False, f"分析异常: {str(e)}")
            return False

    async def test_smart_grading(self):
        """测试智能评分功能"""
        try:
            grading_data = {
                "question_content": "请解释什么是人工智能？",
                "standard_answer": "人工智能是计算机科学的一个分支，旨在创建能够执行通常需要人类智能的任务的系统。",
                "student_answer": "人工智能是让机器像人一样思考的技术。",
                "question_type": "short_answer",
                "max_score": 10
            }
            
            response = self.session.post(
                f"{self.base_url}/api/v1/ai/smart-grading",
                json=grading_data
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    result = data.get("data", {})
                    score = result.get("score", 0)
                    self.log_test("智能评分", True, f"评分结果: {score}分")
                    return True
                else:
                    self.log_test("智能评分", False, f"评分失败: {data.get('message', '未知错误')}")
                    return False
            else:
                self.log_test("智能评分", False, f"HTTP错误: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("智能评分", False, f"评分异常: {str(e)}")
            return False

    async def test_ability_assessment(self):
        """测试学习能力评估功能"""
        try:
            assessment_data = {
                "study_time": 120,
                "questions_completed": 50,
                "accuracy": 85.5,
                "subjects": ["数学", "物理"],
                "wrong_questions_distribution": {"数学": 3, "物理": 2}
            }
            
            response = self.session.post(
                f"{self.base_url}/api/v1/ai/ability-assessment",
                json=assessment_data
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    result = data.get("data", {})
                    level = result.get("overall_level", "未知")
                    self.log_test("学习能力评估", True, f"能力等级: {level}")
                    return True
                else:
                    self.log_test("学习能力评估", False, f"评估失败: {data.get('message', '未知错误')}")
                    return False
            else:
                self.log_test("学习能力评估", False, f"HTTP错误: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("学习能力评估", False, f"评估异常: {str(e)}")
            return False

    async def test_learning_style(self):
        """测试学习风格分析功能"""
        try:
            style_data = {
                "time_distribution": {"9": 60, "14": 90, "20": 120},
                "question_type_preference": {"single_choice": 40, "multiple_choice": 30, "fill_blank": 20, "short_answer": 10},
                "learning_mode": "continuous",
                "review_frequency": 3,
                "wrong_question_handling": "review_frequently"
            }
            
            response = self.session.post(
                f"{self.base_url}/api/v1/ai/learning-style",
                json=style_data
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    result = data.get("data", {})
                    style_type = result.get("style_type", "未知")
                    self.log_test("学习风格分析", True, f"学习风格: {style_type}")
                    return True
                else:
                    self.log_test("学习风格分析", False, f"分析失败: {data.get('message', '未知错误')}")
                    return False
            else:
                self.log_test("学习风格分析", False, f"HTTP错误: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("学习风格分析", False, f"分析异常: {str(e)}")
            return False

    async def test_motivation_plan(self):
        """测试学习动机激励功能"""
        try:
            motivation_data = {
                "learning_status": "steady",
                "learning_difficulties": ["注意力不集中", "时间管理"],
                "learning_goals": ["提高数学成绩", "掌握物理概念"],
                "learning_achievements": ["完成50道题目", "连续学习7天"],
                "personal_characteristics": ["有毅力", "喜欢挑战"]
            }
            
            response = self.session.post(
                f"{self.base_url}/api/v1/ai/motivation",
                json=motivation_data
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    result = data.get("data", {})
                    self.log_test("学习动机激励", True, "成功生成激励方案")
                    return True
                else:
                    self.log_test("学习动机激励", False, f"生成失败: {data.get('message', '未知错误')}")
                    return False
            else:
                self.log_test("学习动机激励", False, f"HTTP错误: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("学习动机激励", False, f"生成异常: {str(e)}")
            return False

    async def test_user_ability_assessment(self):
        """测试用户能力评估功能"""
        try:
            response = self.session.get(f"{self.base_url}/api/v1/ai/user-ability-assessment")
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    result = data.get("data", {})
                    level = result.get("overall_level", "未知")
                    self.log_test("用户能力评估", True, f"能力等级: {level}")
                    return True
                else:
                    self.log_test("用户能力评估", False, f"评估失败: {data.get('message', '未知错误')}")
                    return False
            else:
                self.log_test("用户能力评估", False, f"HTTP错误: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("用户能力评估", False, f"评估异常: {str(e)}")
            return False

    async def test_user_learning_style(self):
        """测试用户学习风格识别功能"""
        try:
            response = self.session.get(f"{self.base_url}/api/v1/ai/user-learning-style")
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    result = data.get("data", {})
                    self.log_test("用户学习风格识别", True, "成功识别学习风格")
                    return True
                else:
                    self.log_test("用户学习风格识别", False, f"识别失败: {data.get('message', '未知错误')}")
                    return False
            else:
                self.log_test("用户学习风格识别", False, f"HTTP错误: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("用户学习风格识别", False, f"识别异常: {str(e)}")
            return False

    async def test_learning_path(self):
        """测试学习路径推荐功能"""
        try:
            path_data = {"target_skill": "数学分析"}
            
            response = self.session.post(
                f"{self.base_url}/api/v1/ai/learning-path",
                json=path_data
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    result = data.get("data", {})
                    self.log_test("学习路径推荐", True, "成功推荐学习路径")
                    return True
                else:
                    self.log_test("学习路径推荐", False, f"推荐失败: {data.get('message', '未知错误')}")
                    return False
            else:
                self.log_test("学习路径推荐", False, f"HTTP错误: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("学习路径推荐", False, f"推荐异常: {str(e)}")
            return False

    async def test_generate_exam(self):
        """测试AI组卷功能"""
        try:
            exam_data = {
                "subject": "数学",
                "difficulty": 3,
                "exam_type": "单元测试",
                "question_distribution": json.dumps({
                    "single_choice": 10,
                    "multiple_choice": 5,
                    "fill_blank": 5,
                    "short_answer": 3
                })
            }
            
            response = self.session.post(
                f"{self.base_url}/api/v1/ai/generate-exam",
                data=exam_data
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    result = data.get("data", {})
                    self.log_test("AI组卷", True, "成功生成试卷")
                    return True
                else:
                    self.log_test("AI组卷", False, f"组卷失败: {data.get('message', '未知错误')}")
                    return False
            else:
                self.log_test("AI组卷", False, f"HTTP错误: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("AI组卷", False, f"组卷异常: {str(e)}")
            return False

    async def test_learning_report(self):
        """测试学习报告生成功能"""
        try:
            response = self.session.get(f"{self.base_url}/api/v1/ai/learning-report")
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    result = data.get("data", {})
                    self.log_test("学习报告生成", True, "成功生成学习报告")
                    return True
                else:
                    self.log_test("学习报告生成", False, f"生成失败: {data.get('message', '未知错误')}")
                    return False
            else:
                self.log_test("学习报告生成", False, f"HTTP错误: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("学习报告生成", False, f"生成异常: {str(e)}")
            return False

    async def test_analyze_wrong_question(self):
        """测试错题分析功能"""
        try:
            wrong_data = {
                "question_content": "求解方程：2x + 3 = 7",
                "user_answer": "x = 3",
                "correct_answer": "x = 2",
                "subject": "数学"
            }
            
            response = self.session.post(
                f"{self.base_url}/api/v1/ai/analyze-wrong-question",
                data=wrong_data
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    result = data.get("data", {})
                    self.log_test("错题分析", True, "成功分析错题")
                    return True
                else:
                    self.log_test("错题分析", False, f"分析失败: {data.get('message', '未知错误')}")
                    return False
            else:
                self.log_test("错题分析", False, f"HTTP错误: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("错题分析", False, f"分析异常: {str(e)}")
            return False

    async def test_learning_motivation(self):
        """测试学习激励生成功能"""
        try:
            response = self.session.get(f"{self.base_url}/api/v1/ai/learning-motivation")
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    result = data.get("data", {})
                    self.log_test("学习激励生成", True, "成功生成学习激励")
                    return True
                else:
                    self.log_test("学习激励生成", False, f"生成失败: {data.get('message', '未知错误')}")
                    return False
            else:
                self.log_test("学习激励生成", False, f"HTTP错误: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("学习激励生成", False, f"生成异常: {str(e)}")
            return False

    async def test_identify_learning_style(self):
        """测试学习风格识别功能"""
        try:
            response = self.session.get(f"{self.base_url}/api/v1/ai/learning-style")
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    result = data.get("data", {})
                    self.log_test("学习风格识别", True, "成功识别学习风格")
                    return True
                else:
                    self.log_test("学习风格识别", False, f"识别失败: {data.get('message', '未知错误')}")
                    return False
            else:
                self.log_test("学习风格识别", False, f"HTTP错误: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("学习风格识别", False, f"识别异常: {str(e)}")
            return False

    async def run_all_tests(self):
        """运行所有测试"""
        logger.info("🚀 开始AI功能全面测试...")
        
        # 登录测试
        if not await self.login():
            logger.error("❌ 登录失败，无法继续测试")
            return
        
        # 定义所有测试方法
        test_methods = [
            ("AI题目推荐", self.test_ai_recommendations),
            ("学习计划生成", self.test_study_plan),
            ("学习模式分析", self.test_learning_pattern),
            ("难度分析", self.test_difficulty_analysis),
            ("智能评分", self.test_smart_grading),
            ("学习能力评估", self.test_ability_assessment),
            ("学习风格分析", self.test_learning_style),
            ("学习动机激励", self.test_motivation_plan),
            ("用户能力评估", self.test_user_ability_assessment),
            ("用户学习风格", self.test_user_learning_style),
            ("学习路径推荐", self.test_learning_path),
            ("AI组卷", self.test_generate_exam),
            ("学习报告生成", self.test_learning_report),
            ("错题分析", self.test_analyze_wrong_question),
            ("学习激励生成", self.test_learning_motivation),
            ("学习风格识别", self.test_identify_learning_style),
        ]
        
        # 执行所有测试
        for test_name, test_method in test_methods:
            try:
                await test_method()
                await asyncio.sleep(0.5)  # 避免请求过于频繁
            except Exception as e:
                self.log_test(test_name, False, f"测试执行异常: {str(e)}")
        
        # 生成测试报告
        self.generate_test_report()

    def generate_test_report(self):
        """生成测试报告"""
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - passed_tests
        
        logger.info("\n" + "="*60)
        logger.info("📊 AI功能测试报告")
        logger.info("="*60)
        logger.info(f"总测试数: {total_tests}")
        logger.info(f"通过测试: {passed_tests} ✅")
        logger.info(f"失败测试: {failed_tests} ❌")
        logger.info(f"通过率: {(passed_tests/total_tests*100):.1f}%")
        
        if failed_tests > 0:
            logger.info("\n❌ 失败的测试:")
            for result in self.test_results:
                if not result["success"]:
                    logger.info(f"  - {result['test_name']}: {result['message']}")
        
        logger.info("\n✅ 通过的测试:")
        for result in self.test_results:
            if result["success"]:
                logger.info(f"  - {result['test_name']}: {result['message']}")
        
        # 保存详细报告到文件
        report_file = "ai_test_report.json"
        with open(report_file, "w", encoding="utf-8") as f:
            json.dump({
                "summary": {
                    "total_tests": total_tests,
                    "passed_tests": passed_tests,
                    "failed_tests": failed_tests,
                    "pass_rate": round(passed_tests/total_tests*100, 1)
                },
                "test_results": self.test_results
            }, f, ensure_ascii=False, indent=2)
        
        logger.info(f"\n📄 详细测试报告已保存到: {report_file}")
        logger.info("="*60)

async def main():
    """主函数"""
    # 创建测试套件
    test_suite = AITestSuite()
    
    # 运行所有测试
    await test_suite.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main()) 