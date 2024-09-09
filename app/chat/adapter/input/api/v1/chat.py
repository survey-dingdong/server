from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, WebSocket

from app.chat.container import ChatContainer
from app.chat.domain.usecase.chat import ChatUseCase
from core.fastapi.dependencies.permission import IsAuthenticated, PermissionDependency

chat_router = APIRouter()


@chat_router.websocket(
    "/ws/{room_id}/{user_id}",
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
@inject
async def send_chat(
    websocket: WebSocket,
    room_id: int,
    user_id: int,
    usecase: ChatUseCase = Depends(Provide[ChatContainer.chat_service]),
):
    await usecase.send_chat(websocket=websocket, room_id=str(room_id), user_id=user_id)
