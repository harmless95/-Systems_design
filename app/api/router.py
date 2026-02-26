from fastapi import APIRouter

from app.api.Dependencies import handler
from app.core.model import TelegramData

router_app = APIRouter()


@router_app.webhooks.post("new-message")
async def new_message_docs(body: TelegramData):
    """ "
    Это описание появится в Swagger в разделе Webhooks.
    Оно объясняет внешним системам, как слать нам данные.
    """
    pass


@router_app.post("/webhook")
async def new_message(body: TelegramData):
    result = await handler()
    print(f"Name: {body.username}, message: {body.message}")
    return {"status": "ok", "delivered": True}
