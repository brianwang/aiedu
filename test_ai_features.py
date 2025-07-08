#!/usr/bin/env python3
"""
AI功能测试脚本
测试所有新增的AI功能是否正常工作
"""

import requests
import json
import time

# 配置
BASE_URL = "http://localhost:8111"
TEST_USER_TOKEN = None

def login_as_teacher():
    """登录为教师用户"""
    global TEST_USER_TOKEN
    
    login_data = {
        "username": "teacher",
        "password": "teacher"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/v1/login", json=login_data)
        if response.status_code == 200:
            data = response.json()
            TEST_USER_TOKEN = data.get("access_token")
            print("✅ 教师登录成功")
            return True
        else:
            print(f"❌ 教师登录失败: {response.status_code}")
            print(f"   错误: {response.text}")
            return False
    except Exception as e:
        print(f"❌ 登录请求失败: {e}")
        return False

def test_ai_feature(feature_name, method, endpoint, data=None, headers=None):
    """测试AI功能"""
    if not TEST_USER_TOKEN:
        print(f"❌ {feature_name}: 未登录")
        return False
    
    if headers is None:
        headers = {"Authorization": f"Bearer {TEST_USER_TOKEN}"}
    
    try:
        if method == "GET":
            response = requests.get(f"{BASE_URL}{endpoint}", headers=headers)
        elif method == "POST":
            response = requests.post(f"{BASE_URL}{endpoint}", data=data, headers=headers)
        else:
            print(f"❌ {feature_name}: 不支持的HTTP方法")
            return False
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ {feature_name}: 成功")
            print(f"   响应: {json.dumps(result, ensure_ascii=False, indent=2)[:200]}...")
            return True
        else:
            print(f"❌ {feature_name}: 失败 (状态码: {response.status_code})")
            print(f"   错误: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ {feature_name}: 请求失败 - {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 开始测试AI功能...")
    print("=" * 50)
    
    # 1. 登录
    if not login_as_teacher():
        print("❌ 无法登录，测试终止")
        return
    
    print("\n📋 测试结果:")
    print("-" * 30)
    
    # 2. 测试智能组卷
    exam_data = {
        "subject": "数学",
        "difficulty": "3",
        "exam_type": "comprehensive",
        "question_distribution": '{"single_choice": 5, "multiple_choice": 3, "fill_blank": 2}'
    }
    test_ai_feature("智能组卷", "POST", "/api/v1/ai/generate-exam", data=exam_data)
    
    # 3. 测试学习分析报告
    test_ai_feature("学习分析报告", "GET", "/api/v1/ai/learning-report")
    
    # 4. 测试错题分析
    wrong_question_data = {
        "question_content": "求解方程 2x + 3 = 7",
        "user_answer": "x = 3",
        "correct_answer": "x = 2",
        "subject": "数学"
    }
    test_ai_feature("错题分析", "POST", "/api/v1/ai/analyze-wrong-question", data=wrong_question_data)
    
    # 5. 测试学习激励
    test_ai_feature("学习激励", "GET", "/api/v1/ai/learning-motivation")
    
    # 6. 测试学习风格识别
    test_ai_feature("学习风格识别", "GET", "/api/v1/ai/learning-style")
    
    # 7. 测试题目推荐
    test_ai_feature("题目推荐", "GET", "/api/v1/ai/recommend-questions?subject=数学&count=5")
    
    # 8. 测试学习计划
    plan_data = {
        "subject": "数学",
        "goal": "提高代数运算能力",
        "duration": 30
    }
    test_ai_feature("学习计划", "POST", "/api/v1/ai/create-study-plan", data=plan_data)
    
    # 9. 测试学习模式分析
    test_ai_feature("学习模式分析", "GET", "/api/v1/ai/analyze-learning-pattern")
    
    print("\n" + "=" * 50)
    print("🎉 AI功能测试完成！")
    print("\n💡 提示:")
    print("- 如果某些功能显示失败，可能是因为数据库中没有足够的学习数据")
    print("- 建议先进行一些学习活动，然后再测试分析功能")
    print("- 所有功能都有降级方案，即使AI服务不可用也能正常工作")

if __name__ == "__main__":
    main() 