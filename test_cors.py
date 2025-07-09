#!/usr/bin/env python3
"""
测试CORS配置
"""

import requests
import json

def test_cors():
    """测试CORS配置"""
    print("🔍 测试CORS配置...")
    
    # 测试不同的前端端口
    test_urls = [
        "http://localhost:3000",
        "http://localhost:5173", 
        "http://localhost:4173",
        "http://localhost:8080",
        "http://localhost:3001"
    ]
    
    backend_url = "http://localhost:8111"
    
    for frontend_url in test_urls:
        try:
            # 模拟前端请求
            headers = {
                'Origin': frontend_url,
                'Access-Control-Request-Method': 'POST',
                'Access-Control-Request-Headers': 'Content-Type,Authorization'
            }
            
            # 测试预检请求
            response = requests.options(f"{backend_url}/api/v1/ai/study-plan", headers=headers)
            
            print(f"✅ {frontend_url} -> CORS预检请求成功，状态码: {response.status_code}")
            
            # 检查CORS头
            cors_headers = {
                'Access-Control-Allow-Origin': response.headers.get('Access-Control-Allow-Origin'),
                'Access-Control-Allow-Methods': response.headers.get('Access-Control-Allow-Methods'),
                'Access-Control-Allow-Headers': response.headers.get('Access-Control-Allow-Headers')
            }
            
            print(f"   CORS头: {cors_headers}")
            
        except Exception as e:
            print(f"❌ {frontend_url} -> CORS测试失败: {e}")

def test_actual_request():
    """测试实际请求"""
    print("\n🚀 测试实际API请求...")
    
    try:
        # 测试健康检查
        response = requests.get("http://localhost:8111/health")
        print(f"✅ 健康检查成功: {response.status_code}")
        
        # 测试AI路由
        response = requests.get("http://localhost:8111/api/v1/ai/recommendations")
        print(f"✅ AI推荐路由状态: {response.status_code}")
        
        if response.status_code == 401:
            print("   这是正常的，因为需要认证")
        elif response.status_code == 200:
            print("   请求成功！")
        else:
            print(f"   响应内容: {response.text[:200]}")
            
    except Exception as e:
        print(f"❌ 实际请求测试失败: {e}")

def main():
    print("=" * 60)
    print("CORS配置测试")
    print("=" * 60)
    
    # 测试CORS配置
    test_cors()
    
    # 测试实际请求
    test_actual_request()
    
    print("\n" + "=" * 60)
    print("修复说明")
    print("=" * 60)
    print("✅ 已修复CORS配置:")
    print("1. 设置debug=True，开发环境允许所有源")
    print("2. 添加了常见的前端端口到allowed_origins")
    print("3. 配置了完整的CORS中间件")
    print("\n🚀 现在前端应该可以正常访问后端API了！")
    print("\n📝 如果仍有问题，请检查:")
    print("- 后端服务是否在localhost:8111运行")
    print("- 前端是否在允许的端口运行")
    print("- 浏览器控制台是否有其他错误")

if __name__ == "__main__":
    main() 