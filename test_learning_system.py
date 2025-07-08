#!/usr/bin/env python3
"""
AI学习计划系统测试脚本
测试整个学习计划系统的功能
"""

import requests
import json
import time
from datetime import datetime, timedelta

# 配置
BASE_URL = "http://localhost:8000/api/v1"
TEST_USER = {
    "username": "test_student",
    "email": "test@example.com",
    "password": "test123456"
}

def print_step(step, description):
    """打印测试步骤"""
    print(f"\n{'='*50}")
    print(f"步骤 {step}: {description}")
    print(f"{'='*50}")

def test_api_health():
    """测试API健康状态"""
    print_step(1, "测试API健康状态")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ API服务正常运行")
            return True
        else:
            print(f"❌ API服务异常: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 无法连接到API服务: {e}")
        return False

def test_user_registration():
    """测试用户注册"""
    print_step(2, "测试用户注册")
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=TEST_USER)
        if response.status_code == 200:
            print("✅ 用户注册成功")
            return response.json()
        elif response.status_code == 400 and "already exists" in response.text:
            print("⚠️ 用户已存在，尝试登录")
            return test_user_login()
        else:
            print(f"❌ 用户注册失败: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ 注册请求失败: {e}")
        return None

def test_user_login():
    """测试用户登录"""
    print_step(3, "测试用户登录")
    try:
        login_data = {
            "username": TEST_USER["username"],
            "password": TEST_USER["password"]
        }
        response = requests.post(f"{BASE_URL}/auth/login", data=login_data)
        if response.status_code == 200:
            data = response.json()
            print("✅ 用户登录成功")
            return data["access_token"]
        else:
            print(f"❌ 用户登录失败: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ 登录请求失败: {e}")
        return None

