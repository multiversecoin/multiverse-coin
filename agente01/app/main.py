"""FastAPI application entry point."""

import logging

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import init_db
from app.core.security import hash_password
from app.api.routes import auth, users, operations, evidences, reports, audit, compliance

logging.basicConfig(
    level=logging.INFO if not settings.DEBUG else logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Starting {settings.APP_NAME} ({settings.APP_ENV})")
    await init_db()
    await _seed_admin_user()
    yield
    logger.info("Shutting down")


async def _seed_admin_user():
    from sqlalchemy import select
    from app.core.database import async_session_factory
    from app.models.user import User

    async with async_session_factory() as session:
        result = await session.execute(select(User).where(User.email == "admin@agente01.local"))
        if not result.scalar_one_or_none():
            admin = User(
                email="admin@agente01.local",
                password_hash=hash_password("admin123"),
                full_name="Administrador do Sistema",
                role="ADMIN",
            )
            session.add(admin)
            await session.commit()
            logger.info("Admin user seeded: admin@agente01.local / admin123")


app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="Sistema de geração automatizada de relatórios técnicos para operações subaquáticas.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.APP_ENV == "DEV" else [],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix=settings.API_PREFIX)
app.include_router(users.router, prefix=settings.API_PREFIX)
app.include_router(operations.router, prefix=settings.API_PREFIX)
app.include_router(evidences.router, prefix=settings.API_PREFIX)
app.include_router(reports.router, prefix=settings.API_PREFIX)
app.include_router(audit.router, prefix=settings.API_PREFIX)
app.include_router(compliance.router, prefix=settings.API_PREFIX)


@app.get("/health")
async def health():
    return {"status": "ok", "env": settings.APP_ENV}
