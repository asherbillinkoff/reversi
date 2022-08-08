from model.player import Player

class AIPlayer(Player):
    """    Class for the AI player.
    """
    def __init__(self, name='AI', colour='White'):
        super().__init__(name, colour)
        self.name = name
        self.symbol = 3
        self.valid_moves = []
