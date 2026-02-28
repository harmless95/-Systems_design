from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import logger
from core.model import TelegramData, TelegramDB


async def save_db(session: AsyncSession, data: TelegramData) -> TelegramDB | None:
    logger.info("Input data to be saved in the database.: %s", data)
    try:
        stmt = TelegramDB(**data.model_dump())
        session.add(stmt)
        await session.commit()
        await session.refresh(stmt)
        return stmt

    except SQLAlchemyError as ex:
        await session.rollback()
        logger.error("SQLAlchemy error: %s", ex)
    except Exception:
        await session.rollback()
        logger.error("Unexpected error while saving data.")
    return None
