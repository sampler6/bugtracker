import asyncio
import pytest_asyncio as pytest
from fastapi import Depends
from typing import AsyncGenerator

from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from main import app
from models import Base
from config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_TEST_NAME
from database import get_async_session
from httpx import AsyncClient
from fastapi.testclient import TestClient

DATABASE_URL_TEST = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_TEST_NAME}"

engine_test = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)
async_session_maker = async_sessionmaker(engine_test, expire_on_commit=False)
Base.metadata.bind = engine_test


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


app.dependency_overrides[get_async_session] = override_get_async_session


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
