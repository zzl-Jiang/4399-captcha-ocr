# BQYX Captcha OCR Service

这是一个基于 Python、Flask 和 ddddocr 的轻量级微服务，专门用于识别《爆枪英雄》游戏 (包括其他4399游戏) 登录时可能出现的4399验证码。

该服务被设计为 Node.js 主应用的辅助服务，通过一个简单的 HTTP API 端点接收验证码图片，并返回识别出的文本结果。

![ddddocr](https://img.shields.io/badge/OCR%20Engine-ddddocr-blue)
![Flask](https://img.shields.io/badge/Framework-Flask-green)
![Python](https://img.shields.io/badge/Python-3.8+-blueviolet)

---

## 🚀 功能特性

- **高效识别**: 使用 `ddddocr` 库，加载了针对 4399 验证码的特定 ONNX 模型，识别准确率高。
- **高性能**: Flask 服务启动时预加载 OCR 模型，后续识别请求响应速度快，避免了重复加载模型的开销。
- **标准 API 接口**: 提供一个简单的 `/recognize` 端点，通过 `POST` 请求接收图片文件，返回 JSON 格式的结果，易于任何编程语言（如本项目中的 Node.js）进行调用。
- **健壮性**: 包含健康检查 (`/health`) 端点，并对输入和识别过程中的潜在异常进行了处理。
- **易于部署**: 结构简单，依赖清晰，可以轻松地通过 Docker 或在任何支持 Python 的云平台上进行部署。

---

## 🛠️ 安装与环境设置

为了确保项目依赖的隔离性，强烈建议在 Python 虚拟环境中运行此服务。

### 1. 克隆仓库

```bash
git clone zzl-Jiang/4399-captcha-ocr
```

### 2. 安装依赖

本项目的所有 Python 依赖都记录在 `requirements.txt` 文件中。

```bash
# 确保虚拟环境已激活
(venv) pip install -r requirements.txt
```

**`requirements.txt` 文件内容:**
```
flask
ddddocr
waitress
# 或者 gunicorn (用于 Linux 生产环境)
```

### 4. 准备模型文件

请确保以下文件已放置在 `data/ocr_data/` 目录下：

- `4399ocr.onnx` (ONNX 模型文件)
- `4399ocr.json` (模型对应的字符集文件)

项目结构应如下所示：
```
.
├── data/
│   └── ocr_data/
│       ├── 4399ocr.json
│       └── 4399ocr.onnx
├── ocr_server.py
└── requirements.txt
```

---

## 🏃‍♂️ 如何运行

### 开发环境

在开发和测试时，您可以直接运行 `ocr_server.py`。

```bash
# 确保虚拟环境已激活
(venv) python ocr_server.py
```

服务启动后，您将在终端看到类似如下的输出：
```
正在加载 OCR 模型...
OCR 模型加载成功！
在 http://0.0.0.0:5001 上启动 OCR 服务...
```
这表示服务正在监听 `5001` 端口，随时准备接收识别请求。

### 生产环境 (推荐)

在生产环境中，建议使用 `waitress` (跨平台) 或 `gunicorn` (Linux) 来运行 Flask 应用，它们比 Flask 自带的开发服务器更稳定、性能更好。

**使用 Waitress:**
```bash
(venv) waitress-serve --host=0.0.0.0 --port=5001 ocr_server:app
```

**使用 Gunicorn (Linux/macOS):**
```bash
(venv) gunicorn --workers 4 --bind 0.0.0.0:5001 ocr_server:app
```

---

## 📡 API 使用说明

### 端点: `/recognize`

- **方法**: `POST`
- **请求类型**: `multipart/form-data`
- **参数**:
  - `image`: (文件) 必须。包含验证码图片二进制内容的文件。

**示例调用 (使用 curl):**
```bash
curl -X POST -F "image=@/path/to/your/captcha.png" http://localhost:5001/recognize
```

**成功响应 (Status `200 OK`):**
```json
{
  "success": true,
  "result": "qny2" 
}
```

**失败响应 (Status `400` or `500`):**
```json
{
  "success": false,
  "error": "No image file found in the request" 
}
```

### 端点: `/health`

- **方法**: `GET`
- **用途**: 用于健康检查，可以被部署平台（如 Render, Docker）或监控系统调用，以确认服务是否正常运行。

**成功响应 (Status `200 OK`):**
```json
{
  "status": "ok"
}
```

**失败响应 (Status `503 Service Unavailable`):**
```json
{
  "status": "error",
  "message": "OCR model not loaded"
}
```

---

## 🤝 与主应用 (Node.js) 的集成

在 Node.js 应用中，可以使用 `axios` 和 `form-data` 库来调用此 OCR 服务。请参考主应用 `src/services/captchaService.js` 文件 (由于安全性考虑，仓库暂时未公开) 中的具体实现。