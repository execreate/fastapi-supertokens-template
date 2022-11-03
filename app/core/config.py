import os
from enum import Enum
from functools import lru_cache
from typing import Optional

from pydantic import AnyHttpUrl, BaseSettings, PostgresDsn


class EnvironmentEnum(str, Enum):
    PRODUCTION = "production"
    STAGING = "staging"
    DEVELOP = "develop"
    LOCAL = "local"


class GlobalSettings(BaseSettings):
    PROJECT_NAME: str = "FastAPI Template"
    API_V1_STR: str = "/v1"

    SUPERTOKENS_CONNECTION_URI: AnyHttpUrl | None = None
    SUPERTOKENS_WEBSITE_DOMAIN: AnyHttpUrl | None = None
    SUPERTOKENS_API_DOMAIN: AnyHttpUrl | None = None
    SUPERTOKENS_API_KEY: str | None = None
    SUPERTOKENS_API_BASE_PATH: str = "/auth"
    SUPERTOKENS_WEBSITE_BASE_PATH: str = "/"

    BACKEND_CORS_ORIGINS: Set[AnyHttpUrl] = set()

    ENVIRONMENT: EnvironmentEnum
    DEBUG: bool = False
    TESTING: bool = False

    DATABASE_URL: Optional[
        PostgresDsn
    ] = "postgresql://user:pass@postgres_db:5434/my_db"
    DB_ECHO_LOG: bool = False

    @property
    def async_database_url(self) -> Optional[str]:
        return (
            self.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
            if self.DATABASE_URL
            else self.DATABASE_URL
        )

    class Config:
        case_sensitive = True


class LocalSettings(GlobalSettings):
    DEBUG = True
    ENVIRONMENT = EnvironmentEnum.LOCAL


class DevelopSettings(GlobalSettings):
    DEBUG = True
    ENVIRONMENT = EnvironmentEnum.DEVELOP


class StagingSettings(GlobalSettings):
    DEBUG = False
    ENVIRONMENT = EnvironmentEnum.STAGING


class ProductionSettings(GlobalSettings):
    DEBUG = False
    ENVIRONMENT = EnvironmentEnum.PRODUCTION


class FactoryConfig:
    def __init__(self, environment: Optional[str]):
        self.environment = environment

    def __call__(self) -> GlobalSettings:
        match self.environment:
            case EnvironmentEnum.PRODUCTION:
                return ProductionSettings()
            case EnvironmentEnum.STAGING:
                return StagingSettings()
            case EnvironmentEnum.DEVELOP:
                return DevelopSettings()
            case _:
                return LocalSettings()


@lru_cache()
def get_configuration() -> GlobalSettings:
    return FactoryConfig(os.environ.get("ENVIRONMENT"))()


settings = get_configuration()
