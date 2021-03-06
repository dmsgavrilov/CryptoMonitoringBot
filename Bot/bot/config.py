import os
from typing import Optional, Dict, Any

from pydantic import BaseSettings, PostgresDsn, validator, HttpUrl
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    TOKEN: str = os.getenv('TOKEN')

    PERCENT_CHANGE: float = float(os.getenv('PERCENT_CHANGE'))

    CURRENCY_URL: HttpUrl = 'https://bitinfocharts.com/ru/crypto-kurs'

    SENTRY_DSN: Optional[HttpUrl]
    POSTGRES_SERVER: str = "postgres"
    DB_USER: str = "db_user"
    DB_USER_PASSWORD: str = "qwerty"
    POSTGRES_DB: str = "app"
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None
    SQLALCHEMY_POOL_TIMEOUT: int = 30
    SQLALCHEMY_POOL_SIZE: int = 20
    SQLALCHEMY_MAX_OVERFLOW: int = 40

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("DB_USER"),
            password=values.get("DB_USER_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB', 'app')}",
        )


settings = Settings()
