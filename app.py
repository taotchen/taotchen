import base64
import ddddocr
from flask import Flask, request, jsonify
import json
import hashlib

app = Flask(__name__)

@app.route('/recognize_captcha', methods=['POST'])
def recognize_captcha():
    if request.method == 'POST':
        data = request.data.decode('utf-8') # 将请求数据转为字符串形式
        # 从请求体中解析 Base64 编码的图像数据
        base64Data = data.split(',')[1] # 提取 Base64 数据部分

        #  写入文件
        with open('image.jpg', 'wb') as f:
            f.write(base64.b64decode(base64Data))

        # 使用 ddddocr 识别图片验证码
        ocr = ddddocr.DdddOcr()
        with open('image.jpg', 'rb') as f:
            img_bytes = f.read()
        result = ocr.classification(img_bytes)
        return jsonify({'code': 200, 'msg': 'success', 'result': result})
    else:
        return jsonify({'code': 405, 'msg': 'Method Not Allowed'}), 405


@app.route('/encrypt', methods=['POST'])
def encrypt():
    password = request.json.get('pwd')
    print(password)
    md5 = hashlib.md5()
    md5.update(password.encode('utf-8'))
    encrypted_password = md5.hexdigest()
    return jsonify({'code': 200, 'msg': 'success', 'encrypted_password': encrypted_password})

@app.route('/')
def hello():
    return "Hello, World!"

# 启动服务器
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
