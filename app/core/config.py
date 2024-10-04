from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = ConfigDict(env_file='.env')
    app_name: str
    app_version: str
    database_url: str


settings = Settings()
