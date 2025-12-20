import asyncio as aio
from typing import Iterable, Optional

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from telemetry.data_flow.tm_model import TmMeasure


class StorageManager:
    def __init__(
        self,
        db_session: AsyncSession,
        db_tm_model,        
        tm_queue: aio.Queue,
        polling_interval_sec: int,
        batch_size: int = 10
    ):
        self._tm_db = db_session
        self._tm_db_model = db_tm_model
        self._tm_queue = tm_queue
        self._get_timeout = polling_interval_sec + 0.1
        self._batch_size = batch_size

        self._store_task: Optional[aio.Task] = None
        self._store_stopped = False

    def start(self):
        self._store_stopped = False
        self._tm_task = aio.create_task(self._run_storing())
    
    async def stop(self):
        self._store_stopped = True
        await self._tm_task

    async def _run_storing(self):
        measures = []

        while self._store_stopped is False:
            measure = await self._get_measure()
            if measure is None:
                continue

            tm_db_model = self._tm_db_model(**measure.model_dump(exclude_unset=True))
            measures.append(tm_db_model)

            if len(measures) >= self._batch_size:
                await self._store_measures(measures)
                measures.clear()

        await self._store_measures(measures)

    async def _get_measure(self) -> TmMeasure:
        try:
            return await aio.wait_for(
                self._tm_queue.get(), timeout=self._get_timeout,
            )
        except aio.TimeoutError:
            if self._store_stopped is False:
                logger.warning('Не удалось считать данные телеметрии из очереди')
    
    async def _store_measures(self, measures: Iterable):
        self._tm_db.add_all(measures)
        await self._tm_db.commit()
