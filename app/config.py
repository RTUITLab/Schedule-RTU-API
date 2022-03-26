from pydantic import BaseSettings


class Settings(BaseSettings):

    database_url: str
    app_secret: str
    root_path: str = ''

    class Config:
        env_file = ".env"
