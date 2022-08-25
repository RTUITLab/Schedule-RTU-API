import os

from app.database.database import engine


def automigrate():
    os.system("alembic stamp head")
    os.system("alembic revision --autogenerate")
    os.system("alembic upgrade head")
    engine.execute('DROP TABLE IF EXISTS alembic_version')


if __name__ == "__main__":
    automigrate()
