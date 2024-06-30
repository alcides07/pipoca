from decouple import config


def get_session_local():
    from database import SessionLocal
    return SessionLocal()


def get_db():
    db = get_session_local()
    try:
        yield db
    finally:
        db.close()
