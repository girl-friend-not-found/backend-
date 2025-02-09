# config.py
import os

class Settings:
    # 環境変数から取得、なければデフォルト値（※実際にはデフォルト値のハードコーディングは推奨されません）
    PALM_API_KEY: str = os.environ.get("GOOGLE_PALM_API_KEY", "YOUR_DEFAULT_API_KEY")
    PALM_MODEL_NAME: str = os.environ.get("GOOGLE_PALM_MODEL_NAME", "gemini-pro")

settings = Settings()
