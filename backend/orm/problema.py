from sqlalchemy.orm import Session
from schemas.common.pagination import pagination_schema
from models.problema import Problema
from schemas.problema import Problema_Create


def create_problema(db: Session, problema: Problema_Create):
    db_problema = Problema(**problema.model_dump())
    db.add(db_problema)
    db.commit()
    db.refresh(db_problema)
    return db_problema
