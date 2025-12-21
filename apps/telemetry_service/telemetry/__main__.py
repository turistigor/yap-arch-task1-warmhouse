import asyncio as aio
from contextlib import asynccontextmanager
from os import environ

import uvicorn
from fastapi import FastAPI
from loguru import logger

from telemetry.api import health_router, tm_stat_router
from telemetry.data_flow import StorageManager, TmManager, get_devices
from telemetry.db import DbModelsManager, get_db
from telemetry.settings import Settings

st = Settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info('Starting telemetry system...')

    db_models_manager = DbModelsManager()
    await db_models_manager.init_db_models()
    db_tm_model = db_models_manager.get_tm_model()

    devices = await get_devices(st.devices_url)

    tm_queue = aio.Queue()
    tm_manager = TmManager(
        devices,
        tm_queue, 
        polling_interval=st.polling_interval_sec,
        temperature=st.temp_api_url,
    )
    tm_manager.start()

    db_session = await anext(get_db())
    st_manager = StorageManager(
        db_session,
        db_tm_model,
        tm_queue,
        st.polling_interval_sec,
        batch_size=3,
    )
    st_manager.start()

    logger.success(f'Telemetry system API started on {st.api_url}')

    yield

    logger.info("Stopping telemetry system...")

    if tm_manager:
        await tm_manager.stop()
    
    if st_manager:
        await st_manager.stop()


async def main():
    app = FastAPI(
        lifespan=lifespan,
        title="Touristic maps",
        docs_url="/api/v1/swagger",
        openapi_url="/api/v1/openapi",
        version="0.1.0"
    )

    app.include_router(tm_stat_router)
    app.include_router(health_router)

    config = uvicorn.Config(app, host='0.0.0.0', port=8082, log_level="info")
    server = uvicorn.Server(config)    

    await server.serve()


if __name__ == '__main__':
    aio.run(main())