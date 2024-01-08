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
    prefix="/get",
)


@router.get('/tasks', response_model=List[TaskRead])
async def get_all_tasks(user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(Task.__table__)
        print(query)
        result = await session.execute(query)
        return list(result.all())
    except:
        raise HTTPException(status_code=500, detail="None")


@router.get('/task', response_model=Optional[TaskRead])
async def get_task(task_number: Optional[int] = None, header: Optional[str] = None, description: Optional[str] = None,
                   user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)):
    if task_number is None and header is None and description is None:
        raise HTTPException(status_code=422, detail="One of the fields must be filled")
    try:
        if task_number is not None:
            query = select(Task.__table__).where(Task.__table__.c.number == task_number)
        elif header is not None:
            query = select(Task.__table__,
                           func.similarity(Task.__table__.c.header, header)
                           ).where(
                                Task.__table__.c.header.bool_op('%')(header),
                            ).order_by(
                                func.similarity(Task.__table__.c.header, header).desc(),
                                Task.__table__.c.time_of_modification.desc()
                            )
        else:
            query = select(Task.__table__,
                           func.similarity(Task.__table__.c.description, description)
                           ).where(
                Task.__table__.c.description.bool_op('%')(description),
            ).order_by(
                func.similarity(Task.__table__.c.description, description).desc(),
                Task.__table__.c.time_of_modification.desc()
            )

        result = await session.execute(query)
        return result.first()
    except NoResultFound:
        return None
    except Exception as e:
        raise e
        raise HTTPException(status_code=500, detail="None")


@router.get("/subtasks/{task_number}", response_model=List[int])
async def get_subtasks(task_number: int, user: User = Depends(current_user),
                       session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(Subtasks.__table__.c.sub_task).where(Subtasks.__table__.c.main_task == task_number)
        result = await session.execute(query)
        return list(x[0] for x in result.all())
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="None")
