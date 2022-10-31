from typing import Set

from pydantic import AnyHttpUrl, BaseSettings, PostgresDsn


class Settings(BaseSettings):
    PROJECT_NAME: str = 'MedHub FastAPI Template'
    API_V0_STR: str = '/v0'
    API_V1_STR: str = '/v1'

    SUPERTOKENS_CONNECTION_URI: AnyHttpUrl | None = None
    SUPERTOKENS_WEBSITE_DOMAIN: AnyHttpUrl | None = None
    SUPERTOKENS_API_DOMAIN: AnyHttpUrl | None = None
    SUPERTOKENS_API_KEY: str | None = None
    SUPERTOKENS_API_BASE_PATH: str = '/auth'
    SUPERTOKENS_WEBSITE_BASE_PATH: str = '/'

    BACKEND_CORS_ORIGINS: Set[AnyHttpUrl] = set()

    SQLALCHEMY_DATABASE_URI: PostgresDsn


settings = Settings()
