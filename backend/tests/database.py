from sqlalchemy import text
from database import engine
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from database import Base
from decouple import config

DATABASE_LOCAL_TEST = str(config("DATABASE_LOCAL_TEST"))

engine = create_engine(
    DATABASE_LOCAL_TEST,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


def get_db_test():
    try:
        USE_DOCKER = config("USE_DOCKER")
        if (USE_DOCKER == "0"):
            with engine.connect() as connection:
                connection.execute(text('PRAGMA foreign_keys=ON'))

        db = TestingSessionLocal()
        yield db
    finally:
        db.close()
