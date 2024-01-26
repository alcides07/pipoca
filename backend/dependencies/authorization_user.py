from typing import Any
from models.user import User
from sqlalchemy.orm import Session


def user_autenthicated(token: str, db: Session):
    from dependencies.authenticated_user import get_authenticated_user
    return get_authenticated_user(token, db)


async def has_authorization_user(
    model: Any,
    db: Session,
    db_object: Any,
    token: str = "",
    model_has_user_key: Any = None,
):

    obj_model_has_user_key = db_object

    if (model != model_has_user_key and hasattr(db_object, model_has_user_key.__name__.lower())):
        obj_model_has_user_key = getattr(
            db_object, model_has_user_key.__name__.lower())

    user = await user_autenthicated(token, db)

    if (isinstance(obj_model_has_user_key, User) and user.id == obj_model_has_user_key.id):
        return True

    elif (hasattr(obj_model_has_user_key, "usuario_id") and obj_model_has_user_key.usuario_id == user.id):
        return True

    return False
