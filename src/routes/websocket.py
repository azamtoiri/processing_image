from fastapi import APIRouter, WebSocket
from starlette.websockets import WebSocketDisconnect

from src.websocket_manager import websocket_endpoint

router = APIRouter()


# WebSocket для оповещений
@router.websocket("/ws/{project_id}")
async def websocket_endpoint(websocket: WebSocket, project_id: int):
    await websocket_endpoint.connect(websocket, project_id)
    try:
        while True:
            # Веб-сокет соединение может слушать изменения статусов изображений
            # и отправлять их клиентам
            await websocket.receive_text()
    except WebSocketDisconnect:
        websocket_endpoint.active_connections.pop(project_id, None)
