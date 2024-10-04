from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = ConfigDict(env_file='.env')
    app_name: str = 'test-test'
    app_version: str = '0.1.0'
    database_url: str = 'postgresql+asyncpg://postgres:postgres@localhost:5432/cats'


settings = Settings()
