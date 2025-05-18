from fastapi import WebSocket
from app.game_manager import GameManager

class WebSocketManager:
    def __init__(self):
        self.connections = {}  # Almacena conexiones activas
        self.game_manager = GameManager()

    async def connect(self, websocket: WebSocket, game_id: str, player_id: str):
        await websocket.accept()
        self.connections[player_id] = websocket

        game = self.game_manager.get_game(game_id)
        if not game:
            game_id = self.game_manager.create_game()
            game = self.game_manager.get_game(game_id)

        symbol = "X" if len(game.players) == 0 else "O"
        game.add_player(player_id, symbol)

        await self.broadcast_game_state(game_id)

    async def disconnect(self, player_id: str, game_id: str):
        if player_id in self.connections:
            del self.connections[player_id]

        game = self.game_manager.get_game(game_id)
        if game:
            await self.notify_player_disconnection(game_id, player_id)

    async def notify_player_disconnection(self, game_id: str, player_id: str):
        message = {"type": "disconnect", "message": f"Jugador {player_id} ha salido."}
        for player, ws in self.connections.items():
            if player != player_id:
                await ws.send_json(message)

    async def receive_message(self, player_id: str, message: dict):
        game_id = message.get("game_id")
        row, col = message.get("position", (None, None))

        if game_id and self.game_manager.get_game(game_id):
            game = self.game_manager.get_game(game_id)
            if game.make_move(player_id, row, col):
                await self.broadcast_game_state(game_id)

    async def broadcast_game_state(self, game_id: str):
        game = self.game_manager.get_game(game_id)
        if game:
            game_state = {
                "board": game.board,
                "current_turn": game.current_turn,
                "winner": game.winner
            }
            for player_id, websocket in self.connections.items():
                await websocket.send_json(game_state)

