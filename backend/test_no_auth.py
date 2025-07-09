import urllib.request
import json

def test_api():
    print("🧪 测试分析API（无认证）...")
    
    # 测试根路径
    try:
        with urllib.request.urlopen("http://localhost:8111/", timeout=5) as response:
            data = response.read()
            print(f"✅ 根路径: {response.status}")
            print(f"📊 响应: {data.decode('utf-8')}")
    except Exception as e:
        print(f"❌ 根路径失败: {e}")
    
    # 测试健康检查
    try:
        with urllib.request.urlopen("http://localhost:8111/health", timeout=5) as response:
            data = response.read()
            print(f"✅ 健康检查: {response.status}")
            print(f"📊 响应: {data.decode('utf-8')}")
    except Exception as e:
        print(f"❌ 健康检查失败: {e}")

if __name__ == "__main__":
    test_api() 