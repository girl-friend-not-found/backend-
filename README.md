# Google Gemini & OpenAI APIを利用したチャットバックエンド

## 必要条件
- Python 3.8以上
- Google PaLM (Gemini) APIキー
- OpenAI APIキー

## セットアップ

1. 依存パッケージをインストール：
```bash
pip install fastapi uvicorn google-generativeai openai python-dotenv
```

## 環境設定

```plaintext
GOOGLE_PALM_API_KEY=your_palm_api_key_here
GOOGLE_PALM_MODEL_NAME=gemini-pro
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL_NAME=gpt-3.5-turbo
```

## 使用方法

1. サーバーの起動：
```bash
uvicorn main:app --reload
```

### Google PaLM (Gemini) チャットリクエスト例：
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"user_input": "こんにちは、元気ですか？"}' \
  http://127.0.0.1:8000/chat/gemini
```

### OpenAI チャットリクエスト例：
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"user_input": "こんにちは、元気ですか？"}' \
  http://127.0.0.1:8000/chat/openai
```

## APIエンドポイント

- `/chat/gemini` - Google Gemini APIを使用したチャット
- `/chat/openai` - OpenAI GPT-3.5-turboを使用したチャット

## レスポンス形式

成功時のレスポンス例：
```json
{
  "reply": "AIからの応答テキスト"
}
```

