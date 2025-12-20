from typing import AsyncGenerator

from sqlalchemy.ext.automap import automap_base

from telemetry.db.connection import SessionManager


class DbModelsManager:
    def __init__(self):
        self._base = None
    
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "instance"):
            cls.instance = super(DbModelsManager, cls).__new__(cls)
        return cls.instance

    async def init_db_models(self):
        self._base = automap_base()
        async with SessionManager().engine.begin() as conn:
            await conn.run_sync(self._base.prepare)

    def get_tm_model(self):
        return self._base.classes.telemetry


async def get_db_models_manager() -> AsyncGenerator[DbModelsManager, None]:
    manager = DbModelsManager()
    await manager.init_db_models()

    yield manager
