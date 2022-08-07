from model.board import Board
from model.game_logic import GameLogic
from model.player import Player

class AIPlayer(Player):
    def __init__(self, name='AI', colour='White'):
        super().__init__(name, colour)
        self.name = name
        self.symbol = 3
        self.valid_moves = []
