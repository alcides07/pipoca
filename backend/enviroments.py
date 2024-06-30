from decouple import config

ENV = str(config("ENV"))
ALGORITHM = str(config("ALGORITHM"))
SECRET_KEY = str(config("SECRET_KEY"))
VERSION_API = str(config("VERSION_API", default="0.0.0"))
TOKEN_EXPIRE_MINUTES = float(config("TOKEN_EXPIRE_MINUTES"))

DATABASE_URL = str(config("DATABASE_URL"))
FRONT_BASE_URL = str(config("FRONT_BASE_URL"))
API_BASE_URL = str(config("API_BASE_URL"))
BROKER_URL = str(config("BROKER_URL"))

if (ENV == "production"):
    PASSWORD_EMAIL = str(config("PASSWORD_EMAIL"))
