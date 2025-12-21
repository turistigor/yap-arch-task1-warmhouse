from datetime import datetime
from fastapi.routing import APIRouter

health_router = APIRouter(prefix="/api/v1")


@health_router.get("/healthcheck")
async def health_check() -> dict:
    return {"status": "OK"}
