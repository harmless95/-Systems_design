import uvicorn
from fastapi import FastAPI, status
from contextlib import asynccontextmanager

from api.router import router_app
from core.model import helper_db
from core.config import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        yield
    finally:
        await helper_db.dispose()


app = FastAPI(lifespan=lifespan)
app.include_router(router=router_app)


@app.get(
    "/",
    status_code=status.HTTP_200_OK,
)
async def get_hello() -> dict[str, str]:
    logger.info("Start APP Hello")
    return {
        "message": "Hello",
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
