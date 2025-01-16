from fastapi import APIRouter

from app.chat.adapter.input.api.v1.chat import chat_router as chat_v1_router

router = APIRouter()
router.include_router(chat_v1_router, tags=["Chat"])

__all__ = ["router"]
