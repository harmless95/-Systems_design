import asyncio
import os
import httpx
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message

logger = logging.getLogger("ProjectTG")

TG_TOKEN = os.getenv("TG_TOKEN")
URL_APP = os.getenv("URL_APP")

bot = Bot(token=TG_TOKEN)
dp = Dispatcher()


async def handler_message(message: Message):

    data_json = message.model_dump()
    logger.error("Data TG: %s, %s", type(data_json), data_json)
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url=URL_APP, json=data_json)
            logger.error("Resp: %s", response)
            if response.status_code == 200:
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
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
