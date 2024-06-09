from decouple import config

ENV = str(config("ENV"))
ALGORITHM = str(config("ALGORITHM"))
SECRET_KEY = str(config("SECRET_KEY"))
VERSION_API = str(config("VERSION_API", default="0.0.0"))


if (ENV == "production"):
    DATABASE_URL = str(config("PRODUCTION_DATABASE_URL"))
    FRONT_BASE_URL = str(config("PRODUCTION_FRONT_BASE_URL"))
    API_BASE_URL = str(config("PRODUCTION_API_BASE_URL"))
    BROKER_URL = str(config("PRODUCTION_BROKER_URL"))
    PASSWORD_EMAIL = str(config("PRODUCTION_PASSWORD_EMAIL"))


elif (ENV == "test"):
    DATABASE_URL = str(config("TEST_DATABASE_URL"))
    FRONT_BASE_URL = str(config("DEV_FRONT_BASE_URL"))
    API_BASE_URL = str(config("DEV_API_BASE_URL"))
    BROKER_URL = str(config("DEV_BROKER_URL"))


elif (ENV == "development"):
    DATABASE_URL = str(config("DEV_DATABASE_URL"))
    FRONT_BASE_URL = str(config("DEV_FRONT_BASE_URL"))
    API_BASE_URL = str(config("DEV_API_BASE_URL"))
    BROKER_URL = str(config("DEV_BROKER_URL"))
