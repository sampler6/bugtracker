from fastapi import FastAPI, Depends
from fastapi_users import FastAPIUsers

from auth.auth import auth_backend, fastapi_users
from auth.schemas import UserRead, UserCreate
from tasks.router import router as router_task
from auth.router import router as router_users

app = FastAPI(
    Title="Bug Tracker"
)


app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(router_task)
app.include_router(router_users)
