from pydantic import BaseSettings


class Settings(BaseSettings):
    # database settings
    database_url: str
    test_database_url: str
    app_secret: str
    # test_secret: str
    # main app settings
    debug: bool 

    # proxy settings
    root_path: str = ''

    class Config:
        env_file = ".env"
