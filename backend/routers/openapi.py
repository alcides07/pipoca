from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi import APIRouter
from starlette.responses import RedirectResponse

router = APIRouter()


@router.get("/", include_in_schema=False)
async def redirect():
    response = RedirectResponse(url="/docs")
    return response


@router.get("/docs", include_in_schema=False)
def overridden_swagger():
    return get_swagger_ui_html(openapi_url="/openapi.json",
                               title="API PIPOCA",
                               swagger_favicon_url="https://cdn-icons-png.flaticon.com/512/1522/1522352.png")


@router.get("/redoc", include_in_schema=False)
def overridden_redoc():
    return get_redoc_html(openapi_url="/openapi.json",
                          title="API PIPOCA",
                          redoc_favicon_url="https://images.emojiterra.com/twitter/v14.0/512px/1f37f.png")
