# config.py
import os

class Settings:
    # 環境変数から取得、なければデフォルト値
    PALM_API_KEY: str = os.environ.get("GOOGLE_PALM_API_KEY", "YOUR_DEFAULT_API_KEY")
    PALM_MODEL_NAME: str = os.environ.get("GOOGLE_PALM_MODEL_NAME", "gemini-pro")
    OPENAI_API_KEY: str = os.environ.get("OPENAI_API_KEY", "openai_api_key")
    OPENAI_MODEL_NAME: str = os.environ.get("OPENAI_MODEL_NAME", "gpt-3.5-turbo")

settings = Settings()
