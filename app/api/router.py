from typing import Annotated
from fastapi import APIRouter, status, Depends, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from api.Dependencies.tasks_background import create_tasks
from core.config import logger
from core.model import helper_db

router_app = APIRouter()


@router_app.post(
    "/webhook",
    status_code=status.HTTP_202_ACCEPTED,
)
async def new_message(
    session: Annotated[AsyncSession, Depends(helper_db.session_getter)],
    tasks_data: BackgroundTasks,
    body: dict,
) -> dict:
    logger.info("Input data: %s", body)

    tasks_data.add_task(create_tasks, body, session)
    return {"status": "ok"}
