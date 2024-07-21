import os

from pydantic import EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    ENV: str = "development"
    DEBUG: bool = True
    ENABLE_CORS_OPTION: bool = True
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    DB_URL: str = "mysql+aiomysql://admin:devpassword@127.0.0.1:3306/survey_dingdong"
    JWT_SECRET_KEY: str = "fastapi"
    JWT_ALGORITHM: str = "HS256"
    REFRESH_TOKEN_TTL: int = 60 * 60 * 14  # 14 Days
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_KEY_PREFIX: str = "dingdong-survey"
    MAIL_USERNANE: EmailStr = "dingdong-survey@gmail.com"
    MAIL_PASSWORD: str = "?"

    model_config = SettingsConfigDict(env_file=".env", env_prefix="app_")


class TestConfig(Config):
    DB_URL: (
        str
    ) = "mysql+aiomysql://admin:devpassword@127.0.0.1:3306/survey_dingdong_test"

    model_config = SettingsConfigDict(env_file=".env.test", env_prefix="test_")


class LocalConfig(Config):
    ...


def get_config():
    env = os.getenv("ENV", "local")
    config_type = {
        "test": TestConfig(),
        "local": LocalConfig(),
    }
    return config_type[env]


config: Config = get_config()
