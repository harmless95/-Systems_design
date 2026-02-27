import logging

from core.model import TelegramData
from pydantic import ValidationError

logger = logging.getLogger("ValidationData")


async def check_valid(data: dict):
    try:
        result_data = TelegramData.model_validate(data)
        return result_data
    except ValidationError:
        logger.warning("Invalid data")
    except Exception as ex:
        logger.error("Error validation: %s", ex)
