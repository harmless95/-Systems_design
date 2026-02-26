FROM python:3.14.0-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY /app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY /app .

ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]