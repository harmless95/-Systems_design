import logging

from sqlalchemy.ext.asyncio import AsyncSession

from core.model import TelegramData, TelegramDB

logger = logging.getLogger("SaveCRUD")


async def save_db(session: AsyncSession, data: TelegramData) -> TelegramDB:
    logger.error("CRUD: %s", data)
    stmt = TelegramDB(**data.model_dump())
    session.add(stmt)
    await session.commit()
    await session.refresh(stmt)
    return stmt
