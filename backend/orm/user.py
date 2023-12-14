from sqlalchemy.orm import Session
from models.user import User
from schemas.user import User_Create


def create_user(db: Session, user: User_Create):
    db_user = User(
        **user.model_dump(exclude=set(["passwordConfirmation"])))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
