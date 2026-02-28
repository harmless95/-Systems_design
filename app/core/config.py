from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, PostgresDsn

from core.log_settings import setup_logger

BASE_DIR = Path(__file__).resolve().parent.parent

# fmt: off
LOG_DEFAULT_FORMAT = "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
# fmt: on


class Redis(BaseModel):
    host: str


class AIAssistant(BaseModel):
    token: str


class PostgresDB(BaseModel):
    url: PostgresDsn
    url_app: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class LoggingConfig(BaseModel):
    log_level: Literal[
        "DEBUG",
        "INFO",
        "WARNING",
        "ERROR",
        "CRITICAL",
    ] = "WARNING"
    log_format: str = LOG_DEFAULT_FORMAT
    log_file: str = BASE_DIR / "data_logs/error_logs.log"


class Setting(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(
            BASE_DIR / ".env.template",
            BASE_DIR / ".env",
        ),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )
    db: PostgresDB
    ai_bot: AIAssistant
    redis: Redis
    log: LoggingConfig = LoggingConfig()


setting = Setting()

logger = setup_logger(
    log_level=setting.log.log_level,
    log_file=setting.log.log_file,
    log_format=setting.log.log_format,
)
