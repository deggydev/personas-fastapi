from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import DeclarativeBase, Session

from app.config import (
    DB_DATABASE,
    DB_HOST,
    DB_PASSWORD,
    DB_PORT,
    DB_SSLMODE,
    DB_USERNAME,
)


class Base(DeclarativeBase):
    pass


engine = create_engine(
    URL.create(
        "postgresql+psycopg",
        username=DB_USERNAME,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        database=DB_DATABASE,
        query={"sslmode": DB_SSLMODE},
    ),
    pool_pre_ping=True,
    pool_size=3,
    max_overflow=2,
)


def get_db():
    with Session(engine) as db:
        yield db


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)
    yield
    engine.dispose()
