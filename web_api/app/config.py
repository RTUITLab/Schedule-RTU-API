from pydantic import BaseSettings


class Settings(BaseSettings):

    database_url: str = 'postgresql://postgres:ujhrb1331@localhost:5433/postgres'
    app_secret: str = '123'
    root_path: str = ''

    class Config:
        env_file = ".env"
