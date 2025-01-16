from fastapi import APIRouter

from app.websocket.adapter.input.api.v1.websocket import (
    websocket_router as websocket_v1_router,
)

router = APIRouter()
router.include_router(websocket_v1_router, tags=["Websocket"])

__all__ = ["router"]
