from database import SessionLocal, engine
from sqlalchemy import text
from decouple import config


def get_db():
    db = SessionLocal()
    try:
        USE_DOCKER = config("USE_DOCKER")

        if (USE_DOCKER == "0"):
            with engine.connect() as connection:
                connection.execute(text('PRAGMA foreign_keys=ON'))
        yield db
    finally:
        db.close()
