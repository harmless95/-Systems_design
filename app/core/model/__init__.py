__all__ = (
    "TelegramData",
    "Base",
    "TelegramDB",
)

from .telegram_schema import TelegramData

from .Base import Base
from .telegram import TelegramDB
