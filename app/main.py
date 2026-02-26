import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def get_hello() -> dict[str, str]:
    return {
        "message": "Hello",
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
