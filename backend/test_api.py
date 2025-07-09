#!/usr/bin/env python3
"""测试API接口"""

import requests
import json

BASE_URL = "http://localhost:8111/api/v1"

def test_analytics_api():
    """测试分析API"""
    print("🧪 测试分析API接口...")
    
    # 测试成就统计
    try:
        response = requests.get(f"{BASE_URL}/analytics/achievement-stats", 
                              headers={"Authorization": "Bearer test_token"})
        print(f"✅ 成就统计: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   数据: {json.dumps(data, ensure_ascii=False, indent=2)}")
    except Exception as e:
        print(f"❌ 成就统计失败: {e}")
    
    # 测试学习趋势
    try:
        response = requests.get(f"{BASE_URL}/analytics/study-trends?days=7", 
                              headers={"Authorization": "Bearer test_token"})
        print(f"✅ 学习趋势: {response.status_code}")
    except Exception as e:
        print(f"❌ 学习趋势失败: {e}")
    
    # 测试学科表现
    try:
        response = requests.get(f"{BASE_URL}/analytics/subject-performance", 
                              headers={"Authorization": "Bearer test_token"})
        print(f"✅ 学科表现: {response.status_code}")
    except Exception as e:
        print(f"❌ 学科表现失败: {e}")
    
    # 测试难度分析
    try:
        response = requests.get(f"{BASE_URL}/analytics/difficulty-analysis", 
                              headers={"Authorization": "Bearer test_token"})
        print(f"✅ 难度分析: {response.status_code}")
    except Exception as e:
        print(f"❌ 难度分析失败: {e}")
    
    # 测试学习模式
    try:
        response = requests.get(f"{BASE_URL}/analytics/learning-patterns", 
                              headers={"Authorization": "Bearer test_token"})
        print(f"✅ 学习模式: {response.status_code}")
    except Exception as e:
        print(f"❌ 学习模式失败: {e}")

if __name__ == "__main__":
    test_analytics_api() 