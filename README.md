# Telegram Data Extractor Bot

Асинхронный сервис для автоматического извлечения и структурирования данных из сообщений Telegram с помощью ИИ (LLM).

## Архитектура системы

- **FastAPI**: Принимает Webhook от Telegram, выполняет первичную валидацию и делегирует обработку в фон.
- **LLM Layer**: Если данные не структурированы, подключается нейросеть для парсинга текста в JSON.
- **SQLAlchemy (Async)**: Асинхронная запись в **PostgreSQL**.
- **Redis Pub/Sub**: Шина событий. После записи в БД улетает сигнал для мгновенного уведомления.
- **Aiogram Listener**: Слушает Redis-канал и отправляет пользователю результат обработки.

## Стек технологий

* **Python 3.10+** | **FastAPI** | **Aiogram 3.x**
* **PostgreSQL** (БД) | **SQLAlchemy + Alembic** (ORM & Миграции)
* **Redis** (Pub/Sub брокер)
* **Pydantic v2** (Валидация схем)
* **Httpx** (Асинхронные запросы к LLM)

## Установка и запуск

### 1. Клонирование
```
git clone https://github.com/harmless95/-Systems_design
cd -Systems_design
```
Используйте код с осторожностью.

2. Настройка окружения (.env)
В корне проекта или в соответствующих папках сервисов:
env
```
# --- PostgreSQL (Docker) ---
- POSTGRES_USER=user
- POSTGRES_PASSWORD=password
- POSTGRES_DB=db
```
```
# --- FastAPI Service ---
- APP_CONFIG__DB__URL=postgresql+asyncpg://user:password@db_systems:5432/db
- APP_CONFIG__AI_BOT__TOKEN_AI=your_llm_api_key
- APP_CONFIG__REDIS__HOST=redis
```
```
# --- Telegram Bot Service ---
- TG_TOKEN=your_telegram_token
- URL_APP=http://app_system:8000/webhook
- REDIS_HOST=redis
```
Используйте код с осторожностью.

3. Запуск через Docker (рекомендуется)

```
docker-compose up --build
```
Используйте код с осторожностью.

4. Применение миграций
После запуска контейнеров необходимо создать структуру таблиц:
```
docker-compose exec app_system alembic upgrade head
```

## API Endpoints
* Метод	Эндпоинт	Описание
* POST	/webhook	Прием обновлений от Telegram (обработка сообщений)
* GET	/health	Проверка жизнеспособности API и соединений с БД

### Жизненный цикл сообщения
- User: Пишет боту произвольный текст (навыки, вакансии, задачи).
- FastAPI: Получает Webhook. Если данные не валидны (сырой текст), отправляет их в LLM.
- LLM: Возвращает структурированный объект: {"username": "...", "message": "..."}.
- DB: SQLAlchemy сохраняет объект в Postgres.
- Redis: В канал notifications публикуется ID новой записи.
- Bot: Получает сигнал из Redis и присылает юзеру: "Данные сохранены с ID: 123".