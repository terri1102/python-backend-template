from typing import Dict, AsyncGenerator
from contextlib import asynccontextmanager
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session

from app.core.config import settings
from app.core.db import create_tables, init_db, engine
from app.api.v1.router import api_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    create_tables()
    with Session(engine) as session:
        init_db(session)
    yield


app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.get("/health", tags=["healthcheck"], status_code=status.HTTP_200_OK)
async def health() -> Dict[str, str]:
    return {"status": "OK"}


app.include_router(api_router, prefix=settings.API_VER_STR)
