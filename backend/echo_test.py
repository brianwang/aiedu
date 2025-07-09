print("Hello World!")
print("测试开始...")

try:
    import urllib.request
    print("urllib导入成功")
    
    response = urllib.request.urlopen("http://localhost:8111/", timeout=5)
    print(f"连接成功，状态码: {response.status}")
    
except Exception as e:
    print(f"错误: {e}")

print("测试结束") 