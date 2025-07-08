#!/usr/bin/env python3
"""
测试学习相关API接口
"""
import requests
import json

BASE_URL = "http://localhost:8111"

def test_learning_apis():
    """测试学习相关API接口"""
    print("🧪 开始测试学习相关API接口...")
    
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
    
    # 3. 测试获取学习计划列表
    print("\n3. 测试获取学习计划列表...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/learning/plans", headers=headers)
        print(f"   状态码: {response.status_code}")
        if response.status_code == 200:
            plans = response.json()
            print(f"   ✅ 获取学习计划成功，共 {len(plans)} 个计划")
        else:
            print(f"   ❌ 获取学习计划失败: {response.json()}")
    except Exception as e:
        print(f"   ❌ 请求失败: {e}")
    
    # 4. 测试获取成就列表
    print("\n4. 测试获取成就列表...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/learning/achievements", headers=headers)
        print(f"   状态码: {response.status_code}")
        if response.status_code == 200:
            achievements = response.json()
            print(f"   ✅ 获取成就成功，共 {len(achievements)} 个成就")
        else:
            print(f"   ❌ 获取成就失败: {response.json()}")
    except Exception as e:
        print(f"   ❌ 请求失败: {e}")
    
    # 5. 测试获取学习统计
    print("\n5. 测试获取学习统计...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/learning/statistics", headers=headers)
        print(f"   状态码: {response.status_code}")
        if response.status_code == 200:
            stats = response.json()
            print(f"   ✅ 获取学习统计成功")
            print(f"   总学习时间: {stats.get('total_study_time', 0)} 分钟")
            print(f"   完成率: {stats.get('completion_rate', 0):.2%}")
        else:
            print(f"   ❌ 获取学习统计失败: {response.json()}")
    except Exception as e:
        print(f"   ❌ 请求失败: {e}")
    
    # 6. 测试获取用户画像
    print("\n6. 测试获取用户画像...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/learning/profile", headers=headers)
        print(f"   状态码: {response.status_code}")
        if response.status_code == 200:
            profile = response.json()
            print(f"   ✅ 获取用户画像成功")
        elif response.status_code == 404:
            print(f"   ℹ️ 用户画像不存在（正常）")
        else:
            print(f"   ❌ 获取用户画像失败: {response.json()}")
    except Exception as e:
        print(f"   ❌ 请求失败: {e}")
    
    # 7. 测试创建用户画像
    print("\n7. 测试创建用户画像...")
    profile_data = {
        "age": 25,
        "learning_style": "visual",
        "difficulty_preference": "progressive",
        "daily_study_time": 120,
        "weekly_study_days": 5,
        "learning_environment": "online"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/v1/learning/profile", 
                               json=profile_data, headers=headers)
        print(f"   状态码: {response.status_code}")
        if response.status_code == 200:
            profile = response.json()
            print(f"   ✅ 创建用户画像成功")
        elif response.status_code == 400:
            print(f"   ℹ️ 用户画像已存在（正常）")
        else:
            print(f"   ❌ 创建用户画像失败: {response.json()}")
    except Exception as e:
        print(f"   ❌ 请求失败: {e}")
    
    # 8. 测试获取学习目标
    print("\n8. 测试获取学习目标...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/learning/goals", headers=headers)
        print(f"   状态码: {response.status_code}")
        if response.status_code == 200:
            goals = response.json()
            print(f"   ✅ 获取学习目标成功，共 {len(goals)} 个目标")
        else:
            print(f"   ❌ 获取学习目标失败: {response.json()}")
    except Exception as e:
        print(f"   ❌ 请求失败: {e}")
    
    print("\n🎉 测试完成！")

if __name__ == "__main__":
    test_learning_apis() 