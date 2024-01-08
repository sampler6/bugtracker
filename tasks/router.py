from fastapi import APIRouter, Depends, HTTPException
from tasks.delete import router as router_delete
from tasks.patch import router as router_patch
from tasks.post import router as router_post
from tasks.get import router as router_get

router = APIRouter(
    prefix="/task",
    tags=['Task']
)

router.include_router(router_get)
router.include_router(router_post)
router.include_router(router_patch)
router.include_router(router_delete)
