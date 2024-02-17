from typing import Any
from models.administrador import Administrador
from models.user import User
from sqlalchemy.orm import Session
from utils.get_nested_attr import get_nested_attr


def user_autenthicated(token: str, db: Session):
    from dependencies.authenticated_user import get_authenticated_user
    return get_authenticated_user(token, db)


async def has_authorization_object_single(
    model: Any,
    db: Session,
    db_object: Any,
    token: str,
    path_has_user_key: str
):
    """Verifica se o usuário autenticado possui autorização para manipular um objeto de um modelo qualquer do banco de dados.

    Args:
        model (Any): Modelo do banco de dados o qual se deseja manipular
        db (Session): Sessão de banco de dados
        db_object (Any): Objeto específico do modelo que se deseja manipular
        token (str): Token do usuário autenticado
        path_has_user_key (str): Caminho possivelmente aninhado que indica o atributo que realmente armazena a chave estrangeira do usuário. A fim de verificar se o usuário autenticado tem permissão para operar em um objeto específico.

    Returns:
        bool: Retorna True ou False conforme a autorização do usuário para efetuar a ação desejada.
    """
    model_name = (model.__name__).lower()
    path_has_user_key = path_has_user_key.lower()

    if (isinstance(db_object, User)):
        user_id = getattr(db_object, "id")

    elif (model_name == path_has_user_key):
        user_id = getattr(db_object, "usuario_id")

    else:
        path = f"{path_has_user_key}.usuario_id"
        user_id = get_nested_attr(db_object, path)

    user_db = await user_autenthicated(token, db)

    return is_admin(user_db) or user_id == user_db.id


def is_admin(user):
    if (isinstance(user, Administrador)):
        return True
    return False


def is_user(user):
    if (isinstance(user, User)):
        return True
    return False
