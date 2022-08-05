from re import X
from model.board import Board
import datetime
from model.player import Player

class Game:
    """ This class contains all the methods related to the game logic."""

    def __init__(self, board_size):
        """ Initializes the Game object by creating the board, setting the
        current player and intializing the valid move flag (is_valid).

            Args:
                board_size (int): Number is passed to the board object for
                initializing a board for the given size
        """
        self.curr_player = 1
        self.opponent = 2
        self.is_valid = False
        self.board = Board(board_size)

    def place_starting_pieces(self):
        self.board.mat[self.board.size // 2 - 1][self.board.size // 2 - 1] = self.curr_player.symbol
        self.board.mat[self.board.size // 2][self.board.size // 2] = self.curr_player.symbol
        self.board.mat[self.board.size // 2 - 1][self.board.size // 2] = self.opponent.symbol
        self.board.mat[self.board.size // 2][self.board.size // 2 - 1] = self.opponent.symbol

    def change_player(self):
        """ Method changes players after a turn and keeps track of who the
        opponent is."""

        self.curr_player, self.opponent = self.opponent, self.curr_player

    def sum_player_pts(self):
        """ Method keeps track of the by iterating over the game board and
        summing totals.
        
            Return: Tuple containing the score for Player X and Player 0.
        """
        player_1_pts = 0        # Player 1 is will always be the human player.
        player_2_pts = 0        # Player 2 will be either human or AI.

        # Iterates over the entire board matrix and returns the player point totals.
        for i in range(self.board.size):
            for j in range(self.board.size):
                if self.board.mat[i][j] == 1:
                    player_1_pts += 1
                elif self.board.mat[i][j] == 2:
                    player_2_pts += 1
                
                # Since values 2 and 3 will never be on the board at the same time
                # we can use the same player_2_pts variable in this statement.
                elif self.board.mat[i][j] == 3:
                    player_2_pts += 1
        return (player_1_pts, player_2_pts)

    def check_winner(self):
        """ Method checks for a winner by confirming if there are any remaining
        cells in the matrix with a zero value. If there are then the game has
        not yet concluded.
        """

        # TODO - figure out how to reference winner and loser
        for i in range(self.board.size):
            for j in range(self.board.size):
                if self.board.mat[i][j] == 0:
                    return False
                else:
                    pass
        score = self.sum_player_pts()
        check_human = isinstance(self.curr_player, Player)
        if score[0] > score[1]:
            if check_human:
                if self.curr_player.name == 'Player 2':
                    return self.opponent
            else:
                return self.curr_player
        if score[0] < score[1]:
            if check_human:
                if self.curr_player.name == 'Player 2':
                    return self.curr_player
            else:
                return self.opponent

    def record_winner(self, score, player):
        """ Records the time, date, winner and game score to a text file."""
        now = datetime.datetime.now()
        with open('winner_records.txt','a') as f:
            print(now, 'Winner:', player, score, file=f)





