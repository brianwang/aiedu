#!/usr/bin/env python3
"""
测试AI功能
"""
import requests
import json

BASE_URL = "http://localhost:8111"

def test_ai_features():
    """测试AI功能"""
    print("🧪 开始测试AI功能...")
    
    # 1. 测试健康检查
    print("\n1. 测试健康检查...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"   状态码: {response.status_code}")
        print(f"   响应: {response.json()}")
    except Exception as e:
        print(f"   ❌ 健康检查失败: {e}")
        return
    
    # 2. 测试登录获取token
    print("\n2. 测试登录...")
    login_data = {
        "username": "testuser2",
        "password": "password123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/v1/login", json=login_data)
        print(f"   状态码: {response.status_code}")
        if response.status_code == 200:
            token = response.json().get("access_token")
            print(f"   ✅ 登录成功，获取到token")
        else:
            print(f"   ❌ 登录失败: {response.json()}")
            return
    except Exception as e:
        print(f"   ❌ 登录请求失败: {e}")
        return
    
    # 设置请求头
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # 3. 测试AI状态
    print("\n3. 测试AI状态...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/ai/ai-status", headers=headers)
        print(f"   状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ AI状态检查成功")
            print(f"   AI可用: {data.get('data', {}).get('ai_available', False)}")
            print(f"   客户端数量: {data.get('data', {}).get('clients_count', 0)}")
            print(f"   可用模型: {data.get('data', {}).get('available_models', [])}")
        else:
            print(f"   ❌ AI状态检查失败: {response.json()}")
    except Exception as e:
        print(f"   ❌ AI状态检查失败: {e}")
    
    # 4. 测试实时问答
    print("\n4. 测试实时问答...")
    qa_data = {
        "question": "什么是人工智能？",
        "context": "",
        "user_level": "intermediate"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/v1/ai/real-time-qa", json=qa_data, headers=headers)
        print(f"   状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ 实时问答成功")
            if data.get('success'):
                answer = data.get('data', {}).get('answer', '')
                print(f"   AI回答: {answer[:100]}...")
            else:
                print(f"   ❌ 问答失败: {data.get('message')}")
        else:
            print(f"   ❌ 实时问答失败: {response.json()}")
    except Exception as e:
        print(f"   ❌ 实时问答失败: {e}")
    
    # 5. 测试智能评分
    print("\n5. 测试智能评分...")
    grading_data = {
        "question_content": "请解释什么是机器学习",
        "standard_answer": "机器学习是人工智能的一个分支，它使计算机能够在没有明确编程的情况下学习和改进。",
        "student_answer": "机器学习是让计算机自己学习的技术",
        "question_type": "short_answer",
        "max_score": 10,
        "student_level": "intermediate"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/v1/ai/smart-grading", json=grading_data, headers=headers)
        print(f"   状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ 智能评分成功")
            if data.get('success'):
                score = data.get('data', {}).get('score', 0)
                print(f"   评分结果: {score}/10")
            else:
                print(f"   ❌ 评分失败: {data.get('message')}")
        else:
            print(f"   ❌ 智能评分失败: {response.json()}")
    except Exception as e:
        print(f"   ❌ 智能评分失败: {e}")
    
    # 6. 测试学习报告
    print("\n6. 测试学习报告...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/ai/learning-report", headers=headers)
        print(f"   状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ 学习报告生成成功")
            if data.get('success'):
                report = data.get('data', {})
                print(f"   学习时长: {report.get('total_study_time', 0)}分钟")
                print(f"   答题数量: {report.get('total_questions', 0)}")
            else:
                print(f"   ❌ 报告生成失败: {data.get('message')}")
        else:
            print(f"   ❌ 学习报告失败: {response.json()}")
    except Exception as e:
        print(f"   ❌ 学习报告失败: {e}")
    
    # 7. 测试学习风格分析
    print("\n7. 测试学习风格分析...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/ai/learning-style", headers=headers)
        print(f"   状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ 学习风格分析成功")
            if data.get('success'):
                style = data.get('data', {})
                print(f"   学习类型: {style.get('style_type', '未知')}")
            else:
                print(f"   ❌ 风格分析失败: {data.get('message')}")
        else:
            print(f"   ❌ 学习风格分析失败: {response.json()}")
    except Exception as e:
        print(f"   ❌ 学习风格分析失败: {e}")
    
    # 8. 测试学习激励
    print("\n8. 测试学习激励...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/ai/learning-motivation", headers=headers)
        print(f"   状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ 学习激励生成成功")
            if data.get('success'):
                motivation = data.get('data', {})
                message = motivation.get('encouragement_message', '')
                print(f"   激励信息: {message[:100]}...")
            else:
                print(f"   ❌ 激励生成失败: {data.get('message')}")
        else:
            print(f"   ❌ 学习激励失败: {response.json()}")
    except Exception as e:
        print(f"   ❌ 学习激励失败: {e}")
    
    print("\n🎉 AI功能测试完成！")

if __name__ == "__main__":
    test_ai_features() 