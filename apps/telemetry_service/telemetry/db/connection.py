from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from telemetry.settings import Settings


class SessionManager:
    def __init__(self):
        self._database_url = Settings().tm_db_url
        self.engine = create_async_engine(self._database_url, echo=False, future=True)
        self.session_local = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "instance"):
            cls.instance = super(SessionManager, cls).__new__(cls)
        return cls.instance

    def get_session_maker(self) -> sessionmaker:
        return sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False)

    def refresh(self) -> None:
        self.engine.dispose()
        self.engine = create_async_engine(self._database_url, echo=False, future=True)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    session_maker = SessionManager().get_session_maker()
    async with session_maker() as session:
        yield session
