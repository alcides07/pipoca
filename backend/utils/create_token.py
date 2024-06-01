from jose import jwt
from datetime import datetime, timedelta, timezone
from decouple import config


def create_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + expires_delta
    expire_timestamp = int(expire.timestamp())
    to_encode.update({"exp": expire_timestamp})

    SECRET_KEY = str(config("SECRET_KEY"))
    ALGORITHM = str(config("ALGORITHM"))

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