def test_create_learning_profile(token):
    """测试创建学习画像"""
    print_step(4, "测试创建学习画像")
    headers = {"Authorization": f"Bearer {token}"}
    
    profile_data = {
        "age": 25,
        "daily_study_time": 60,
        "weekly_study_days": 5,
        "learning_style": "visual",
        "difficulty_preference": "progressive",
        "learning_environment": "online"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/learning/profile", json=profile_data, headers=headers)
        if response.status_code == 200:
            print("✅ 学习画像创建成功")
            return response.json()
        else:
            print(f"❌ 学习画像创建失败: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ 创建画像请求失败: {e}")
        return None

def test_create_learning_goals(token):
    """测试创建学习目标"""
    print_step(5, "测试创建学习目标")
    headers = {"Authorization": f"Bearer {token}"}
    
    goals_data = [
        {
            "subject": "Python编程",
            "skill_area": "Web开发",
            "target_level": "intermediate",
            "target_timeframe": 6,
            "priority": 5
        },
        {
            "subject": "数据结构与算法",
            "skill_area": "算法设计",
            "target_level": "advanced",
            "target_timeframe": 12,
            "priority": 4
        }
    ]
    
    created_goals = []
    for goal_data in goals_data:
        try:
            response = requests.post(f"{BASE_URL}/learning/goals", json=goal_data, headers=headers)
            if response.status_code == 200:
                print(f"✅ 学习目标创建成功: {goal_data['subject']}")
                created_goals.append(response.json())
            else:
                print(f"❌ 学习目标创建失败: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"❌ 创建目标请求失败: {e}")
    
    return created_goals

def test_generate_learning_plan(token):
    """测试生成学习计划"""
    print_step(6, "测试生成学习计划")
    headers = {"Authorization": f"Bearer {token}"}
    
    plan_data = {
        "user_id": 1  # 假设用户ID为1
    }
    
    try:
        response = requests.post(f"{BASE_URL}/learning/generate-plan", json=plan_data, headers=headers)
        if response.status_code == 200:
            print("✅ 学习计划生成成功")
            plan = response.json()
            print(f"   短期计划: {plan.get('short_term_plan', {}).get('title', 'N/A')}")
            print(f"   中期计划: {plan.get('medium_term_plan', {}).get('title', 'N/A')}")
            print(f"   长期计划: {plan.get('long_term_plan', {}).get('title', 'N/A')}")
            return plan
        else:
            print(f"❌ 学习计划生成失败: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ 生成计划请求失败: {e}")
        return None

def test_get_learning_plans(token):
    """测试获取学习计划"""
    print_step(7, "测试获取学习计划")
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/learning/plans", headers=headers)
        if response.status_code == 200:
            plans = response.json()
            print(f"✅ 获取学习计划成功，共 {len(plans)} 个计划")
            for plan in plans:
                print(f"   - {plan.get('title', 'N/A')} ({plan.get('plan_type', 'N/A')})")
            return plans
        else:
            print(f"❌ 获取学习计划失败: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ 获取计划请求失败: {e}")
        return None

def test_get_learning_statistics(token):
    """测试获取学习统计"""
    print_step(8, "测试获取学习统计")
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/learning/statistics", headers=headers)
        if response.status_code == 200:
            stats = response.json()
            print("✅ 获取学习统计成功")
            print(f"   总学习时间: {stats.get('total_study_time', 0)} 分钟")
            print(f"   完成率: {stats.get('completion_rate', 0) * 100:.1f}%")
            print(f"   连续学习: {stats.get('current_streak', 0)} 天")
            return stats
        else:
            print(f"❌ 获取学习统计失败: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ 获取统计请求失败: {e}")
        return None

def test_ai_study_functionality(token):
    """测试AI学习功能"""
    print_step(9, "测试AI学习功能")
    headers = {"Authorization": f"Bearer {token}"}
    
    ai_data = {
        "question": "什么是机器学习？",
        "context": "我正在学习人工智能相关课程"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/ai/chat", json=ai_data, headers=headers)
        if response.status_code == 200:
            result = response.json()
            print("✅ AI学习功能正常")
            print(f"   AI回复: {result.get('response', 'N/A')[:100]}...")
            return result
        else:
            print(f"❌ AI学习功能异常: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ AI请求失败: {e}")
        return None

def main():
    """主测试函数"""
    print("🚀 开始测试AI学习计划系统")
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 1. 测试API健康状态
    if not test_api_health():
        print("❌ API服务不可用，停止测试")
        return
    
    # 2. 测试用户注册/登录
    user_data = test_user_registration()
    if not user_data:
        print("❌ 用户认证失败，停止测试")
        return
    
    token = user_data.get("access_token") if isinstance(user_data, dict) else user_data
    
    # 3. 测试学习画像创建
    profile = test_create_learning_profile(token)
    
    # 4. 测试学习目标创建
    goals = test_create_learning_goals(token)
    
    # 5. 测试学习计划生成
    plan = test_generate_learning_plan(token)
    
    # 6. 测试获取学习计划
    plans = test_get_learning_plans(token)
    
    # 7. 测试获取学习统计
    stats = test_get_learning_statistics(token)
    
    # 8. 测试AI学习功能
    ai_result = test_ai_study_functionality(token)
    
    # 总结
    print(f"\n{'='*50}")
    print("🎉 测试完成总结")
    print(f"{'='*50}")
    print(f"✅ API服务: 正常")
    print(f"✅ 用户认证: {'成功' if token else '失败'}")
    print(f"✅ 学习画像: {'成功' if profile else '失败'}")
    print(f"✅ 学习目标: {'成功' if goals else '失败'}")
    print(f"✅ 学习计划: {'成功' if plan else '失败'}")
    print(f"✅ 学习统计: {'成功' if stats else '失败'}")
    print(f"✅ AI学习: {'成功' if ai_result else '失败'}")
    
    success_count = sum([
        1 if token else 0,
        1 if profile else 0,
        1 if goals else 0,
        1 if plan else 0,
        1 if stats else 0,
        1 if ai_result else 0
    ])
    
    total_tests = 6
    print(f"\n📊 测试结果: {success_count}/{total_tests} 项功能正常")
    
    if success_count == total_tests:
        print("🎊 所有功能测试通过！系统运行正常")
    else:
        print("⚠️ 部分功能需要检查，请查看上述错误信息")

if __name__ == "__main__":
    main() 