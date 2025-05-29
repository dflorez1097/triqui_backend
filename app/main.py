from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .ws_manager import WebSocketManager
import json
from logging import getLogger

log = getLogger("main")

app = FastAPI()
ws_manager = WebSocketManager()
games = []
 
origins = [
    "http://localhost:5173",
    "http://localhost:3000", 
    "(http://172.18.0.1:51646)",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GameResponse(BaseModel):
    message: str
    game_waiting: str


@app.websocket("/{game_id}/{player_id}")
async def websocket_endpoint(websocket: WebSocket, game_id: int, player_id: str):
    await ws_manager.connect(websocket, game_id, player_id)  
    try:
        while True:
            data = await websocket.receive_json()
            await ws_manager.receive_message(player_id, data) 
    except Exception as e:
        log.error(f"Error in webhook: {e}")
        await ws_manager.disconnect(player_id, game_id)
        await websocket.close()


@app.get("/game_waiting")
async def game_waiting() -> GameResponse:
    games = ws_manager.game_manager.games

    if not games:
        return GameResponse(message="No games found", game_waiting='')
    
    game_waiting = None

    for game in games.values():
        if len(game.players) < 2:
            game_waiting = game
            break
    
    if not game_waiting:
        return GameResponse(message="Games not found", game_waiting='')
    
    game_id = str(game_waiting.game_id)
    return GameResponse(
        message="Game found sucessfully",
        game_waiting=game_id
    )