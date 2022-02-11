from pydantic import BaseSettings


class Settings(BaseSettings):
    # database settings
    database_url: str = "sqlite:///./sql_app.db"

    # main app settings
    debug: bool = False

    # proxy settings
    root_path: str = '/api'

    class Config:
        env_file = ".env"
