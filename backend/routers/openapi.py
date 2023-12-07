from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi import APIRouter
from starlette.responses import RedirectResponse

router = APIRouter()


@router.get("/")
async def redirect():
    response = RedirectResponse(url="/docs")
    return response


@router.get("/docs", include_in_schema=False)
def overridden_swagger():
    return get_swagger_ui_html(openapi_url="/openapi.json",
                               title="API Juiz Online",
                               swagger_favicon_url="https://images.emojiterra.com/twitter/v13.1/512px/1f341.png")


@router.get("/redoc", include_in_schema=False)
def overridden_redoc():
    return get_redoc_html(openapi_url="/openapi.json",
                          title="API Juiz Online",
                          redoc_favicon_url="https://images.emojiterra.com/twitter/v13.1/512px/1f341.png")
