from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from utils.translate import translate
from utils.errors import errors
from openapi.validation_exception import validation_exception_handler
from routers.common.index import routes
from fastapi.openapi.utils import get_openapi
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from decouple import config

TEST_ENV = str(config("TEST_ENV"))


def get_config_database():
    from database import engine, Base
    return engine, Base


if (TEST_ENV != "1"):
    engine, Base = get_config_database()
    Base.metadata.create_all(bind=engine)

app = FastAPI(docs_url=None,
              redoc_url=None,
              swagger_ui_parameters={"syntaxHighlight.theme": "nord"},
              responses={
                  401: errors[401]
              },
              exception_handlers={
                  RequestValidationError: validation_exception_handler
              }  # type: ignore
              )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.mount("/static", StaticFiles(directory="static"), name="static")


for router in routes:
    app.include_router(router)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="API do sistema PIPOCA",
        version="0.0.1",
        description="API em desenvolvimento da Plataforma Interativa de Programação On-line e Competições Acadêmicas (PIPOCA)",
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


@app.exception_handler(HTTPException)
async def exception_handler(_: Request, exception: HTTPException):
    return JSONResponse(
        status_code=exception.status_code,
        content={"error": translate(exception.detail)}
    )

app.openapi = custom_openapi
