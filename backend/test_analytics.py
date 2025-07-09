#!/usr/bin/env python3
"""测试analytics模块导入"""

try:
    print("正在测试analytics模块导入...")
    from app.api import analytics
    print("✅ analytics模块导入成功")
    print(f"路由前缀: {analytics.router.prefix}")
    print(f"路由标签: {analytics.router.tags}")
    
    # 列出所有路由
    print("\n📋 可用的路由:")
    for route in analytics.router.routes:
        if hasattr(route, 'path'):
            print(f"  {route.methods} {route.path}")
    
except ImportError as e:
    print(f"❌ analytics模块导入失败: {e}")
except Exception as e:
    print(f"❌ 其他错误: {e}")

if __name__ == "__main__":
    print("测试完成") 