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
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()
