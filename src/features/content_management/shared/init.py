from fastapi import APIRouter

from src.features.content_management.register_content.register_content_endpoint import (
    router as register_content_router,
)
from src.features.content_management.rate_content.rate_content_endpoint import (
    router as rate_content_router,
)

router = APIRouter()
router.include_router(register_content_router)
router.include_router(rate_content_router)
