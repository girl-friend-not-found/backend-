# main.py

from fastapi import FastAPI, HTTPException, Request, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from service.openai_client import OpenAIClient
import logging
from openai import OpenAI
from fastapi.responses import JSONResponse
from config import settings
import base64
from io import BytesIO
from PIL import Image
import cv2
import numpy as np
from deepface import DeepFace
import os
from starlette.middleware.base import BaseHTTPMiddleware

# TensorFlowの警告を抑制
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPIのファイルアップロード制限を設定
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.datastructures import UploadFile as StarletteUploadFile
from starlette.requests import Request as StarletteRequest

# アップロードサイズを16MBに設定
StarletteUploadFile.spool_max_size = 16 * 1024 * 1024  # 16MB

app = FastAPI()

# ファイルサイズ制限を設定（例：10MB = 10 * 1024 * 1024）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# アプリケーションの設定
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

class CustomMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # クライアントの最大サイズを16MBに設定
        request.scope["max_client_size"] = 16 * 1024 * 1024  # 16MB
        response = await call_next(request)
        return response

app.add_middleware(CustomMiddleware)

openai_client = OpenAIClient()
client = OpenAI(api_key=settings.OPENAI_API_KEY)

@app.get("/")
def read_root():
    return {"message": "Hello from OpenAI Backend!"}

@app.post("/chat/openai")
async def chat_with_openai(request: Request):
    try:
        data = await request.json()
        user_input = data.get("user_input", "").strip()
        emotion = data.get("emotion")  # emotionデータを取得
        
        if not user_input:
            raise HTTPException(status_code=400, detail="user_input is required")

        logger.info(f"Received user input: {user_input}")
        if emotion:
            logger.info(f"Received emotion data: {emotion}")

        try:
            reply_text = openai_client.generate_reply(user_input, emotion)  # emotionを渡す
            logger.info(f"Generated reply: {reply_text}")

            return {
                "reply": reply_text,
                "should_speak": True
            }
        except Exception as e:
            logger.error(f"OpenAI API Error: {str(e)}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"OpenAI API Error: {str(e)}")
    
    except HTTPException as http_exc:
        logger.error(f"HTTP Exception: {http_exc.detail}")
        raise http_exc
    except Exception as e:
        logger.error(f"Unexpected error in /chat/openai endpoint: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


@app.post("/transcribe")
async def transcribe(
    file: UploadFile = File(..., max_size=16*1024*1024),
    img: Optional[str] = Form(None),
    request: Request = None
):
    try:
        contents = await file.read()
        logger.info(f"Received file size: {len(contents)} bytes")
        if img:
            logger.info(f"Received image data size: {len(img)} bytes")

        # 1) 音声ファイルを読み込み
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=("audio.wav", contents, "audio/wav")
        )
        logger.info(f"Transcription result: {transcription.text}")

        # 2) DeepFace で感情分析
        emotion = None
        if img:
            try:
                image_data = base64.b64decode(img)
                image = Image.open(BytesIO(image_data))
                image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

                face_analysis = DeepFace.analyze(
                    img_path=image_cv,
                    actions=['emotion'],
                    enforce_detection=False
                )
                emotion_dict = face_analysis[0]['emotion']
                emotion = {key: float(val) for key, val in emotion_dict.items()}

            except Exception as e:
                logger.error(f"DeepFace感情分析エラー: {str(e)}", exc_info=True)
                emotion = {"error": "DeepFace感情分析エラー"}

        # 3) ChatGPT との対話（emotionデータを含める）
        new_request = Request(scope={"type": "http"})
        new_request._json = {
            "user_input": transcription.text,
            "emotion": emotion
        }
        chat_response = await chat_with_openai(new_request)

        return {
            "transcription": transcription.text,
            "reply": chat_response["reply"],
            "should_speak": True,
            "emotion": emotion
        }

    except Exception as e:
        logger.error(f"Error during processing: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")
