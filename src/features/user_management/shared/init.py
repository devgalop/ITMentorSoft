from fastapi import APIRouter

from src.features.user_management.create_user.create_user_endpoint import (
    router as create_user_router,
)
from src.features.user_management.login.login_endpoint import router as login_router
from src.features.user_management.get_user.get_user_endpoint import (
    router as get_user_router,
)
from src.features.user_management.recovery_password.recovery_password_endpoint import (
    router as recovery_password_router,
)
from src.features.user_management.change_password.change_password_endpoint import (
    router as change_password_router,
)
from src.features.user_management.assign_role.assign_role_endpoint import (
    router as assign_role_router,
)
from src.features.user_management.get_available_roles.get_available_roles_endpoint import (
    router as get_available_roles_router,
)

router = APIRouter()
router.include_router(create_user_router)
router.include_router(login_router)
router.include_router(get_available_roles_router)
router.include_router(get_user_router)
router.include_router(recovery_password_router)
router.include_router(change_password_router)
router.include_router(assign_role_router)
