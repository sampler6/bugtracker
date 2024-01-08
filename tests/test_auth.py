import pytest_asyncio
import pytest
import pytest_order
from fastapi import Depends
from httpx import AsyncClient
from enums.enums import Roles
from conftest import engine_test


@pytest.mark.order(1)
async def test_register(ac: AsyncClient):
    response = await ac.post("/auth/register", json={
        "email": "user_Manager@example.com",
        "password": "pass",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "role": Roles.Manager.value
    })

    assert response.status_code == 201

    response = await ac.post("/auth/register", json={
        "email": "user_Developer@example.com",
        "password": "pass",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "role": Roles.Developer.value
    })

    assert response.status_code == 201

    response = await ac.post("/auth/register", json={
        "email": "user_Team_Lead@example.com",
        "password": "pass",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "role": Roles.Team_lead.value
    })

    assert response.status_code == 201

    response = await ac.post("/auth/register", json={
        "email": "user_QA@example.com",
        "password": "pass",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "role": Roles.QA.value
    })

    assert response.status_code == 201


async def test_register_with_bad_input(ac: AsyncClient):
    response = await ac.post("/auth/register", json={
        "email": "user@example.com",
        "password": "pass",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "role": "NotExistingRole"
    })

    assert response.status_code == 422

    response = await ac.post("/auth/register", json={
        "email": "user_Manager@example.com",
        "password": "pass",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "role": "Manager"
    })

    assert response.status_code == 400


@pytest.mark.order(2)
async def test_auth(ac: AsyncClient):
    response = await ac.post("/auth/jwt/login", data={'username': "user_Manager@example.com", "password": "pass"})

    assert response.status_code == 204
