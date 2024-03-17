from fastapi import Depends, HTTPException, status
from dependencies.authenticated_user import get_authenticated_user
from models.administrador import Administrador
from routers.auth import oauth2_scheme
from sqlalchemy.orm import Session
from dependencies.database import get_db


async def is_admin_dependencies(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    user = await get_authenticated_user(token, db)
    if (isinstance(user, Administrador)):
        return True

    raise HTTPException(status.HTTP_401_UNAUTHORIZED)
