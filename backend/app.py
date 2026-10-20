from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import base64
import os
import re
from rapidocr_onnxruntime import RapidOCR
from db import init_db, add_bill, get_bills

app = Flask(__name__)
CORS(app)
init_db()

# 全局OCR实例，程序启动加载一次
ocr = RapidOCR()

UPLOAD_FOLDER = os.path.join("static", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/static/uploads/<filename>')
def serve_img(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# OCR识别接口：接收base64图片，提取金额
@app.route("/api/ocr_price", methods=["POST"])
def api_ocr_price():
    req_data = request.get_json()
    img_base64 = req_data.get("img", "")
    if not img_base64:
        return jsonify({"code": 400, "msg": "图片不能为空"})

    _, img_str = img_base64.split(",")
    img_bytes = base64.b64decode(img_str)
    tmp_img_path = "tmp_ocr.jpg"
    with open(tmp_img_path, "wb") as f:
        f.write(img_bytes)

    result, elapse = ocr(tmp_img_path)
    all_text = []
    if result:
        for line in result:
            # rapidocr 格式: [box, text, score]
            txt = line[1]
            all_text.append(txt)
    os.remove(tmp_img_path)

    pattern = re.compile(r'¥?(\d+\.\d{1,2}|\d+)')
    candidates = []
    for text in all_text:
        matches = pattern.findall(text)
        for m in matches:
            try:
                num = float(m)
                if 0 < num < 999999:
                    candidates.append(num)
            except:
                continue
    if candidates:
        price = max(candidates)
        return jsonify({"code": 200, "price": price, "text_list": all_text})
    else:
        return jsonify({"code": 201, "msg": "未识别到金额", "price": ""})

# 新增账单接口
@app.route("/api/add_bill", methods=["POST"])
def api_add_bill():
    req_data = request.get_json()
    name = req_data.get("name", "")
    price = req_data.get("price", 0)
    remark = req_data.get("remark", "")
    img_base64 = req_data.get("img", "")

    if not name or not img_base64:
        return jsonify({"code": 400, "msg": "物品名称和照片不能为空"})
    try:
        price = float(price)
    except:
        return jsonify({"code": 400, "msg": "价格必须是数字"})

    _, img_str = img_base64.split(",")
    img_bytes = base64.b64decode(img_str)
    filename = f"bill_{int(os.times()[4])}.jpg"
    save_path = os.path.join(UPLOAD_FOLDER, filename)
    with open(save_path, "wb") as f:
        f.write(img_bytes)

    img_url = f"/static/uploads/{filename}"
    add_bill(name, price, remark, img_url)
    return jsonify({"code": 200, "msg": "记账成功", "img_url": img_url})

# 获取账单列表
@app.route("/api/bills", methods=["GET"])
def api_get_bills():
    data = get_bills()
    return jsonify({"code": 200, "data": data})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
