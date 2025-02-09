 # services/palm_client.py
import google.generativeai as palm
from config import settings
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class PalmClient:
    def __init__(self):
        palm.configure(api_key=settings.PALM_API_KEY)
        self.model_name = settings.PALM_MODEL_NAME
        try:
            # 利用するモデルのインスタンスを作成
            self.model = palm.GenerativeModel(self.model_name)
            logger.info(f"Initialized PalmClient with model '{self.model_name}'")
        except Exception as e:
            logger.error(f"Failed to initialize PalmClient: {e}")
            raise

    def generate_reply(self, prompt: str) -> str:
        """
        入力プロンプトから応答テキストを生成する。
        将来的にエラーチェックやパラメータ調整などを追加しやすい構造です。
        """
        try:
            response = self.model.generate_content(prompt)
            reply_text = response.text  # 応答オブジェクトからテキストを抽出
            return reply_text
        except Exception as e:
            logger.error(f"Error during generate_reply: {e}")
            raise

# PalmClient のシングルトンインスタンスを作成しておくと、他モジュールから使いやすい
palm_client = PalmClient()
