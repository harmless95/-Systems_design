import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

from api.router import router_app
from core.model import helper_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        yield
    finally:
        await helper_db.dispose()


app = FastAPI(lifespan=lifespan)
app.include_router(router=router_app)


@app.get("/")
async def get_hello() -> dict[str, str]:
    return {
        "message": "Hello",
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
