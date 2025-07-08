#!/usr/bin/env python3
"""
API连接测试脚本
用于验证前后端API连接是否正常
"""

import requests
import json
import sys
from datetime import datetime

# 配置
BASE_URL = "http://localhost:8111"
API_BASE = f"{BASE_URL}/api/v1"

def test_health_check():
    """测试健康检查接口"""
    print("🔍 测试健康检查...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ 健康检查通过")
            return True
        else:
            print(f"❌ 健康检查失败: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ 健康检查失败: {e}")
        return False

def test_root_endpoint():
    """测试根路径接口"""
    print("🔍 测试根路径...")
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 根路径正常: {data.get('message', 'Unknown')}")
            return True
        else:
            print(f"❌ 根路径失败: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ 根路径失败: {e}")
        return False

def test_api_docs():
    """测试API文档接口"""
    print("🔍 测试API文档...")
    try:
        response = requests.get(f"{BASE_URL}/docs", timeout=5)
        if response.status_code == 200:
            print("✅ API文档可访问")
            return True
        else:
            print(f"❌ API文档失败: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ API文档失败: {e}")
        return False

def test_auth_endpoints():
    """测试认证相关接口"""
    print("🔍 测试认证接口...")
    
    # 测试注册接口（不实际注册）
    try:
        response = requests.post(f"{API_BASE}/register", 
                               json={
                                   "username": "testuser",
                                   "email": "test@example.com",
                                   "password": "testpassword",
                                   "confirm_password": "testpassword"
                               }, timeout=5)
        if response.status_code in [201, 400]:  # 201成功或400参数错误都算正常
            print("✅ 注册接口正常")
        else:
            print(f"❌ 注册接口异常: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ 注册接口失败: {e}")
        return False
    
    # 测试登录接口（使用不存在的用户）
    try:
        response = requests.post(f"{API_BASE}/login", 
                               json={
                                   "username": "nonexistent",
                                   "password": "wrongpassword"
                               }, timeout=5)
        if response.status_code == 401:  # 401未授权是预期的
            print("✅ 登录接口正常")
            return True
        else:
            print(f"❌ 登录接口异常: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ 登录接口失败: {e}")
        return False

def test_question_endpoints():
    """测试题目相关接口"""
    print("🔍 测试题目接口...")
    try:
        response = requests.get(f"{API_BASE}/questions", timeout=5)
        if response.status_code in [200, 401]:  # 200成功或401需要认证都算正常
            print("✅ 题目接口正常")
            return True
        else:
            print(f"❌ 题目接口异常: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ 题目接口失败: {e}")
        return False

def test_ai_endpoints():
    """测试AI相关接口"""
    print("🔍 测试AI接口...")
    try:
        response = requests.get(f"{API_BASE}/ai/recommendations", timeout=5)
        if response.status_code in [200, 401]:  # 200成功或401需要认证都算正常
            print("✅ AI推荐接口正常")
            return True
        else:
            print(f"❌ AI推荐接口异常: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ AI推荐接口失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 AI智能教育平台 - API连接测试")
    print("=" * 50)
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"后端地址: {BASE_URL}")
    print(f"API前缀: {API_BASE}")
    print()
    
    tests = [
        ("健康检查", test_health_check),
        ("根路径", test_root_endpoint),
        ("API文档", test_api_docs),
        ("认证接口", test_auth_endpoints),
        ("题目接口", test_question_endpoints),
        ("AI接口", test_ai_endpoints),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        print("-" * 30)
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ {test_name}测试异常: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！API连接正常")
        return 0
    else:
        print("⚠️  部分测试失败，请检查后端服务状态")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 