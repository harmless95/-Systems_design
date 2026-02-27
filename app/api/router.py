from typing import Annotated
from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from api.crud.telegram_crud import save_db
from core.model import TelegramData, helper_db

from api.Dependencies.llm_connect import conn_client
from api.Dependencies.validation_data import check_valid
from pydantic import ValidationError

from api.Dependencies import handler

router_app = APIRouter()
logger = logging.getLogger("WebhookAPP")


@router_app.post(
    "/webhook",
    status_code=status.HTTP_200_OK,
)
async def new_message(
    session: Annotated[AsyncSession, Depends(helper_db.session_getter)],
    body: dict,
) -> dict:
    res_valid = await check_valid(data=body)
    if not res_valid:
        client = await conn_client()
        result = await handler(data=body, client=client)
        logger.error("Result LLM data: %s", result)

        prepared_data = {
            "username": result.get("username") or "unknown",
            "message": result.get("message") or "",
        }

        try:
            data_object = TelegramData.model_validate(prepared_data)
            logger.error("result LLM: %s", data_object)
        except ValidationError as ex:
            logger.critical("Даже после ИИ данные не валидны: %s", ex)
            return {
                "status": "error",
                "reason": "invalid_data",
            }
    else:
        data_object = res_valid
    db_item = await save_db(session=session, data=data_object)
    logger.info("Saved to DB with ID: %s", db_item.id)

    return {"status": "ok", "delivered": True}
