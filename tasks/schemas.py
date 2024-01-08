from datetime import datetime
from typing import Optional

from pydantic import Field, BaseModel

import database
from enums.enums import TaskType, Status, Priority


class TaskCreate(BaseModel):
    type: TaskType
    priority: Optional[Priority] = None
    header: str
    description: Optional[str] = None
    executor: Optional[int] = Field(ge=0)
    creator: int = Field(ge=0)


class TaskRead(BaseModel):
    number: int
    type: TaskType
    priority: Optional[Priority] = None
    status: Status
    header: str
    description: Optional[str] = None
    executor: Optional[int] = Field(gt=0)
    creator: int = Field(gt=0)
    time_of_creation: datetime
    time_of_modification: datetime


class SubtaskCreate(BaseModel):
    main_task: int
    sub_task: int

