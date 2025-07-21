from fastapi import APIRouter
from .endpoints import (
    v1_router,
    service_router,
    main_router,
    user_router
)

router = APIRouter()

router.include_router(main_router)
router.include_router(v1_router, prefix="/v1")
router.include_router(service_router, prefix="/service")
router.include_router(user_router, prefix="/user")