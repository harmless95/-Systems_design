from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from core.config import setting


class HelperDB:

    def __init__(
        self,
        url: str,
        echo: bool,
        echo_pool: bool,
        pool_size: int,
        max_overflow: int,
    ):
        self.async_engine = create_async_engine(
            url=url,
            echo=echo,
            echo_pool=echo_pool,
            pool_size=pool_size,
            max_overflow=max_overflow,
        )
        self.fabric_session = async_sessionmaker(
            bind=self.async_engine,
            autoflush=False,
            expire_on_commit=False,
        )

    async def dispose(self) -> None:
        await self.async_engine.dispose()

    async def session_getter(self) -> AsyncGenerator[AsyncSession | None]:
        async with self.fabric_session() as session:
            yield session
            await session.close()


helper_db = HelperDB(
    url=str(setting.db.url_app),
    echo=setting.db.echo,
    echo_pool=setting.db.echo_pool,
    pool_size=setting.db.pool_size,
    max_overflow=setting.db.max_overflow,
)
