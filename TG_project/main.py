import asyncio
import os
import httpx
import logging
import json

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message

logger = logging.getLogger("ProjectTG")

TG_TOKEN = os.getenv("TG_TOKEN")
URL_APP = os.getenv("URL_APP")

bot = Bot(token=TG_TOKEN)
dp = Dispatcher()


async def handler_message(message: Message):
    data = message.json()
    data_json = json.loads(data)
    logger.error("Data TG: %s, %s", type(data_json), data_json)
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url=URL_APP, json=data_json)
            logger.error("Resp: %s", response)
            if response.status_code == 200:
                return True
            else:
                logger.warning(f"Приложение вернуло ошибку: {response.status_code}")
                return False
    except Exception as ex:
        logger.error("Error sending webhook: %s", ex)


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
    if result_app:
        await message.answer("Сообщение обработанно")
    else:
        await message.answer("Произошла ошибка при связи с сервером")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
