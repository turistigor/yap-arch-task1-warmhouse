
import asyncio as aio
from typing import Optional

import httpx
from loguru import logger

from telemetry.data_flow.tm_model import TmMeasure
from telemetry.data_flow.devices import Devices


class TmManager:
    def __init__(
        self, devices: Devices,
        storage_queue: aio.Queue,
        polling_interval: int, 
        **tm_urls,
    ):
        self._devices = devices
        self._storage_queue = storage_queue
        self._polling_interval_sec = polling_interval
        self._tm_sources = {**tm_urls}

        self._tm_task: Optional[aio.Task] = None
        self._tm_stopped = False
    
    def start(self):
        self._tm_stopped = False
        self._tm_task = aio.create_task(self._run_telemetry())
    
    async def stop(self):
        self._tm_stopped = True
        await self._tm_task

    async def _run_telemetry(self):
        while self._tm_stopped is False:
            async with httpx.AsyncClient() as client:
                for dev in self._devices:
                    source = self._tm_sources[dev.type]
                    tm_addr = f'{source}/{dev.id}'

                    try:
                        resp = await client.get(tm_addr)
                    except httpx.RequestError as ex:
                        logger.error(ex)
                    else:
                        await self._process_tm_response(resp)

                await aio.sleep(self._polling_interval_sec)

    async def _process_tm_response(self, resp: httpx.Response) -> TmMeasure:
        try:
            resp.raise_for_status()
        except httpx.HTTPStatusError as ex:
            logger.error(ex)
            return

        payload = resp.json()
        measure = TmMeasure(**payload)
        await self._storage_queue.put(measure)
        logger.debug(measure)
