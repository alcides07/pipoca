from dependencies.authenticated_user import get_authenticated_user
from models.problema import Problema
from models.tag import Tag
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from sqlalchemy.orm import Session
from fastapi import status
from schemas.tag import TagCreate


async def associate_tag_with_problema(
    db: Session,
    db_tag: Tag,
    token: str,
    problema_id: int
):
    db_problema = db.query(Problema).filter(Problema.id == problema_id).first()

    if (not db_problema):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    user = await get_authenticated_user(token=token, db=db)
    if (db_problema.usuario_id != user.id):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    db_problema.tags.append(db_tag)
    db.refresh(db_problema)
    return db_tag


async def create_tag(
    db: Session,
    tag: TagCreate,
    token: str
):
    try:
        db_tag = db.query(Tag).filter(Tag.nome == tag.nome).first()
        if (not db_tag):
            db_tag = Tag(nome=tag.nome)
            db.add(db_tag)

        if (tag.problema_id):
            await associate_tag_with_problema(
                db=db,
                db_tag=db_tag,
                token=token,
                problema_id=tag.problema_id
            )

        db.commit()
        db.refresh(db_tag)

        return db_tag

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)
