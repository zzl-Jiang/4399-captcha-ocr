import os
from pathlib import Path
from flask import Flask, request, jsonify
from ddddocr import DdddOcr

# 初始化 Flask 应用
app = Flask(__name__)

# 配置和模型加载
# 将模型加载放在全局，确保只执行一次
try:
    print("正在加载 OCR 模型...")
    CURRENT_DIR = Path(__file__).parent
    OCR_PATH = CURRENT_DIR / "data" / "ocr_data"
    
    # 检查模型文件是否存在
    model_path = OCR_PATH / "4399ocr.onnx"
    charsets_path = OCR_PATH / "4399ocr.json"
    if not model_path.exists() or not charsets_path.exists():
        raise FileNotFoundError("OCR 模型或字符集文件未找到！请检查 'data/ocr_data' 目录。")

    ocr = DdddOcr(
        show_ad=False,
        # ddddocr 默认使用 CPU
        import_onnx_path=str(model_path),
        charsets_path=str(charsets_path),
    )
    print("OCR 模型加载成功！")

except Exception as e:
    print(f"OCR 模型加载失败: {e}")
    # 如果模型加载失败，服务无法工作，可以选择退出
    ocr = None


# 定义 API 路由
@app.route('/recognize', methods=['POST'])
def recognize_captcha():
    # 确保模型已成功加载
    if ocr is None:
        return jsonify({'success': False, 'error': 'OCR 服务不可用，模型导入失败'}), 503

    # 从 POST 请求中获取图片文件
    if 'image' not in request.files:
        return jsonify({'success': False, 'error': 'request 中没有图片文件'}), 400
    
    image_file = request.files['image']
    
    # 读取图片文件的二进制内容
    image_bytes = image_file.read()
    
    try:
        # 调用 ddddocr 进行识别
        result = ocr.classification(image_bytes)
        
        # 简单的结果验证
        if result and len(result) > 0:
            print(f"识别成功: {result}")
            # 返回成功的 JSON 响应
            return jsonify({'success': True, 'result': result.lower()}) # type: ignore
        else:
            print("识别结果为空")
            return jsonify({'success': False, 'error': 'Recognition result is empty'})

    except Exception as e:
        print(f"识别过程中发生错误: {e}")
        # 返回服务器内部错误的 JSON 响应
        return jsonify({'success': False, 'error': f'An error occurred during recognition: {e}'}), 500

# 添加检查端点
@app.route('/health', methods=['GET'])
def health_check():
    if ocr:
        return jsonify({'status': 'ok'})
    else:
        return jsonify({'status': 'error', 'message': 'OCR model not loaded'}), 503

# --- 启动服务器 ---
if __name__ == '__main__':
    # 使用 Waitress 来运行应用
    from waitress import serve
    print("在 http://0.0.0.0:10000 上启动 OCR 服务...")
    serve(app, host='0.0.0.0', port=10000)