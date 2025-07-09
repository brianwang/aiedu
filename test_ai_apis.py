#!/usr/bin/env python3
"""
测试AI API功能
"""

import requests
import json
from datetime import datetime

# 配置
BASE_URL = "http://localhost:8111"
API_BASE = f"{BASE_URL}/api/v1"

def test_login():
    """测试登录获取token"""
    print("🔐 测试登录...")
    
    login_data = {
        "username": "student1",
        "password": "password123"
    }
    
    try:
        response = requests.post(f"{API_BASE}/auth/login", json=login_data)
        print(f"登录响应状态: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"登录响应: {json.dumps(data, indent=2, ensure_ascii=False)}")
            if data.get("success"):
                return data["data"]["access_token"]
        else:
            print(f"登录失败: {response.text}")
    except Exception as e:
        print(f"登录异常: {e}")
    
    return None

def test_ability_assessment(token):
    """测试学习能力评估"""
    print("\n📊 测试学习能力评估...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # 模拟用户数据
    assessment_data = {
        "study_time": 120,
        "questions_completed": 50,
        "accuracy": 75.0,
        "subjects": ["数学", "英语"],
        "wrong_questions_distribution": {
            "数学": 8,
            "英语": 4
        }
    }
    
    try:
        response = requests.post(f"{API_BASE}/ai/ability-assessment", 
                               json=assessment_data, headers=headers)
        print(f"能力评估响应状态: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"能力评估响应: {json.dumps(data, indent=2, ensure_ascii=False)}")
            return True
        else:
            print(f"能力评估失败: {response.text}")
    except Exception as e:
        print(f"能力评估异常: {e}")
    
    return False

def test_learning_style(token):
    """测试学习风格分析"""
    print("\n🎨 测试学习风格分析...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # 模拟用户数据
    style_data = {
        "time_distribution": {
            "上午": 30,
            "下午": 40,
            "晚上": 30
        },
        "question_type_preference": {
            "single_choice": 40,
            "multiple_choice": 30,
            "fill_blank": 20,
            "short_answer": 10
        },
        "learning_mode": "visual",
        "review_frequency": 3,
        "wrong_question_handling": "immediate"
    }
    
    try:
        response = requests.post(f"{API_BASE}/ai/learning-style", 
                               json=style_data, headers=headers)
        print(f"学习风格分析响应状态: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"学习风格分析响应: {json.dumps(data, indent=2, ensure_ascii=False)}")
            return True
        else:
            print(f"学习风格分析失败: {response.text}")
    except Exception as e:
        print(f"学习风格分析异常: {e}")
    
    return False

def test_ai_routes():
    """测试AI路由是否可用"""
    print("\n🔍 测试AI路由...")
    
    try:
        # 测试健康检查
        response = requests.get(f"{BASE_URL}/health")
        print(f"健康检查状态: {response.status_code}")
        
        # 测试API文档
        response = requests.get(f"{BASE_URL}/docs")
        print(f"API文档状态: {response.status_code}")
        
        # 测试AI路由前缀
        response = requests.get(f"{API_BASE}/ai/recommendations")
        print(f"AI推荐路由状态: {response.status_code}")
        
    except Exception as e:
        print(f"路由测试异常: {e}")

def main():
    """主测试函数"""
    print("=" * 60)
    print("AI API功能测试")
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"API地址: {BASE_URL}")
    print("=" * 60)
    
    # 测试路由
    test_ai_routes()
    
    # 测试登录
    token = test_login()
    if not token:
        print("\n❌ 登录失败，无法继续测试")
        return
    
    # 测试功能
    results = []
    results.append(test_ability_assessment(token))
    results.append(test_learning_style(token))
    
    # 总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    success_rate = (passed / total) * 100
    
    print(f"总测试数: {total}")
    print(f"通过数: {passed}")
    print(f"失败数: {total - passed}")
    print(f"成功率: {success_rate:.1f}%")
    
    if success_rate >= 80:
        print("🎉 AI API功能测试基本通过！")
    elif success_rate >= 60:
        print("⚠️  AI API功能测试部分通过，需要进一步优化")
    else:
        print("❌ AI API功能测试失败较多，需要重点修复")

if __name__ == "__main__":
    main() 