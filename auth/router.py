from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import Field, EmailStr
from auth.auth import fastapi_users
from auth.schemas import UserRead
from models import User
from database import get_async_session
from enums.enums import Roles


router = APIRouter(
    prefix="/users",
    tags=['Users']
)

current_user = fastapi_users.current_user()


@router.get("/get_users", response_model=List[UserRead])
async def get_users(user: User = Depends(current_user),
                      session: AsyncSession = Depends(get_async_session)):
    if user.role != Roles.Manager:
        raise HTTPException(status_code=422, detail="you must have role 'manager'")

    query = select(User.__table__.c.id, User.__table__.c.email, User.__table__.c.role)
    result = await session.execute(query)
    return result.all()


@router.get("/get_user/{user_id}", response_model=UserRead)
async def get_user(user_id: int, user: User = Depends(current_user),
                      session: AsyncSession = Depends(get_async_session)):
    if user.role != Roles.Manager:
        raise HTTPException(status_code=422, detail="you must have role 'manager'")

    query = select(User.__table__.c.id, User.__table__.c.email, User.__table__.c.role)\
        .where(User.__table__.c.id == user_id)
    result = await session.execute(query)
    return result.one()


@router.patch("/change/role")
async def change_role(user_id: int, new_role: Roles, user: User = Depends(current_user),
                      session: AsyncSession = Depends(get_async_session)):
    if user.role != Roles.Manager:
        raise HTTPException(status_code=422, detail="you must have role 'manager'")
    try:
        query = update(User.__mapper__).values(role=new_role).where(User.__mapper__.c.id == user_id)
        await session.execute(query)
        await session.commit()
        return {"status": "success", "detail": "None"}
    except:
        return {"status": "error", "detail": "User with id does not exist"}


@router.patch("/change/email")
async def change_email(user_id: int, new_email: EmailStr, user: User = Depends(current_user),
                      session: AsyncSession = Depends(get_async_session)):
    if user.role != Roles.Manager:
        raise HTTPException(status_code=422, detail="you must have role 'manager'")
    try:

        query = update(User.__mapper__).values(email=new_email).where(User.__mapper__.c.id == user_id)
        await session.execute(query)
        await session.commit()
        return {"status": "success", "detail": "None"}
    except:
        return {"status": "error", "detail": "User with id does not exist"}
