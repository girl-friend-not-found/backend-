# OpenAI APIを利用したチャットバックエンド

## 必要条件
- Python 3.8以上(3.12.5が望ましい)
- OpenAI APIキー

## セットアップ

1. 依存パッケージをインストール(必要に応じて仮想環境で)：
```bash
pip install fastapi uvicorn google-generativeai openai python-dotenv tf_keras deepface opencv-python numpy
```

2.  環境設定
config.example.pyをconfig.pyにリネームし、コメント化を解除する。
```plaintext
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL_NAME=gpt-3.5-turbo
```

## 使用方法

1. サーバーの起動：
```bash
uvicorn main:app --reload
```
### OpenAI チャットリクエスト例：
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"user_input": "こんにちは、元気ですか？"}' \
  http://127.0.0.1:8000/chat/openai
```

## APIエンドポイント
### `/chat/openai` - OpenAI GPT-3.5-turboを使用したチャット

#### レスポンス形式

成功時のレスポンス例：
```json
{
  "reply": "AIからの応答テキスト"
}
```

### `/detect_emotion` - Deepface感情分析


#### 入力形式
HTTPリクエストにはPOST形式を使用する。リクエストボディには以下のようなJSON形式で入力。imgキーの中にbase64のData URL形式で画像を渡す。
```json
{"img" : "画像のData URL"}
```
##### 例:
```json
{
  "img": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAAAAAAAD/2wBDAAoHBwkHBgoJCAkLCwoMDxkQDw4ODx4WFxIZJCAmJSMgI...(以下略)"
}
```
#### レスポンス形式

```json
{
  "angry": 怒りのパラメータ (0-100, float型),
  "disgust": 嫌悪のパラメータ (0-100, float型),
  "fear": 恐怖のパラメータ (0-100, float型),
  "happy": 幸福のパラメータ (0-100, float型),
  "sad": 悲しみのパラメータ (0-100, float型),
  "surprise": 驚きのパラメータ (0-100, float型),
  "neutral": 中立のパラメータ (0-100, float型)
}
```

##### 例: 

```json
{
  "angry": 0.8030961155891418,
  "disgust": 1.0965406005425393e-07,
  "fear": 0.0970025509595871,
  "happy": 1.7105669485317776e-06,
  "sad": 14.971575736999512,
  "surprise": 7.323064323827566e-07,
  "neutral": 84.12832641601562
}
```
