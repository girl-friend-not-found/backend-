# config.py
import os

class Settings:
    # 環境変数から取得、なければデフォルト値
    OPENAI_API_KEY: str = os.environ.get("OPENAI_API_KEY", "openai_api_key")
    OPENAI_MODEL_NAME: str = os.environ.get("OPENAI_MODEL_NAME", "gpt-3.5-turbo")

settings = Settings()
