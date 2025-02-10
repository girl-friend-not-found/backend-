# main.py
from fastapi import FastAPI, HTTPException, Request
from service.palm_client import palm_client
from service.openai_client import openai_client
import logging

# ロガーの設定（必要に応じて設定ファイルなどで詳細設定することも可能）
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello from Google PaLM and OpenAI Backend!"}

@app.post("/chat/gemini")
async def chat_with_palm(request: Request):
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
        
        # PalmClient を利用して応答生成
        reply_text = palm_client.generate_reply(user_input)
        return {"reply": reply_text}
    
    except HTTPException as http_exc:
        logger.error(f"HTTP Exception: {http_exc.detail}")
        raise http_exc
    except Exception as e:
        logger.error(f"Unexpected error in /chat endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

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
        
        # OpenAIClient を利用して応答生成
        reply_text = openai_client.generate_reply(user_input)
        return {"reply": reply_text}
    
    except HTTPException as http_exc:
        logger.error(f"HTTP Exception: {http_exc.detail}")
        raise http_exc
    except Exception as e:
        logger.error(f"Unexpected error in /chat/openai endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
