from fastapi import FastAPI
from models.common.custom_exception import Custom_Exception
from routers import openapi, user, problema
from database import engine, Base
from fastapi.openapi.utils import get_openapi
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


Base.metadata.create_all(bind=engine)

app = FastAPI(docs_url=None,
              redoc_url=None,
              swagger_ui_parameters={"syntaxHighlight.theme": "nord"})

app.include_router(openapi.router)
app.include_router(user.router)
app.include_router(problema.router)


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
    app.openapi_schema = openapi_schema
    return app.openapi_schema


@app.exception_handler(Custom_Exception)
async def exception_handler(request: Request, exception: Custom_Exception):
    return JSONResponse(
        status_code=exception.status_code,
        content={
            "error": exception.error
        },
    )

app.openapi = custom_openapi
