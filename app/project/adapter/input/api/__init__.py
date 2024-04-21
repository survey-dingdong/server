from fastapi import APIRouter

from app.project.adapter.input.api.v1.project import project_router as project_v1_router

router = APIRouter()
router.include_router(project_v1_router, prefix="/workspaces", tags=["Project"])

__all__ = ["router"]
