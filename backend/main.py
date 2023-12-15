from fastapi import FastAPI
from utils.errors import errors
from openapi.validation_exception import validation_exception_handler
from routers.index import routes
from database import engine, Base
from fastapi.openapi.utils import get_openapi
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError


Base.metadata.create_all(bind=engine)

app = FastAPI(docs_url=None,
              redoc_url=None,
              swagger_ui_parameters={"syntaxHighlight.theme": "nord"},
              responses={
                  401: errors[401]
              },
              exception_handlers={
                  RequestValidationError: validation_exception_handler
              }
              )

for router in routes:
    app.include_router(router)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="API Juiz Online",
        version="0.0.1",
        summary="",
        description="API em desenvolvimento",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }

    # Remove retorno HTTP 422 por padrão em GET e DELETE
    for method in openapi_schema["paths"]:
        try:
            del openapi_schema["paths"][method]["get"]["responses"]["422"]
            del openapi_schema["paths"][method]["delete"]["responses"]["422"]
        except KeyError:
            pass

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
