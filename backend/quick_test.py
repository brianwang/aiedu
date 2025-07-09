import urllib.request
import urllib.parse
import json

def test_api():
    print("🧪 测试分析API...")
    
    url = "http://localhost:8111/api/v1/analytics/achievement-stats"
    headers = {"Authorization": "Bearer test_token"}
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            data = response.read()
            print(f"✅ 状态码: {response.status}")
            print(f"📊 响应数据: {data.decode('utf-8')}")
    except Exception as e:
        print(f"❌ 测试失败: {e}")

if __name__ == "__main__":
    test_api() 