import asyncio
import os
import logging

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message

TG_TOKEN = os.getenv("TG_TOKEN")
URL_APP = os.getenv("URL_APP")

logger = logging.getLogger("TG_app")

bot = Bot(token=TG_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start(message: Message):
    await message.answer(
        f"Привет, <b>{message.from_user.full_name}</b>!",
        parse_mode="HTML",
    )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
