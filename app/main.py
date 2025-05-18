from fastapi import FastAPI, WebSocket
from app.ws_manager import WebSocketManager

app = FastAPI()
ws_manager = WebSocketManager()

@app.websocket("/ws/{game_id}/{player_id}")
async def websocket_endpoint(websocket: WebSocket, game_id: str, player_id: str):
    await ws_manager.connect(websocket, game_id, player_id)
    try:
        while True:
            data = await websocket.receive_json()
            await ws_manager.receive_message(player_id, data)
    except:
        await ws_manager.disconnect(player_id, game_id)

