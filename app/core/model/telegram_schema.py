from pydantic import BaseModel, ConfigDict


class TelegramData(BaseModel):
    username: str
    message: str

    model_config = ConfigDict(
        from_attributes=True,
    )
