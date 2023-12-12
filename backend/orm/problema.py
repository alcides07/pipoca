from sqlalchemy.orm import Session
from schemas.common.pagination import Metadata_Schema, Pagination_Schema
from models.problema import Problema
from models.tag import Tag
from schemas.problema import Problema_Create


def read_problemas(db: Session, common: Pagination_Schema):
    problemas = db.query(Problema).offset(
        common.offset).limit(common.limit)
    total = db.query(Problema).count()
    metadata = Metadata_Schema(
        count=problemas.count(), total=total, offset=common.offset, limit=common.limit)

    return problemas.all(), metadata


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
