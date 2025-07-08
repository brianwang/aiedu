#!/usr/bin/env python3
"""
AI功能集成测试脚本
测试deepseek大模型API集成是否正常工作
"""

import requests
import json
import time

# 配置
BASE_URL = "http://localhost:8111"
API_BASE = f"{BASE_URL}/api/v1"

# 测试用户信息
TEST_USER = {
    "username": "ai_teacher_user",
    "email": "ai_teacher@example.com",
    "password": "test123456",
    "role": "teacher"
}

def create_teacher_user():
    """创建教师用户（通过CLI命令）"""
    print("👨‍🏫 创建教师用户...")
    
    try:
        import subprocess
        # 使用add_user.py的quick命令创建教师用户
        result = subprocess.run([
            "python", "add_user.py", "quick",
            TEST_USER["username"],
            TEST_USER["email"], 
            TEST_USER["password"],
            "teacher"
        ], capture_output=True, text=True, cwd="backend")
        
        if result.returncode == 0:
            print("✅ 教师用户创建成功!")
            return True
        elif "already exists" in result.stdout or "already exists" in result.stderr:
            print("ℹ️ 教师用户已存在，继续登录...")
            return True
        else:
            print(f"❌ 教师用户创建失败: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ 创建教师用户异常: {e}")
        return False

def register_user():
    """注册测试用户"""
    print("👤 注册测试用户...")
    
    url = f"{API_BASE}/register"
    data = {
        "username": TEST_USER["username"],
        "email": TEST_USER["email"],
        "password": TEST_USER["password"],
        "confirm_password": TEST_USER["password"]
    }
    
    try:
        response = requests.post(url, json=data)
        if response.status_code == 201:
            print("✅ 用户注册成功!")
            return True
        elif "already exists" in response.text or "duplicate" in response.text:
            print("ℹ️ 用户已存在，继续登录...")
            return True
        else:
            print(f"❌ 用户注册失败: {response.text}")
            return False
    except Exception as e:
        print(f"❌ 注册异常: {e}")
        return False

def login_user():
    """登录测试用户"""
    print("🔐 登录测试用户...")
    
    url = f"{API_BASE}/login"
    data = {
        "username": TEST_USER["username"],
        "password": TEST_USER["password"]
    }
    
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            result = response.json()
            token = result.get('access_token')
            if token:
                print("✅ 用户登录成功!")
                return token
            else:
                print("❌ 登录成功但未获取到token")
                return None
        else:
            print(f"❌ 用户登录失败: {response.text}")
            return None
    except Exception as e:
        print(f"❌ 登录异常: {e}")
        return None

def test_ai_generate_questions(token):
    """测试AI题目生成功能"""
    print("\n🧪 测试AI题目生成功能...")
    
    url = f"{API_BASE}/ai/generate-questions"
    params = {
        "subject": "数学",
        "difficulty": 3,
        "count": 5
    }
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.post(url, params=params, headers=headers)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ 题目生成成功!")
            print(f"生成题目数量: {len(data.get('data', []))}")
            if data.get('data'):
                print(f"第一题内容: {data['data'][0].get('content', 'N/A')[:50]}...")
        else:
            print(f"❌ 题目生成失败: {response.text}")
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")

def test_ai_smart_grading(token):
    """测试AI智能评分功能"""
    print("\n🧪 测试AI智能评分功能...")
    
    url = f"{API_BASE}/ai/smart-grading"
    data = {
        "question_content": "什么是Python？",
        "standard_answer": "Python是一种高级编程语言，具有简洁的语法和强大的功能。",
        "student_answer": "Python是一种编程语言，语法简单。",
        "question_type": "short_answer",
        "max_score": 10
    }
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.post(url, json=data, headers=headers)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 智能评分成功!")
            print(f"得分: {result.get('data', {}).get('score', 'N/A')}")
            print(f"反馈: {result.get('data', {}).get('feedback', 'N/A')}")
        else:
            print(f"❌ 智能评分失败: {response.text}")
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")

def test_ai_learning_path(token):
    """测试AI学习路径推荐功能"""
    print("\n🧪 测试AI学习路径推荐功能...")
    
    url = f"{API_BASE}/ai/learning-path"
    data = {
        "target_skill": "Python编程"
    }
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.post(url, json=data, headers=headers)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 学习路径推荐成功!")
            path_data = result.get('data', {})
            print(f"路径名称: {path_data.get('path_name', 'N/A')}")
            print(f"预计时间: {path_data.get('estimated_time', 'N/A')}小时")
            stages = path_data.get('stages', [])
            print(f"学习阶段数: {len(stages)}")
        else:
            print(f"❌ 学习路径推荐失败: {response.text}")
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")

def test_ai_study_plan(token):
    """测试AI学习计划生成功能"""
    print("\n🧪 测试AI学习计划生成功能...")
    
    url = f"{API_BASE}/ai/study-plan"
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(url, headers=headers)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 学习计划生成成功!")
            plan_data = result.get('data', {})
            print(f"学习等级: {plan_data.get('study_level', 'N/A')}")
            daily_goal = plan_data.get('daily_goal', {})
            print(f"每日目标: {daily_goal.get('questions', 'N/A')}题")
        else:
            print(f"❌ 学习计划生成失败: {response.text}")
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")

def main():
    """主测试函数"""
    print("🚀 开始AI功能集成测试...")
    print("=" * 50)
    
    # 等待服务启动
    print("⏳ 等待服务启动...")
    time.sleep(2)
    
    # 创建教师用户
    if not create_teacher_user():
        print("❌ 教师用户创建失败，测试终止")
        return
    
    # 直接登录教师用户（跳过注册）
    token = login_user()
    if not token:
        print("❌ 用户登录失败，测试终止")
        return
    
    # 测试各项AI功能
    test_ai_generate_questions(token)
    test_ai_smart_grading(token)
    test_ai_learning_path(token)
    test_ai_study_plan(token)
    
    print("\n" + "=" * 50)
    print("🎉 AI功能集成测试完成!")

if __name__ == "__main__":
    main() 