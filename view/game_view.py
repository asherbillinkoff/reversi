from abc import ABC, abstractmethod

class GameView(ABC):
    """     Abstract Class is responsible for preparing necessary information for users
    to interact with the game in the console.
    """

    def __init__(self, game) -> None:
        self.game = game

    @abstractmethod
    def display_greeting_message(self):
        pass

    @abstractmethod
    def get_game_mode(self):
        pass

    @abstractmethod
    def get_human_name(self):
        pass

    @abstractmethod
    def draw_board(self):
        pass

    @abstractmethod
    def display_winner(self, player):
        pass

    @abstractmethod
    def display_score(self, score):
        pass
