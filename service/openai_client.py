from openai import OpenAI
from config import settings
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class OpenAIClient:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model_name = settings.OPENAI_MODEL_NAME
        logger.info(f"Initialized OpenAIClient with model '{self.model_name}'")

    def generate_reply(self, prompt: str) -> str:
        """
        OpenAI APIを使用して応答を生成する
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            reply_text = response.choices[0].message.content
            return reply_text
        except Exception as e:
            logger.error(f"Error during OpenAI generate_reply: {e}")
            raise

openai_client = OpenAIClient() 