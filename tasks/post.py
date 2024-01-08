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
from sqlalchemy.exc import NoResultFound, IntegrityError
from tasks.patch import validate_executor


current_user = fastapi_users.current_user()
router = APIRouter(
    prefix="/post",
)


@router.post("/new_task")
async def add_task(new_task: TaskCreate, user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)):
    try:
        new_task.type = new_task.type.value
        new_task.priority = new_task.priority.value

        await validate_executor(new_task.executor, Status.To_do.value, session)

        stmt = insert(Task.__mapper__).values(dict(new_task.model_dump()))
        await session.execute(stmt)
        await session.commit()
        return {"status": "success", "detail": "None"}
    except NoResultFound:
        raise HTTPException(status_code=422, detail="there is no task with such number")
    except IntegrityError:
        raise HTTPException(status_code=422, detail="there is no user with this id")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="None")


@router.post("/subtask")
async def add_subtask(new_subtask: SubtaskCreate, session: AsyncSession = Depends(get_async_session)):
    try:
        stmt = insert(Subtasks.__mapper__).values(new_subtask.model_dump())
        await session.execute(stmt)
        await session.commit()
        return {"status": "success", "detail": "None"}
    except IntegrityError:
        raise HTTPException(status_code=422, detail="there is no task with this number")
    except NoResultFound:
        raise HTTPException(status_code=422, detail="there is no task with such number")
    except Exception:
        raise HTTPException(status_code=422, detail="task with this number does not exist")