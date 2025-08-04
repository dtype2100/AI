from fastapi import APIRouter

# 분리된 라우터들을 import
from .routers import health, documents, query, system, models

# 메인 라우터 생성
router = APIRouter()

# 각 기능별 라우터를 메인 라우터에 포함
router.include_router(health.router, tags=["Health"])
router.include_router(documents.router, tags=["Documents"])
router.include_router(query.router, tags=["Query"])
router.include_router(system.router, tags=["System"])
router.include_router(models.router, tags=["Models"]) 