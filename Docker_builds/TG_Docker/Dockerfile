FROM python:3.14-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY /TG_project/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY /TG_project .

ENTRYPOINT ["python", "main.py"]