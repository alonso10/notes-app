import contextlib
from typing import AsyncIterator

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
    AsyncSession,
    AsyncEngine,
    AsyncConnection,
    AsyncAttrs,
)


# engine = create_async_engine(settings.database_url, echo=True, future=True)
# async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class DatabaseSessionManager:
    def __init__(self):
        self._engine: AsyncEngine | None = None
        self._sessionmaker: async_sessionmaker | None = None

    def init(self, host: str):
        self._engine = create_async_engine(host)
        self._sessionmaker = async_sessionmaker(
            autocommit=False, bind=self._engine, class_=AsyncSession
        )

    async def close(self):
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        await self._engine.dispose()
        self._engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise Exception("DatabaseSessionManager is not initialized")

        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    # Used for testing
    async def create_all(self, connection: AsyncConnection):
        await connection.run_sync(Base.metadata.create_all)

    async def drop_all(self, connection: AsyncConnection):
        await connection.run_sync(Base.metadata.drop_all)


sessionmanager = DatabaseSessionManager()


async def get_db():
    async with sessionmanager.session() as session:
        yield session


async def init_models(connection: AsyncConnection):
    await sessionmanager.create_all(connection)


"""
async def get_db():
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
"""
