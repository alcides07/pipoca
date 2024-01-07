from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from decouple import config

DATABASE_CONTAINER = str(config("DATABASE_CONTAINER"))
DATABASE_LOCAL = str(config("DATABASE_LOCAL"))
USE_DOCKER = config("USE_DOCKER")

engine = create_engine(DATABASE_LOCAL, connect_args={
                       "check_same_thread": False})

if (USE_DOCKER == "1"):
    engine = create_engine(DATABASE_CONTAINER)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
