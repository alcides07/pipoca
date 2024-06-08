from decouple import config


def get_session_local():
    from database import SessionLocal
    return SessionLocal()


def get_db():
    TEST_ENV = str(config("TEST_ENV"))
    if (TEST_ENV != "1"):
        db = get_session_local()
        try:
            yield db
        finally:
            db.close()
