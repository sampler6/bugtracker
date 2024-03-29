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
from sqlalchemy.exc import NoResultFound, NoForeignKeysError

current_user = fastapi_users.current_user()

router = APIRouter(
    prefix="/patch",
)


async def validate_executor(executor_id: int, task_status: Status,
                      session: AsyncSession = Depends(AsyncSession)):
    """Used for validation executor role + task status fields"""

    if executor_id is not None:
        query = select(User.__table__.c.role).where(User.__table__.c.id == executor_id)
        result = await session.execute(query)
        executor_role: Optional[Roles] = result.one()[0]
    else:
        executor_role = None

    if task_status == Status.To_do and executor_role is None:
        raise HTTPException(status_code=422, detail="task with status 'In progress' must have the executor'")
    if executor_role == Roles.Manager:
        raise HTTPException(status_code=422, detail="Manager can't be the executor")
    if task_status in [Status.To_do, Status.In_progress, Status.Code_review] and executor_role == Roles.QA:
        raise HTTPException(status_code=422, detail=f"QA can't be the executor of task with status"
                                                    f" {next_status_dict[task_status].value}")
    if task_status in [Status.Dev_test] and executor_role == Roles.Developer:
        raise HTTPException(status_code=422, detail=f"Developer can't be the executor of task with status"
                                                    f" {next_status_dict[task_status].value}")


@router.patch("/task_status")
async def change_task_status(task_number: int, status: StatusNext, executor: int = None,
                             user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(Task.__table__).where(Task.__table__.c.number == task_number)
        result = await session.execute(query)
        task: TaskRead = result.one()

        if status == StatusNext.Next:
            await validate_executor(executor, task.status, session)

        if status == StatusNext.To_do:
            stmt = update(Task.__mapper__).values(status="To do", executor=executor,
                                                  time_of_modification=datetime.utcnow())\
                .where(Task.__table__.c.number == task_number)
        elif status == StatusNext.Wontfix:
            stmt = update(Task.__mapper__).values(status=status.Wontfix,
                                                  executor=executor, time_of_modification=datetime.utcnow())\
                .where(Task.__table__.c.number == task_number)
        else:
            nxtstatus = next_status_dict[task.status]
            stmt = update(Task.__mapper__).values(status=nxtstatus, executor=executor,
                                                  time_of_modification=datetime.utcnow())\
                .where(Task.__table__.c.number == task_number)

        await session.execute(stmt)
        await session.commit()
        return {"status": "success", "detail": "None"}
    except NoResultFound:
        raise HTTPException(status_code=422, detail="there is no task with such number")
    except HTTPException as e:
        raise e


@router.patch("/task_column")
async def change_task_column(task_number: int, task_field: TaskFields, new_value, user: User = Depends(current_user),
                             session: AsyncSession = Depends(get_async_session)):
    try:
        if task_field in [TaskFields.executor, TaskFields.creator]:
            new_value: int = int(new_value)
            query = select(Task.__table__.c.status).where(Task.__table__.c.number == task_number)
            result = await session.execute(query)
            status: Status = result.one()

            if task_field.executor:
                await validate_executor(new_value, status)
        elif task_field in [TaskFields.header, TaskFields.description]:
            new_value: str = str(new_value)
        elif task_field in [TaskFields.status]:
            new_value: Status = Status(new_value)
        elif task_field in [TaskFields.type]:
            new_value: TaskType = TaskType(new_value)
        elif task_field in [TaskFields.priority]:
            new_value: Priority = Priority(new_value)

        stmt = eval(f"update(Task.__mapper__).values({task_field.value}=new_value, time_of_modification=datetime.utcnow()).\
        where(Task.__table__.c.number == task_number)")
        await session.execute(stmt)
        await session.commit()

        return {"status": "success", "detail": "None"}
    except ValueError:
        raise HTTPException(status_code=422, detail="new value don't match to task field")
    except NoResultFound:
        raise HTTPException(status_code=422, detail="there is no task with such number")
    except HTTPException as e:
        raise e
