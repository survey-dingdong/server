from fastapi import APIRouter

from app.workspace.adapter.input.api.v1.workspace import (
    workspace_router as workspace_v1_router,
)

router = APIRouter()
router.include_router(
    workspace_v1_router, prefix="/api/v1/workspaces", tags=["Workspace"]
)

__all__ = ["router"]
