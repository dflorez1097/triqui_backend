from .strategy import GameStrategy

class TicTacToeStrategy(GameStrategy):
    def is_valid_move(self, game, player_id, row, col):
        return (
            0 <= row < 3 and 0 <= col < 3 and
            game.board[row][col] is None and
            game.current_turn == game.players[player_id]
        )

    def check_winner(self, game):
        winning_patterns = [
            [(0, 0), (0, 1), (0, 2)], [(1, 0), (1, 1), (1, 2)], [(2, 0), (2, 1), (2, 2)],  
            [(0, 0), (1, 0), (2, 0)], [(0, 1), (1, 1), (2, 1)], [(0, 2), (1, 2), (2, 2)],  
            [(0, 0), (1, 1), (2, 2)], [(0, 2), (1, 1), (2, 0)]  
        ]

        for pattern in winning_patterns:
            symbols = [game.board[row][col] for row, col in pattern]
            if symbols[0] and all(symbol == symbols[0] for symbol in symbols):
                game.winner_positions = pattern
                return symbols[0]

        return None

    def check_draw(self, game):
        return all(cell is not None for row in game.board for cell in row)

