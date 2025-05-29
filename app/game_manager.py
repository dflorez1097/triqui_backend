import uuid
from logging import getLogger

log = getLogger("Game manager")

class TicTacToeGame:
    def __init__(self, game_id: str):
        self.game_id = game_id
        self.board = [[None for _ in range(3)] for _ in range(3)]
        self.players = {}
        self.current_turn = None
        self.winner = None
        self.draw = None
        self.winner_positions = []

    def add_player(self, player_id: str, symbol: str):
        if len(self.players) < 2:
            self.players[player_id] = symbol
            if self.current_turn is None:
                self.current_turn = symbol

    def is_valid_move(self, player_id: str, row: int, col: int) -> bool:
        return (
            0 <= row < 3 and 0 <= col < 3 and
            self.board[row][col] == None and
            self.current_turn == self.players[player_id]
        )

    def make_move(self, player_id: str, row: int, col: int):
        if not self.is_valid_move(player_id, row, col):
            return False
        
        self.board[row][col] = self.players[player_id]

        if self.check_winner():
            self.winner = self.players[player_id]
        elif self.check_draw():
            self.draw = True
        else:
            self.current_turn = next(self.players[player] for player in self.players.keys() if player != player_id)

        return True

    def check_draw(self):
        for row in self.board:
            if None in row:
                return False

        return True

    def check_winner(self):
        winning_patterns = [
            [(0, 0), (0, 1), (0, 2)],  # filas
            [(1, 0), (1, 1), (1, 2)],
            [(2, 0), (2, 1), (2, 2)],
            [(0, 0), (1, 0), (2, 0)],  # columnas
            [(0, 1), (1, 1), (2, 1)],
            [(0, 2), (1, 2), (2, 2)],
            [(0, 0), (1, 1), (2, 2)],  # diagonal principal
            [(0, 2), (1, 1), (2, 0)]   # diagonal inversa
        ]
        
        for pattern in winning_patterns:
            symbols = [self.board[row][col] for row, col in pattern]
            if symbols[0] != '' and all(symbol == symbols[0] for symbol in symbols):
                self.winner_positions = pattern
                return symbols[0]  # Retorna 'X' o 'O'

        return None  # No hay ganador

    def restart(self, player_id):
        self.board = [[None for _ in range(3)] for _ in range(3)]
        self.current_turn = next(self.players[player] for player in self.players.keys() if player != player_id)
        self.draw = None
        self.winner = None
        self.winner_positions = []

class GameManager:
    def __init__(self):
        self.games = {}

    def create_game(self, game_id):
        self.games[game_id] = TicTacToeGame(game_id)
        log.critical(self.games)

    def get_game(self, game_id):
        return self.games.get(game_id)

    def remove_game(self, game_id):
        if game_id in self.games:
            del self.games[game_id]

