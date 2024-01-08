from fastapi_users import schemas
from pydantic import EmailStr, Field, BaseModel

from enums.enums import Roles, TaskType, Status, Priority


class UserRead(schemas.BaseUser):
    id: int
    email: EmailStr
    role: Roles


class UserCreate(schemas.BaseUserCreate):
    email: EmailStr
    role: Roles
    password: str

