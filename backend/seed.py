import random
from typing import Any
from dependencies.database import get_db
from orm.user import create_user
from schemas.user import UserCreate
from models.user import User
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field, EmailStr
import string
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine, MetaData
from database import Base
from decouple import config


def clear_database(engine):
    meta = MetaData()
    meta.reflect(bind=engine)
    meta.drop_all(bind=engine)


def create_users(db, qtd):
    user = UserCreate(username="alcides", email="alcides@email.com",
                      password="1", passwordConfirmation="1")
    create_user(db, user)

    for i in range(qtd):  # Create random users
        username = f"user-{i}"
        email = f"{username}@example.com"
        password = f"user-{i}"
        passwordConfirmation = password
        user = UserCreate(username=username, email=email,
                          password=password, passwordConfirmation=passwordConfirmation)
        create_user(db, user)
    db.close()


def main():
    # Config database
    engine = create_engine(str(config("DATABASE_LOCAL")))
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()

    # Clear database
    clear_database(engine)

    # Create tables
    Base.metadata.create_all(bind=engine)

    QTD_USERS = 15

    create_users(db, QTD_USERS)


if __name__ == "__main__":
    main()
