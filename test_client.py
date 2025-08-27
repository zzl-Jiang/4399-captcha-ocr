import requests

# API 服务器地址
OCR_API_URL = 'http://localhost:5001/recognize'
# 测试图片路径
IMAGE_PATH = 'debug/test_captcha.jpg'

def test_ocr_api():
    print(f"正在向 {OCR_API_URL} 发送图片 {IMAGE_PATH}...")
    
    try:
        # 以二进制模式读取文件
        with open(IMAGE_PATH, 'rb') as f:
            # 构造 multipart/form-data 请求
            files = {'image': (IMAGE_PATH, f, 'image/png')}
            response = requests.post(OCR_API_URL, files=files)

        # 检查响应状态码
        response.raise_for_status() # 如果是 4xx 或 5xx 错误，会抛出异常

        # 解析 JSON 响应
        data = response.json()
        
        print("\n--- API 响应 ---")
        print(data)
        
        if data.get('success'):
            print(f"\n✅ 识别成功! 结果: '{data.get('result')}'")
        else:
            print(f"\n❌ API 返回失败: {data.get('error')}")

    except requests.exceptions.RequestException as e:
        print(f"\n❌ 请求失败: {e}")
    except Exception as e:
        print(f"\n❌ 发生未知错误: {e}")


if __name__ == '__main__':
    test_ocr_api()