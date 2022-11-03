from fastapi import FastAPI, Depends
from fastapi.openapi.utils import get_openapi
from starlette.middleware.cors import CORSMiddleware

from supertokens_python.framework.fastapi import get_middleware
from supertokens_python import get_all_cors_headers

from core.supertokens import init_supertokens
from core.config import settings
from core.docs_security import basic_http_credentials

from routers import docs


description = """
FastAPI template project 🚀
"""


app = FastAPI(
    title=settings.PROJECT_NAME,
    description=description,
    version="v0.0.1",
    contact={
        "name": "Jorilla Abdullaev",
        "url": "https://jorilla.t.me",
        "email": "jorilla.abdullaev@protonmail.com",
    },
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)

if settings.SUPERTOKENS_CONNECTION_URI is not None:
    init_supertokens(settings.PROJECT_NAME)
    app.add_middleware(get_middleware())


# include routes here
app.include_router(docs.router)


@app.get("/openapi.json", include_in_schema=False)
async def openapi(_: str = Depends(basic_http_credentials)):
    schema = get_openapi(
        title=app.title,
        description=app.description,
        version=app.version,
        contact=app.contact,
        routes=app.routes,
    )
    # schema["info"]["x-logo"] = {
    #     "url": "https://YOUR_WEBSITE/logo.svg",
    #     "href": "https://YOUR_WEBSITE/",
    #     "backgroundColor": "#fff",
    #     "altText": "YOUR BRAND NAME",
    # }
    return schema


@app.get("/ping")
async def ping() -> str:
    return "pong"


if settings.SUPERTOKENS_CONNECTION_URI is not None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "PUT", "POST", "DELETE", "OPTIONS", "PATCH"],
        allow_headers=["Content-Type", "Accept-Language"] + get_all_cors_headers(),
    )
