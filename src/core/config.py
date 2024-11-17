from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class OpenAPISettings(BaseSettings):
    openai_base_url: str
    openai_api_key: str
    openai_gpt_model: str


class RedisCache(BaseSettings):
    redis_cache: str


class CeleryConfig(BaseSettings):
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str


class DatabaseConfig(BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_NAME: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    echo: bool = True
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    # авто наминг для ключей БД алембик
    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }

    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_NAME}"


class Settings(BaseModel):
    model_config = SettingsConfigDict(case_sensitive=True)
    db: DatabaseConfig = DatabaseConfig()  # type: ignore
    celery: CeleryConfig = CeleryConfig()  # type: ignore
    openapi: OpenAPISettings = OpenAPISettings()
    cache_url: RedisCache = RedisCache()
    logging: str = "DEBUG"


settings = Settings()
