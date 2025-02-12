# main.py
from fastapi import FastAPI, HTTPException, Request
from service.openai_client import OpenAIClient
import logging

# ロガーの設定（必要に応じて設定ファイルなどで詳細設定することも可能）
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
openai_client = OpenAIClient()

@app.get("/")
def read_root():
    return {"message": "Hello from Google PaLM and OpenAI Backend!"}

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
