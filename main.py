# main.py
from fastapi import FastAPI, HTTPException, Request, UploadFile, File
from service.openai_client import OpenAIClient
import logging
from openai import OpenAI
from fastapi.middleware.cors import CORSMiddleware
from config import settings  # settingsをインポート

# ロガーの設定（必要に応じて設定ファイルなどで詳細設定することも可能）
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
openai_client = OpenAIClient()

# OpenAIクライアントの初期化（settings経由でAPIキーを使用）
client = OpenAI(
    api_key=settings.OPENAI_API_KEY
)

@app.get("/")
def read_root():
    return {"message": "Hello from OpenAI Backend!"}

@app.post("/chat/openai")
async def chat_with_openai(request: Request):
    """
    クライアント（例：Unity）からのJSON形式のリクエスト例：
      {
        "user_input": "こんにちは、調子はどう？"
      }
    """
    try:
        data = await request.json()
        user_input = data.get("user_input", "").strip()
        if not user_input:
            raise HTTPException(status_code=400, detail="user_input is required")
        
        # デバッグ用のログ追加
        logger.info(f"Received user input: {user_input}")
        
        try:
            # OpenAIClient を利用して応答生成
            reply_text = openai_client.generate_reply(user_input)
            logger.info(f"Generated reply: {reply_text}")
            return {"reply": reply_text}
        except Exception as e:
            # OpenAI関連のエラーの詳細をログに出力
            logger.error(f"OpenAI API Error: {str(e)}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"OpenAI API Error: {str(e)}")
    
    except HTTPException as http_exc:
        logger.error(f"HTTP Exception: {http_exc.detail}")
        raise http_exc
    except Exception as e:
        logger.error(f"Unexpected error in /chat/openai endpoint: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@app.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    """
    音声ファイルを文字起こしし、その結果を/chat/openaiに送信してレスポンスを生成する
    """
    try:
        # 音声ファイルを一時的に保存
        contents = await file.read()
        
        # OpenAI Whisper APIを使用して文字起こし
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=("audio.wav", contents, "audio/wav")
        )
        
        # 文字起こし結果をコンソールに表示
        print("=== 文字起こし結果 ===")
        print(transcription.text)
        print("=====================")
        logger.info(f"Transcription result: {transcription.text}")
        
        # 文字起こし結果を/chat/openaiエンドポイントに送信
        request = Request(scope={"type": "http"})
        request._json = {"user_input": transcription.text}
        chat_response = await chat_with_openai(request)
        
        # 両方の結果を返す
        return {
            "transcription": transcription.text,
            "reply": chat_response["reply"]
        }
        
    except Exception as e:
        logger.error(f"Error during processing: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")
