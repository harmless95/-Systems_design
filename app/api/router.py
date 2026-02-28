from typing import Annotated
from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import ValidationError

from api.crud.telegram_crud import save_db
from core.config import logger
from core.model import TelegramData, helper_db
from api.Dependencies.llm_connect import conn_client
from api.Dependencies.validation_data import check_valid

from api.Dependencies import handler

router_app = APIRouter()


@router_app.post(
    "/webhook",
    status_code=status.HTTP_200_OK,
)
async def new_message(
    session: Annotated[AsyncSession, Depends(helper_db.session_getter)],
    body: dict,
) -> dict:
    logger.info("Input data: %s", body)
    try:
        res_valid = await check_valid(data=body)
        logger.info("Result of input data validation: %s", res_valid)
        if not res_valid:
            logger.info("Start LLM")
            client = await conn_client()
            result = await handler(data=body, client=client)
            logger.error("Result LLM data: %s", result)

            data_object = TelegramData.model_validate(result)
            logger.error("result LLM: %s", data_object)
        else:
            data_object = res_valid

        db_item = await save_db(session=session, data=data_object)

        if db_item:
            logger.info("Saved to DB with ID: %s", db_item.id)

        return {"status": "ok"}

    except ValidationError as ex:
        logger.error("Validation failed after LLM: %s", ex.json())
        raise HTTPException(status_code=422, detail="Invalid data structure")

    except Exception as ex:
        logger.exception("Processing error: %s")
        return JSONResponse(status_code=400, content={"status": "error"})
