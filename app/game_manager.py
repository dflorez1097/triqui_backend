from .strategy import GameStrategy
from .tic_tac_toe_strategy import TicTacToeStrategy

class TicTacToeGame:
    def __init__(self, game_id: str, strategy: GameStrategy = None):
        self.game_id = game_id
        self.board = [[None for _ in range(3)] for _ in range(3)]
        self.players = {}
        self.current_turn = None
        self.winner = None
        self.draw = None
        self.winner_positions = []
        self.strategy = strategy if strategy else TicTacToeStrategy()  # Usa Strategy

    def add_player(self, player_id: str, symbol: str):
        if len(self.players) < 2:
            self.players[player_id] = symbol
            if self.current_turn is None:
                self.current_turn = symbol

    def make_move(self, player_id: str, row: int, col: int):
        if not self.strategy.is_valid_move(self, player_id, row, col):  # Valida con Strategy
            return False

        self.board[row][col] = self.players[player_id]

        if self.strategy.check_winner(self):  # Usa Strategy para detectar ganador
            self.winner = self.players[player_id]
        elif self.strategy.check_draw(self):  # Usa Strategy para detectar empate
            self.draw = True
        else:
            self.current_turn = next(self.players[player] for player in self.players.keys() if player != player_id)

        return True

