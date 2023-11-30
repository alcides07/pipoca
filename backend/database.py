from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from decouple import config

DATABASE_URL = config("DATABASE_URL")
DATABASE_URL_DEV = config("DATABASE_URL_DEV")
DEV = config("DEV")

if (DEV == 0):
    engine = create_engine(DATABASE_URL)
else:
    engine = create_engine(DATABASE_URL_DEV)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
