from typing import List, Optional
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete, func
from database import get_async_session
from enums.enums import TaskType, Roles, Status, StatusNext, next_status_dict, TaskFields, Priority
from tasks.schemas import TaskRead, TaskCreate, SubtaskCreate
from auth.auth import fastapi_users
from models import User, Task, Subtasks
from datetime import datetime
from sqlalchemy.exc import NoResultFound

current_user = fastapi_users.current_user()

router = APIRouter(
    prefix="/delete",
)


@router.delete("/{task_number}")
async def delete_task(task_number: int, user: User = Depends(current_user),
                      session: AsyncSession = Depends(get_async_session)):
    if user.role != Roles.Manager:
        raise HTTPException(status_code=422, detail="you must have role 'manager'")

    stmt = delete(Task.__mapper__).where(Task.__table__.c.number == task_number)
    await session.execute(stmt)
    await session.commit()
