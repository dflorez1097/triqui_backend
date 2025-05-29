from abc import ABC, abstractmethod

class GameStrategy(ABC):
    @abstractmethod
    def is_valid_move(self, game, player_id, row, col):
        pass

    @abstractmethod
    def check_winner(self, game):
        pass

    @abstractmethod
    def check_draw(self, game):
        pass

