import asyncio
import os
import logging
import httpx

TG_TOKEN = os.getenv("TG_TOKEN")
URL_APP = os.getenv("URL_APP")
URL_TG = f"https://api.telegram.org/bot{TG_TOKEN}/setWebhook"
WEBHOOK_URL = f"{URL_APP}/webhook"

logger = logging.getLogger("TG_app")


async def set_webhook():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{URL_TG}?url={WEBHOOK_URL}")
            if response.status_code == 200:
                data = response.json()
                logger.info(f"Message: %s", data)
    except Exception as ex:
        logger.error("Error: %s", ex)


async def main():
    await set_webhook()


if __name__ == "__main__":
    asyncio.run(main())
