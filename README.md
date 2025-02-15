# OpenAI APIを利用したチャットバックエンド

## 必要条件
- Python 3.8以上(3.12.5が望ましい)
- OpenAI APIキー

## セットアップ

1. 依存パッケージをインストール(必要に応じて仮想環境で)：
```bash
pip install fastapi uvicorn google-generativeai openai python-dotenv tf_keras deepface opencv-python numpy python-multipart requests
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
### `/transcribe` - 画像認識と音声文字起こし、チャット応答

このエンドポイントは音声ファイルを文字起こしし、その結果を使用してチャット応答を生成する機能を提供します。また、DeepFaceライブラリを用いて画像から感情分析を行います。

#### 説明

このエンドポイントは、音声ファイルをアップロードし、OpenAIのWhisperモデルを使用してその音声内容をテキストに変換することができます。文字起こしが完了した後、得られたテキストはチャットエンドポイント（`/chat/openai`）に送信され、OpenAIのGPTモデルを使用して対話応答を生成します。

さらに、このプロセスではDeepFaceライブラリが用いられ、画像から感情分析を行うこともできます。これにより、提供されるチャットのコンテキストや追加機能を強化するための感情データが得られます。

#### 使用方法

1. **リクエスト形式**
   - HTTP POSTメソッドを使用します。
   - リクエストボディには、音声ファイルと画像のData URL（base64エンコード）を含めます。

2. **入力パラメータ**
   - `file`: 音声ファイル。`audio/wav`形式が推奨されます。
   - `img`: 画像のData URLで、感情分析に使用します。

3. **レスポンス形式**

成功した場合、以下のようなJSONオブジェクトが返されます：

```json
{
  "transcription": "文字起こし結果",
  "reply": "AIからの応答テキスト",
  "emotion": {
    "angry": 怒りのパラメータ (0-100, float型),
    "disgust": 嫌悪のパラメータ (0-100, float型),
    "fear": 恐怖のパラメータ (0-100, float型),
    "happy": 幸福のパラメータ (0-100, float型),
    "sad": 悲しみのパラメータ (0-100, float型),
    "surprise": 驚きのパラメータ (0-100, float型),
    "neutral": 中立のパラメータ (0-100, float型)
  }
}
```

##### レスポンス例:

```json
{
  "transcription": "こんにちは、元気ですか？",
  "reply": "はい、とても元気です。あなたはどうですか？",
  "emotion": {
    "angry": 0.8030961155891418,
    "disgust": 1.0965406005425393e-07,
    "fear": 0.0970025509595871,
    "happy": 1.7105669485317776e-06,
    "sad": 14.971575736999512,
    "surprise": 7.323064323827566e-07,
    "neutral": 84.12832641601562
  }
}
```
