from fastapi import APIRouter, status

from api.Dependencies.tasks_background import create_tasks
from core.config import logger

router_app = APIRouter()


@router_app.post(
    "/webhook",
    status_code=status.HTTP_202_ACCEPTED,
)
async def new_message(body: dict) -> dict:
    logger.info("Input data: %s", body)
    await create_tasks.kiq(body)
    return {"status": "ok"}
