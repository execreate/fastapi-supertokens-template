from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from supertokens_python.framework.fastapi import get_middleware
from supertokens_python import get_all_cors_headers

from core.supertokens import init_supertokens
from core.config import settings


description = """
First beta of MedHub Laboratory API 🚀
This API is intended for Medical Laboratory Systems that are willing to integrate with MedHub Medical System.
"""


app = FastAPI(
    title=settings.PROJECT_NAME,
    description=description,
    version="v0.0.1",
    contact={
        "name": "Jorilla Abdullaev",
        "url": "https://jorilla.t.me",
        "email": "jorilla.abdullaev@medhub.uz",
    },
    docs_url=None,
    redoc_url="/docs",
)

if settings.SUPERTOKENS_CONNECTION_URI is not None:
    init_supertokens(settings.PROJECT_NAME)
    app.add_middleware(get_middleware())


# include routes here
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
