import json

from api.Dependencies.promt_llm import PROMPT
from core.config import logger


async def handler(data: dict, client) -> dict:
    query = json.dumps(data, ensure_ascii=False)
    prompt = PROMPT.format(query=query)
    message = [{"role": "user", "content": prompt}]
    model = "llama-3.1-8b-instant"
    try:
        response = await client.chat.completions.create(
            model=model,
            messages=message,
            response_format={"type": "json_object"},
        )
        logger.info("Result of data processing: %s", response)
        result_text = response.choices[0].message.content
        return json.loads(result_text)
    except Exception as ex:
        logger.error("LLM Error: %s", ex)
        return {}
