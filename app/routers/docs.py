from fastapi import APIRouter, Depends
from fastapi.openapi.docs import get_redoc_html
from core.docs_security import basic_http_credentials


router = APIRouter(dependencies=[Depends(basic_http_credentials)])


@router.get("/docs", include_in_schema=False)
async def get_redoc_documentation():
    return get_redoc_html(
        openapi_url="/openapi.json",
        title="FastAPI | Documentation",
        # redoc_favicon_url="https://YOUR_WEBSITE/favicon.ico",
    )
