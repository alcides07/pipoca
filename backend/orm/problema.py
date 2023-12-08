from sqlalchemy.orm import Session
from schemas.common.pagination import pagination_schema
from models.problema import Problema
from models.tag import Tag
from schemas.problema import Problema_Create


def read_problemas(db: Session, common: pagination_schema):
    return db.query(Problema).offset(common.skip).limit(common.limit).all()


def create_problema(db: Session, problema: Problema_Create):
    db_problema = Problema(**problema.model_dump(exclude="tags"))
    db.add(db_problema)

    for tag in problema.tags:
        db_tag = db.query(Tag).filter(Tag.nome == tag).first()
        if db_tag is None:
            db_tag = Tag(nome=tag)
            db.add(db_tag)
        db_problema.tags.append(db_tag)

    db.commit()
    db.refresh(db_problema)

    return db_problema
