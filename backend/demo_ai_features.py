#!/usr/bin/env python3
"""
AI功能演示脚本
"""
import requests
import json
import time

BASE_URL = "http://localhost:8111"

def demo_ai_features():
    """演示AI功能"""
    print("🤖 AI智能教育平台 - 功能演示")
    print("=" * 50)
    
    # 登录获取token
    print("\n1. 用户登录...")
    login_data = {
        "username": "testuser2",
        "password": "password123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/v1/login", json=login_data)
        if response.status_code == 200:
            token = response.json().get("access_token")
            print("✅ 登录成功")
        else:
            print("❌ 登录失败")
            return
    except Exception as e:
        print(f"❌ 登录失败: {e}")
        return
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # 演示实时问答
    print("\n2. 智能问答演示...")
    questions = [
        "什么是人工智能？",
        "机器学习有哪些类型？",
        "深度学习与传统机器学习有什么区别？",
        "如何提高学习效率？"
    ]
    
    for i, question in enumerate(questions, 1):
        print(f"\n   问题 {i}: {question}")
        try:
            response = requests.post(f"{BASE_URL}/api/v1/ai/real-time-qa", 
                                   json={"question": question, "context": "", "user_level": "intermediate"}, 
                                   headers=headers)
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    answer = data.get('data', {}).get('answer', '')
                    print(f"   AI回答: {answer[:150]}...")
                else:
                    print(f"   ❌ 问答失败: {data.get('message')}")
            else:
                print(f"   ❌ 请求失败: {response.status_code}")
        except Exception as e:
            print(f"   ❌ 请求异常: {e}")
        
        time.sleep(1)  # 避免请求过快
    
    # 演示智能评分
    print("\n3. 智能评分演示...")
    grading_examples = [
        {
            "question": "请解释什么是机器学习",
            "standard_answer": "机器学习是人工智能的一个分支，它使计算机能够在没有明确编程的情况下学习和改进。",
            "student_answer": "机器学习是让计算机自己学习的技术，通过数据训练来改进性能。",
            "score": 10
        },
        {
            "question": "什么是深度学习？",
            "standard_answer": "深度学习是机器学习的一个子集，使用多层神经网络来模拟人脑的学习过程。",
            "student_answer": "深度学习就是很深的网络",
            "score": 10
        }
    ]
    
    for i, example in enumerate(grading_examples, 1):
        print(f"\n   评分示例 {i}:")
        print(f"   题目: {example['question']}")
        print(f"   学生答案: {example['student_answer']}")
        
        try:
            response = requests.post(f"{BASE_URL}/api/v1/ai/smart-grading", 
                                   json={
                                       "question_content": example['question'],
                                       "standard_answer": example['standard_answer'],
                                       "student_answer": example['student_answer'],
                                       "question_type": "short_answer",
                                       "max_score": example['score'],
                                       "student_level": "intermediate"
                                   }, 
                                   headers=headers)
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    result = data.get('data', {})
                    score = result.get('score', 0)
                    accuracy = result.get('accuracy_score', 0)
                    print(f"   评分结果: {score}/{example['score']} (准确率: {accuracy}%)")
                    
                    # 显示反馈
                    feedback = result.get('detailed_feedback', {})
                    if feedback.get('strengths'):
                        print(f"   优点: {', '.join(feedback['strengths'][:2])}")
                    if feedback.get('weaknesses'):
                        print(f"   不足: {', '.join(feedback['weaknesses'][:2])}")
                else:
                    print(f"   ❌ 评分失败: {data.get('message')}")
            else:
                print(f"   ❌ 请求失败: {response.status_code}")
        except Exception as e:
            print(f"   ❌ 请求异常: {e}")
        
        time.sleep(1)
    
    # 演示学习分析
    print("\n4. 学习分析演示...")
    analysis_endpoints = [
        ("学习报告", "/api/v1/ai/learning-report"),
        ("学习风格", "/api/v1/ai/learning-style"),
        ("学习激励", "/api/v1/ai/learning-motivation")
    ]
    
    for name, endpoint in analysis_endpoints:
        print(f"\n   {name}分析:")
        try:
            response = requests.get(f"{BASE_URL}{endpoint}", headers=headers)
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    result = data.get('data', {})
                    if name == "学习报告":
                        print(f"   学习时长: {result.get('total_study_time', 0)}分钟")
                        print(f"   答题数量: {result.get('total_questions', 0)}")
                        print(f"   学习建议: {result.get('suggestions', '无')[:100]}...")
                    elif name == "学习风格":
                        print(f"   学习类型: {result.get('style_type', '未知')}")
                        print(f"   特点: {', '.join(result.get('characteristics', [])[:3])}")
                    elif name == "学习激励":
                        print(f"   激励信息: {result.get('encouragement_message', '')[:100]}...")
                else:
                    print(f"   ❌ 分析失败: {data.get('message')}")
            else:
                print(f"   ❌ 请求失败: {response.status_code}")
        except Exception as e:
            print(f"   ❌ 请求异常: {e}")
        
        time.sleep(1)
    
    print("\n" + "=" * 50)
    print("🎉 AI功能演示完成！")
    print("\n💡 提示:")
    print("   - 要使用真实的AI功能，请在.env文件中配置DeepSeek API密钥")
    print("   - 当前演示使用的是降级方案（模拟数据）")
    print("   - 前端界面在 http://localhost:5173/ai 可以体验完整功能")

if __name__ == "__main__":
    demo_ai_features() 