from datetime import datetime, timedelta, timezone
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, Query, Depends
from fastapi.routing import APIRouter
from pydantic import BaseModel

from telemetry.db import DbModelsManager, get_db, get_db_models_manager
from telemetry.tm_stat import get_tm_stat

tm_stat_router = APIRouter(prefix="/api/v1/stat")


class TelemetryStatsResponse(BaseModel):
    sensor_id: int
    min_value: float
    max_value: float
    average_value: float


@tm_stat_router.get("/get_tm")
async def get_telemetry_stats(
    sensor_id: int = Query(..., ge=1),
    start_time: Optional[str] = Query(None),
    end_time: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
    db_models_manager: DbModelsManager = Depends(get_db_models_manager)
) -> TelemetryStatsResponse:
    """
    Получить статистику телеметрии по sensor_id за интервал времени

    Параметры:
    - sensor_id: ID датчика (обязательный)
    - start_time: начало интервала (по умолчанию: 24 часа назад от end_time)
    - end_time: конец интервала (по умолчанию: текущее время)
    """
    if end_time:
        end_time = datetime.fromisoformat(end_time)
    else:
        end_time = datetime.now(timezone.utc)

    if start_time: 
       start_time = datetime.fromisoformat(start_time)
    else:
        start_time = end_time - timedelta(hours=24)

    if start_time >= end_time:
        raise HTTPException(400, "start_time must be earlier than end_time")

    tm_model = db_models_manager.get_tm_model()
    try:
        stats = await get_tm_stat(tm_model, db, sensor_id, start_time, end_time)
    except Exception as e:
        raise HTTPException(500, f"Internal error: {str(e)}")
    
    if stats is None or stats.min is None:
        raise HTTPException(
            404,
            f'No data for sensor {sensor_id} in specified time range'
        )
    
    return TelemetryStatsResponse(
        sensor_id=sensor_id,
        min_value=float(stats.min),
        max_value=float(stats.max),
        average_value=float(stats.avg)
    )
