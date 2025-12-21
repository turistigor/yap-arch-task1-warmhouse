from datetime import datetime

from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase


async def get_tm_stat(
    tm_model: DeclarativeBase,
    db: AsyncSession,
    sensor_id: int,
    start_time: datetime,
    end_time: datetime,
):
    query = select(
        func.min(tm_model.value).label('min'),
        func.max(tm_model.value).label('max'),
        func.avg(tm_model.value).label('avg')
    ).where(
        and_(
            tm_model.sensor_id == sensor_id,
            tm_model.timestamp >= start_time,
            tm_model.timestamp <= end_time
        )
    )

    result = await db.execute(query)
    return result.fetchone()
