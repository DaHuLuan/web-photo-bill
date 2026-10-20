# web-photo-bill
网页拍照记账工具，浏览器调用摄像头拍照，**支持RapidOCR本地离线识别票据金额**，录入物品价格、备注，本地保存账单与照片。
前端 Vue3，后端 Flask + SQLite，电脑/手机浏览器均可使用。

## ✨ 功能
- H5浏览器调用摄像头拍摄消费照片
- ✨ OCR离线识别票据图片，自动提取金额填入价格框
- 录入物品名称、价格、备注（识别结果支持手动修改）
- 后端SQLite持久化存储账单
- 账单列表展示+图片预览

## 📦 后端环境
```bash
cd backend
pip install -r requirements.txt
```
> 首次运行会自动下载RapidOCR识别模型（仅一次）

## 🚀 启动方式
1. 启动Flask后端
```bash
cd backend
python app.py
```
后端地址：`http://127.0.0.1:5000`

2. 启动前端网页
```bash
cd frontend
python -m http.server 8080
```
浏览器打开 `http://127.0.0.1:8080`

### 使用流程
1. 打开摄像头，拍摄小票/物品照片
2. 点击【OCR识别金额】，自动提取价格填入输入框
3. 补充物品名称、备注，可手动修改识别出来的价格
4. 保存账单，下方表格自动刷新

> ⚠️ 摄像头权限说明：
> - `localhost` 本地调试浏览器允许摄像头；
> - 如果公网部署，**必须HTTPS**才能调用浏览器摄像头（http公网会被浏览器拦截）。

## 📁 存储说明
- `backend/bill.db`：SQLite数据库，账单记录
- `backend/static/uploads/`：存放拍摄的所有照片

## 后续扩展
- 账单按时间筛选、消费统计
- 导出CSV账单
- 标签分类（餐饮、交通、购物）
- OCR识别商品名称

## 📜 License
MIT
