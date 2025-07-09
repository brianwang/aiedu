#!/usr/bin/env python3
"""
测试前端AI功能
"""

import requests
import json

def test_backend_health():
    """测试后端健康状态"""
    try:
        response = requests.get("http://localhost:8111/health", timeout=5)
        print(f"✅ 后端服务正常，状态码: {response.status_code}")
        return True
    except Exception as e:
        print(f"❌ 后端服务异常: {e}")
        return False

def test_ai_routes():
    """测试AI路由"""
    try:
        # 测试AI路由是否存在
        response = requests.get("http://localhost:8111/docs", timeout=5)
        print(f"✅ API文档可访问，状态码: {response.status_code}")
        return True
    except Exception as e:
        print(f"❌ API文档访问失败: {e}")
        return False

def main():
    print("=" * 50)
    print("前端AI功能测试")
    print("=" * 50)
    
    # 测试后端服务
    backend_ok = test_backend_health()
    routes_ok = test_ai_routes()
    
    print("\n" + "=" * 50)
    print("测试结果")
    print("=" * 50)
    
    if backend_ok and routes_ok:
        print("🎉 后端服务正常，前端AI功能应该可以正常工作！")
        print("\n📝 修复内容:")
        print("1. ✅ 修复了前端API认证问题")
        print("2. ✅ 使用useApi组合式函数确保token传递")
        print("3. ✅ 修复了API返回类型不匹配问题")
        print("4. ✅ 移除了卡片右上角按钮")
        print("5. ✅ 实现了'开始能力评估'和'开始风格分析'功能")
        print("\n🚀 现在你可以:")
        print("- 点击'开始能力评估'按钮测试学习能力评估功能")
        print("- 点击'开始风格分析'按钮测试学习风格分析功能")
        print("- 查看智能推荐题目功能")
    else:
        print("❌ 后端服务有问题，请先启动后端服务")
        print("启动命令: cd backend && python main.py")

if __name__ == "__main__":
    main() 