from fastapi import APIRouter

from api.v1.endpoints.auth import router as auth_router
from api.v1.endpoints.kitchen import router as kitchen_router

router = APIRouter()

router.include_router(auth_router)
router.include_router(kitchen_router)
