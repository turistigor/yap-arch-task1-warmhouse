from typing import Iterable

import httpx
from pydantic import BaseModel, ConfigDict

type Devices = Iterable[DeviceInfo]


class DeviceInfo(BaseModel):
    model_config = ConfigDict(extra='ignore')

    id: int
    name: str
    type: str
    location: str


async def get_devices(base_url: str) -> Iterable[DeviceInfo]:
    url = f'{base_url}/api/v1/sensors'
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)

    resp.raise_for_status()
    return [DeviceInfo(**dev_info) for dev_info in resp.json()]
