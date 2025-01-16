from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, WebSocket
from fastapi.responses import HTMLResponse

from app.websocket.container import WebsocketContainer
from app.websocket.domain.usecase.websocket import WebsocketUseCase

websocket_router = APIRouter()


html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <label>Room ID: <input type="text" id="roomId" autocomplete="off" value="foo"/></label>
            <label>User ID: <input type="text" id="userId" autocomplete="off" value="foo"/></label>
            <button onclick="connect(event)">Connect</button>
            <hr>
            <label>Message: <input type="text" id="messageText" autocomplete="off"/></label>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
        var ws = null;
            function connect(event) {
                var roomId = document.getElementById("roomId")
                var userId = document.getElementById("userId")
                ws = new WebSocket("ws://localhost:8000/ws/" + roomId.value + "/" + userId.value);
                ws.onmessage = function(event) {
                    var messages = document.getElementById('messages')
                    var message = document.createElement('li')
                    var content = document.createTextNode(event.data)
                    message.appendChild(content)
                    messages.appendChild(message)
                };
                event.preventDefault()
            }
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@websocket_router.get("/")
async def get():
    return HTMLResponse(html)


@websocket_router.websocket(
    "/ws/{room_id}/{user_id}",
    # dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
@inject
async def send_chat(
    websocket: WebSocket,
    room_id: int,
    user_id: int,
    usecase: WebsocketUseCase = Depends(Provide[WebsocketContainer.chat_service]),
):
    await usecase.send_chat(websocket=websocket, room_id=str(room_id), user_id=user_id)
