from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from decouple import config

TEST_ENV = str(config("TEST_ENV"))
if (TEST_ENV != "1"):
    DATABASE_URL = str(config("DATABASE_URL"))
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
