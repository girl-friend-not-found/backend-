# Google PaLM APIを利用したチャットバックエンド

## 必要条件
- Python 3.8以上
- Google PaLM APIキー

1. 依存パッケージをインストール：
```bash
pip install fastapi uvicorn google-generativeai python-dotenv
```

## 環境設定

```plaintext
GOOGLE_PALM_API_KEY=your_api_key_here
GOOGLE_PALM_MODEL_NAME=gemini-pro
```

## 使用方法

1. サーバーの起動：
```bash
uvicorn main:app --reload
```

### チャットリクエスト例：
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"user_input": "こんにちは、元気ですか？"}' \
  http://127.0.0.1:8000/chat

```
