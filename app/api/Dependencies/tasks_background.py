import json
import redis.asyncio as redis
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from api.Dependencies import handler, check_valid, conn_client
from api.crud.telegram_crud import save_db
from core.config import logger, setting
from core.model import TelegramData

REDIS_HOST = setting.redis.host
redis_channel = "tasks_llm"
redis_client = redis.Redis(
    host=REDIS_HOST,
    port=6379,
    decode_responses=True,
)


async def create_tasks(body: dict, session: AsyncSession):
    try:
        res_valid = await check_valid(data=body)
        logger.info("Result of input data validation: %s", res_valid)
        if not res_valid:
            logger.info("Start LLM")
            client = await conn_client()
            result = await handler(data=body, client=client)
            logger.error("Result LLM data: %s", result)

            data_object = TelegramData.model_validate(result)
            logger.error("result LLM: %s", data_object)
        else:
            data_object = res_valid

        db_item = await save_db(session=session, data=data_object)

        if db_item:
            chat_obj = body.get("chat", {})
            data_dict = {
                "id": db_item.id,
                "message": db_item.message,
                "chat_id": chat_obj.get("id"),
            }
            payload = json.dumps(data_dict)
            logger.info("Saved to DB with ID: %s", db_item.id)
            await redis_client.publish(redis_channel, payload)

    except ValidationError as ex:
        logger.error("Validation failed after LLM: %s", ex.json())
        raise HTTPException(status_code=422, detail="Invalid data structure")

    except Exception as ex:
        logger.exception("Processing error: %s")
        return JSONResponse(status_code=400, content={"status": "error"})
