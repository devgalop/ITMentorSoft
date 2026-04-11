from fastapi import APIRouter

from src.features.user_management.create_user.create_user_endpoint import router as create_user_router
from src.features.user_management.login.login_endpoint import router as login_router

router = APIRouter()
router.include_router(create_user_router)
router.include_router(login_router)