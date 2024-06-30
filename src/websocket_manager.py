from typing import List

from fastapi import APIRouter
from fastapi import WebSocket, WebSocketDisconnect

router = APIRouter()

# Список активных соединений WebSocket
active_websockets: List[WebSocket] = []


@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await websocket.accept()
    active_websockets.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Обработка данных от клиента, например, отправка сообщений другим клиентам
            # Или выполнение других операций на основе полученных данных
    except WebSocketDisconnect:
        active_websockets.remove(websocket)
        # Обработка закрытия соединения
