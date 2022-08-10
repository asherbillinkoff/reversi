import datetime

from model.player import Player
from model.human_player import HumanPlayer
from model.board import Board
from model.game_logic import GameLogic

class Game:
    """     This class contains all the methods related to the game logic.
    """
    
    def __init__(self, board: Board, logic: GameLogic, players):
        """     Initializes the board and logic objects, setting the
        current players and intializing the valid move flag to False (is_valid).
        """
        self.board = board
        self.logic = logic
        self.curr_player = players[0]
        self.opponent = players[1]
        self.player1 = players[0]
        self.player2 = players[1]
        self.is_valid = False

    def change_player(self):
        """     Method changes current and opposing players after each turn.
        """

        self.curr_player, self.opponent = self.opponent, self.curr_player

    def check_winner(self, skipped_turns):
        """     Method checks for a winner by confirming if there are any remaining
        cells in the matrix with a zero value. If there are then the game has
        not yet concluded.
        """
        if skipped_turns > 1:
            pass
        else:
            for i in range(self.board.size):
                for j in range(self.board.size):
                    if self.board.mat[i][j] == 0:
                        return False
                    else:
                        pass
        score = self.logic.sum_player_pts(self.board)
        # If the player is human and symbol 2 then they must be the opponent.
        check_human = isinstance(self.curr_player, HumanPlayer)
        if score[0] > score[1]:
            if check_human:
                if self.curr_player.symbol == 2:
                    return self.opponent.name
            else:
                return self.curr_player

        # If the player is human and symbol 2 then they must be the current player.        
        if score[0] < score[1]:
            if check_human:
                if self.curr_player.symbol == 2:
                    return self.curr_player
            else:
                return self.opponent

    def record_winner(self, score, player: Player):
        """     Records the time, date, winner and game score to a text file.
        """
        
        now = datetime.datetime.now()
        with open('winner_records.txt','a') as f:
            print(now, 'Winner:', player.name, score, file=f)





