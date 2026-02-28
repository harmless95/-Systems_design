import json
import taskiq_redis
from taskiq import TaskiqDepends
import redis.asyncio as redis
from sqlalchemy.ext.asyncio import AsyncSession

from api.Dependencies import handler, check_valid, conn_client
from api.crud.telegram_crud import save_db
from core.config import logger, setting
from core.model import TelegramData, helper_db

REDIS_HOST = setting.redis.host
redis_channel = "tasks_llm"

broker = taskiq_redis.ListQueueBroker(f"redis://{REDIS_HOST}:6379/0")
redis_client = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)


@broker.task
async def create_tasks(
    body: dict, session: AsyncSession = TaskiqDepends(helper_db.session_getter)
):
    try:
        res_valid = await check_valid(data=body)

        if not res_valid:
            logger.info("Start LLM")
            client = await conn_client()
            result = await handler(data=body, client=client)

            data_object = TelegramData.model_validate(result)

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
            payload = json.dumps(data_dict, ensure_ascii=False)
            logger.info("Saved to DB with ID: %s", db_item.id)
            await redis_client.publish(redis_channel, payload)

    except Exception:
        logger.exception("Error in TaskIQ worker")
