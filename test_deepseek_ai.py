#!/usr/bin/env python3
"""
DeepSeek AI功能详细测试脚本
验证真实的AI生成能力
"""

import requests
import json
import time

# 配置
BASE_URL = "http://localhost:8111"
API_BASE = f"{BASE_URL}/api/v1"

# 教师用户信息
TEACHER_USER = {
    "username": "ai_teacher_user",
    "password": "test123456"
}

def login_teacher():
    """登录教师用户"""
    print("🔐 登录教师用户...")
    
    url = f"{API_BASE}/login"
    data = {
        "username": TEACHER_USER["username"],
        "password": TEACHER_USER["password"]
    }
    
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            result = response.json()
            token = result.get('access_token')
            if token:
                print("✅ 教师登录成功!")
                return token
            else:
                print("❌ 登录成功但未获取到token")
                return None
        else:
            print(f"❌ 教师登录失败: {response.text}")
            return None
    except Exception as e:
        print(f"❌ 登录异常: {e}")
        return None

def test_deepseek_question_generation(token):
    """测试DeepSeek题目生成功能"""
    print("\n🧪 测试DeepSeek题目生成功能...")
    
    url = f"{API_BASE}/ai/generate-questions"
    params = {
        "subject": "Python编程",
        "difficulty": 3,
        "count": 3
    }
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.post(url, params=params, headers=headers)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            questions = data.get('data', [])
            print(f"✅ 生成题目数量: {len(questions)}")
            
            for i, question in enumerate(questions, 1):
                print(f"\n📝 第{i}题:")
                print(f"   内容: {question.get('content', 'N/A')}")
                print(f"   类型: {question.get('question_type', 'N/A')}")
                print(f"   选项: {question.get('options', 'N/A')}")
                print(f"   答案: {question.get('answer', 'N/A')}")
                print(f"   解析: {question.get('explanation', 'N/A')}")
                print(f"   难度: {question.get('difficulty', 'N/A')}")
        else:
            print(f"❌ 题目生成失败: {response.text}")
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")

def test_deepseek_smart_grading(token):
    """测试DeepSeek智能评分功能"""
    print("\n🧪 测试DeepSeek智能评分功能...")
    
    test_cases = [
        {
            "question_content": "请解释什么是面向对象编程？",
            "standard_answer": "面向对象编程是一种编程范式，它将数据和操作数据的方法封装在对象中，通过继承、封装、多态等特性来组织代码。",
            "student_answer": "面向对象编程就是把数据和函数放在一起，可以继承和重写。",
            "question_type": "short_answer",
            "max_score": 10
        },
        {
            "question_content": "什么是Python的列表推导式？",
            "standard_answer": "列表推导式是Python中一种简洁的创建列表的方法，语法为[expression for item in iterable if condition]。",
            "student_answer": "列表推导式就是用for循环快速创建列表的方法。",
            "question_type": "short_answer", 
            "max_score": 8
        }
    ]
    
    url = f"{API_BASE}/ai/smart-grading"
    headers = {"Authorization": f"Bearer {token}"}
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 测试案例 {i}:")
        print(f"   题目: {test_case['question_content']}")
        print(f"   标准答案: {test_case['standard_answer']}")
        print(f"   学生答案: {test_case['student_answer']}")
        
        try:
            response = requests.post(url, json=test_case, headers=headers)
            print(f"   状态码: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                data = result.get('data', {})
                print(f"   ✅ 评分结果:")
                print(f"      得分: {data.get('score', 'N/A')}")
                print(f"      反馈: {data.get('feedback', 'N/A')}")
                print(f"      准确度: {data.get('accuracy', 'N/A')}%")
                print(f"      建议: {data.get('suggestions', 'N/A')}")
            else:
                print(f"   ❌ 评分失败: {response.text}")
                
        except Exception as e:
            print(f"   ❌ 请求异常: {e}")

def test_deepseek_learning_path(token):
    """测试DeepSeek学习路径推荐功能"""
    print("\n🧪 测试DeepSeek学习路径推荐功能...")
    
    skills = ["机器学习", "Web开发", "数据分析"]
    
    url = f"{API_BASE}/ai/learning-path"
    headers = {"Authorization": f"Bearer {token}"}
    
    for skill in skills:
        print(f"\n🎯 推荐技能: {skill}")
        data = {"target_skill": skill}
        
        try:
            response = requests.post(url, json=data, headers=headers)
            print(f"状态码: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                path_data = result.get('data', {})
                print(f"✅ 学习路径:")
                print(f"   路径名称: {path_data.get('path_name', 'N/A')}")
                print(f"   描述: {path_data.get('description', 'N/A')}")
                print(f"   预计时间: {path_data.get('estimated_time', 'N/A')}小时")
                print(f"   难度: {path_data.get('difficulty', 'N/A')}")
                
                stages = path_data.get('stages', [])
                print(f"   学习阶段 ({len(stages)}个):")
                for j, stage in enumerate(stages, 1):
                    print(f"      {j}. {stage.get('name', 'N/A')} ({stage.get('duration', 'N/A')})")
                    print(f"         目标: {', '.join(stage.get('goals', []))}")
                    print(f"         资源: {', '.join(stage.get('resources', []))}")
            else:
                print(f"❌ 学习路径推荐失败: {response.text}")
                
        except Exception as e:
            print(f"❌ 请求异常: {e}")

def main():
    """主测试函数"""
    print("🚀 开始DeepSeek AI功能详细测试...")
    print("=" * 60)
    
    # 等待服务启动
    print("⏳ 等待服务启动...")
    time.sleep(2)
    
    # 登录教师用户
    token = login_teacher()
    if not token:
        print("❌ 教师登录失败，测试终止")
        return
    
    # 测试各项DeepSeek AI功能
    test_deepseek_question_generation(token)
    test_deepseek_smart_grading(token)
    test_deepseek_learning_path(token)
    
    print("\n" + "=" * 60)
    print("🎉 DeepSeek AI功能详细测试完成!")
    print("\n💡 测试说明:")
    print("- 如果看到真实的AI生成内容，说明DeepSeek API集成成功")
    print("- 如果看到模拟数据，请检查DEEPSEEK_API_KEY配置")
    print("- 所有功能都有降级机制，确保系统稳定性")

if __name__ == "__main__":
    main() 