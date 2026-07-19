from typing import List

from sqlalchemy.engine import URL
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # App
    APP_NAME: str = "Euro Link Portal"
    APP_ENV: str = "development"
    APP_DEBUG: bool = True
    BASE_URL: str = "http://127.0.0.1:8000"

    # Security
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    SALT_KEY: str = ""
    OPENAI_API_KEY: str = ""
    GEMINI_API_KEY: str = ""

    # Database
    DB_HOST: str
    DB_PORT: int = 3306
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_DRIVER: str = "mysql+pymysql"

    # CORS — comma-separated string in .env
    ORIGINS: str = ""

    @property
    def origins_list(self) -> List[str]:
        return [o.strip() for o in self.ORIGINS.split(",") if o.strip()]

    @property
    def database_url(self) -> URL:
        return URL.create(
            drivername=self.DB_DRIVER,
            username=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT,
            database=self.DB_NAME,
        )


settings = Settings()
