from re import X
from model.players import Player
from model.board import Board
from datetime import datetime

class Game():
    """ This class contains all the methods related to the game logic."""

    def __init__(self, board_size):
        """ Initializes the Game object by creating the board, setting the
        current player and intializing the valid move flag (is_valid).

            Args:
                board_size (int): Number is passed to the board object for
                initializing a board for the given size
        """
        self.board = Board(board_size)
        self.curr_player = Player.X
        self.opponent = Player.O
        self.is_valid = False

    def change_player(self):
        """ Method changes players after a turn and keeps track of who the
        opponent is."""

        self.curr_player, self.opponent = self.opponent, self.curr_player


    def make_move(self, row, col):
        """ Method pass along a user move to the board to be updated."""
        self.board.update_cell(row, col, self.curr_player)

    def sum_player_pts(self):
        """ Method keeps track of the by iterating over the game board and
        summing totals.
        
            Return: Tuple containing the score for Player X and Player 0.
        """
        sum_X = 0
        sum_O = 0

        # Iterates over the entire board matrix and returns the player point totals.
        for i in range(self.board.size):
            for j in range(self.board.size):
                if self.board.mat[i][j] == 1:
                    sum_X += 1
                elif self.board.mat[i][j] == 2:
                    sum_O += 1
        return (sum_X, sum_O)

    def check_winner(self):
        """ Method checks for a winner by confirming if there are any remaining
        cells in the matrix with a zero value. If there are then the game has
        not yet concluded.

            Returns:
                self.curr_player:    (if the game has concluded)
                False:               (if the game has not concluded)
        """

        for i in range(self.board.size):
            for j in range(self.board.size):
                if self.board.mat[i][j] == 0:
                    return False
                else:
                    pass
        return self.curr_player

    def record_winner(self, score, player):
        """ Records the time, date, winner and game score to a text file."""
        now = datetime.datetime
        with open('winner_records.txt', 'w') as f:
            print(now, player, score, file=f)

    def is_valid_move(self, row, col, player):
        ''' Function determines if the user move is valid. If the
        three condition checks pass then the recursive function is called to
        flip opponent disks.'''
        directions = [(0,1), (0,-1), (1,0), (-1,0), (1,1), (1,-1), (-1,1), (-1,-1)]
        self.is_valid = False

        # 1. Check if the user move is within the board boundaries.
        if row > self.board.size or col > self.board.size:
            return self.is_valid

        # 2. Check if user move cell is empty.
        if self.board.get_cell(row, col) != 0:
            return self.is_valid

        # 3. Check if there are any neighbouring disks of the opponent. If True
        # recursive function is called.
        for direction in directions:
            check_cell = (row + direction[0], col + direction[1])
            if self.board.mat[check_cell[0]][check_cell[1]] == self.opponent:
                self._flip_disks(check_cell[0], check_cell[1], direction, player)

    def _flip_disks(self, row, col, direction, player):
        
        if self.board.get_cell(row, col) == player:
            self.board.update_board(row, col, direction, player)
            self.is_valid = True
            return

        elif self.board.get_cell(row, col) == self.opponent:
            row += direction[0]
            col += direction[1]
            self._flip_disks(row, col, direction, player)
