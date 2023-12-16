from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from decouple import config

DATABASE_CONTAINER = config("DATABASE_CONTAINER")
DATABASE_LOCAL = config("DATABASE_LOCAL")
USE_DOCKER = config("USE_DOCKER")

engine = create_engine(DATABASE_LOCAL, connect_args={
                       "check_same_thread": False})

if (USE_DOCKER == "1"):
    engine = create_engine(DATABASE_CONTAINER)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
