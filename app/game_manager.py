import uuid

class TicTacToeGame:
    def __init__(self, game_id: str):
        self.game_id = game_id
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.players = {}
        self.current_turn = None
        self.winner = None

    def add_player(self, player_id: str, symbol: str):
        if len(self.players) < 2:
            self.players[player_id] = symbol
            if self.current_turn is None:
                self.current_turn = player_id

    def is_valid_move(self, player_id: str, row: int, col: int) -> bool:
        return (
            0 <= row < 3 and 0 <= col < 3 and
            self.board[row][col] == "" and
            self.current_turn == player_id
        )

    def make_move(self, player_id: str, row: int, col: int):
        if self.is_valid_move(player_id, row, col):
            self.board[row][col] = self.players[player_id]
            if self.check_winner():
                self.winner = player_id
            else:
                self.current_turn = next(player for player in self.players if player != player_id)
            return True
        return False

    def check_winner(self):
        winning_patterns = [
            [(0, 0), (0, 1), (0, 2)], [(1, 0), (1, 1), (1, 2)], [(2, 0), (2, 1), (2, 2)], 
            [(0, 0), (1, 0), (2, 0)], [(0, 1), (1, 1), (2, 1)], [(0, 2), (1, 2), (2, 2)], 
            [(0, 0), (1, 1), (2, 2)], [(0, 2), (1, 1), (2, 0)]
        ]
        for pattern in winning_patterns:
            symbols = [self.board[row][col] for row, col in pattern]
            if symbols[0] and symbols.count(symbols[0]) == 3:
                return True
        return False

class GameManager:
    def __init__(self):
        self.games = {}

    def create_game(self):
        game_id = str(uuid.uuid4())
        self.games[game_id] = TicTacToeGame(game_id)
        return game_id

    def get_game(self, game_id):
        return self.games.get(game_id)

    def remove_game(self, game_id):
        if game_id in self.games:
            del self.games[game_id]

