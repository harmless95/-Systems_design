import logging
from openai import AsyncOpenAI

from app.core.config import setting

logger = logging.getLogger(__name__)


async def conn_client():
    client = None
    try:
        client = AsyncOpenAI(
            api_key=setting.ai_bot.token_AI,
            base_url="https://api.groq.com/openai/v1",
        )
        logger.info("✅ Groq клиент инициализирован")
    except Exception as e:
        logger.error(f"❌ Ошибка инициализации Groq: {e}")
    return client
