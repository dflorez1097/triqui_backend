from fastapi import WebSocket
from .game_manager import GameManager, TicTacToeGame
from logging import getLogger

log = getLogger("ws_manager")

class WebSocketManager:
    game_manager = GameManager()

    def __init__(self):
        self.connections = {}
        self.connection_by_player = {}  # Almacena conexiones activas

    async def connect(self, websocket: WebSocket, game_id: int, player_id: str):
        await websocket.accept()
        game = self.game_manager.get_game(game_id)
        if not game:
            self.game_manager.create_game(game_id) 
            game = self.game_manager.get_game(game_id)

        connections: list = self.connections.get(game_id, [])
        connections.append(websocket)
        self.connections[game_id] = connections
        self.connection_by_player[player_id] = websocket
        symbol = "X" if len(game.players) == 0 else "O"
        game.add_player(player_id, symbol)
        await self.send_start_event(game, symbol, player_id)

    async def send_event(self, game, event_type, turn, connections):
        message = {
            "type": event_type,
            "turn": turn,
            "game_id": game.game_id,
            "board": game.board
        }
        for ws in connections:
            try:
                await ws.send_json(message)
            except Exception as e:
                    log.error(f"Error sending message: {e}")

    async def send_start_event(self, game, symbol, player_id):
        await self.send_event(game, "init", symbol, [self.connection_by_player[player_id]])
        if len(game.players) == 2:
            await self.send_event(game, "start", game.current_turn, self.connections[game.game_id])
            
    async def disconnect(self, player_id: str, game_id: str):
        if player_id in self.connections:
            del self.connections[player_id]

        game = self.game_manager.get_game(game_id)
        if game:
            player_to_notify = ""
            for player in game.players.keys():
                if player_id != player:
                    player_to_notify = player

            await self.notify_player_disconnection(game, player_to_notify)

    async def notify_player_disconnection(self, game: TicTacToeGame, player_id: str):
        message = {
            "type": "disconnect", 
            "message": f"Jugador {player_id} ha salido.", 
            "board": game.board,
            "game_id": game.game_id
        }

        for connect_game_id, list_ws in self.connections.items():
            if connect_game_id != game.game_id:
                continue

            for ws in list_ws:
                try:
                    await ws.send_json(message)
                except Exception as e:
                    log.error(f"Error sending message: {e}")

    async def receive_message(self, player_id: str, message: dict):
        game_id = message.get("game_id")
        row, col = message.get("position", (None, None))

        if game_id and (game := self.game_manager.get_game(game_id)):
            if (message.get("type", "") == "reset"):
                await self.restart(game, player_id)
                return
            
            if game.make_move(player_id, row, col):
                await self.broadcast_game_state(game_id)

    async def restart(self, game, player_id):
        game.restart(player_id)

        restart_event =  {
            "board": game.board,
            "turn": game.current_turn,
            "game_id": game.game_id,
            "type": "reset",
        }
        
        for connect_game_id, list_ws in self.connections.items():
            if game.game_id != connect_game_id:
                continue

            for websocket in list_ws:
                try:
                    await websocket.send_json(restart_event)
                except Exception as e:
                    log.error(f"Error sending message: {e}")

    async def broadcast_game_state(self, game_id: str):
        game = self.game_manager.get_game(game_id)
        event_type = ""
        if not game.winner and not game.draw:
            event_type = "update"
        elif game.draw:
            event_type = "draw"
        else:
            event_type = "win"

        log.critical(f"game: {game}")
        if not game:
            return
        
        game_state = {
            "board": game.board,
            "turn": game.current_turn,
            "winner": game.winner,
            "game_id": game_id,
            "type": event_type,
            "positions": game.winner_positions,
        }
        
        for connect_game_id, list_ws in self.connections.items():
            if game_id != connect_game_id:
                continue

            for websocket in list_ws:
                try:
                    await websocket.send_json(game_state)
                except Exception as e:
                    log.error(f"Error sending message: {e}")

