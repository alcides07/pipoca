from sqlalchemy.orm import Session
from models.problema import Problema
from models.tag import Tag
from schemas.problema import ProblemaCreate


def create_problema(db: Session, problema: ProblemaCreate):
    db_problema = Problema(**problema.model_dump(exclude=set(["tags"])))
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
