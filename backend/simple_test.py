import requests
import time

def test_api():
    print("等待服务启动...")
    time.sleep(3)
    
    try:
        response = requests.get(
            "http://localhost:8111/api/v1/analytics/achievement-stats",
            headers={"Authorization": "Bearer test_token"},
            timeout=5
        )
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.text}")
    except Exception as e:
        print(f"错误: {e}")

if __name__ == "__main__":
    test_api() 