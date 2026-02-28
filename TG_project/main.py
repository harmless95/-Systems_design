import asyncio
import json
import os
import httpx
import logging
import redis.asyncio as redis

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message

logger = logging.getLogger("ProjectTG")

TG_TOKEN = os.getenv("TG_TOKEN")
URL_APP = os.getenv("URL_APP")

bot = Bot(token=TG_TOKEN)
dp = Dispatcher()

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
redis_channel = "tasks_llm"
redis_client = redis.Redis(
    host=REDIS_HOST,
    port=6379,
    decode_responses=True,
)


async def get_redis(bot: Bot):
    pubsub = redis_client.pubsub()
    await pubsub.subscribe(redis_channel)
    logger.info(f"Subscribed to {redis_channel}")

    try:
        async for message in pubsub.listen():
            logger.info(f"Raw message from Redis: {message}")
            if message["type"] == "message":

                data_app = json.loads(message["data"])
                logger.info("Result app: %s", data_app)
                chat_id = data_app.get("chat_id")
                if not chat_id:
                    continue
                id_data = data_app.get("id")
                message_data = data_app.get("message")
                if isinstance(message_data, (dict, list)):
                    message_data = json.dumps(
                        message_data, ensure_ascii=False, indent=2
                    )
                text = (
                    f"<b>Данные успешно сохранены</b>\n\n"
                    f"<b>ID записи:</b> <code>{id_data}</code>\n"
                    f"<b>Содержимое:</b>\n<pre>{message_data}</pre>"
                )
                await bot.send_message(chat_id, text, parse_mode="HTML")
    except Exception as e:
        logger.error(f"Ошибка Redis: {e}")
    finally:
        await pubsub.unsubscribe(redis_channel)
    await asyncio.sleep(0.1)


async def handler_message(message: Message):

    data_json = message.model_dump()
    logger.error("Data TG: %s, %s", type(data_json), data_json)
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url=URL_APP, json=data_json)
            logger.error("Resp: %s", response)
            if response.status_code == 202:
                return "Сообщение обработанно"

            logger.warning("API Error %s: %s", response.status_code, response.text)
            return "Не удалось обработать данные"

    except httpx.ReadTimeout:
        return "Сервер слишком долго думал, но мы продолжаем обработку"
    except Exception as ex:
        logger.exception("Webhook sending failed")
        return "Ошибка связи с сервером"


@dp.message(CommandStart())
async def get_start(message: Message):
    await message.answer(
        f"Привет, <b>{message.from_user.full_name}</b>! Укажите по каким навыкам искать?",
        parse_mode="HTML",
    )


@dp.message(F.text)
async def message_text(message: Message):
    await message.answer("Сообщение принято")
    result_app = await handler_message(message=message)
    await message.answer(result_app)


async def main():
    redis_tasks = asyncio.create_task(get_redis(bot))
    try:
        await dp.start_polling(bot)
    finally:
        redis_tasks.cancel()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped")
