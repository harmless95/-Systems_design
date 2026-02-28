from pydantic import ValidationError

from core.config import logger
from core.model import TelegramData


async def check_valid(data: dict):
    try:
        result_data = TelegramData.model_validate(data)
        return result_data
    except ValidationError:
        logger.warning("Invalid data")
    except Exception as ex:
        logger.error("Error validation: %s", ex)
