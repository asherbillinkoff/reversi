from re import X
from model.players import Player
from model.board import Board
import datetime

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
        score = self.sum_player_pts()
        if score[0] > score[1]:
            return Player.X
        if score[0] < score[1]:
            return Player.O

    def record_winner(self, score, player):
        """ Records the time, date, winner and game score to a text file."""
        now = datetime.datetime.now()
        with open('winner_records.txt', 'w') as f:
            print(now, player, score,'\n', file=f)

    def is_valid_move(self, row, col, player):
        ''' Function determines if the user move is valid. If the
        three condition checks pass then the recursive function is called to
        flip opponent disks.'''

         # Create a list of all directions in which a valid move exists.
        true_directions = []
        self.is_valid = False
        
        # Valid move condition #1: the cell is empty.
        if self.board.get_cell(row, col) == 0:
            directions = [(0,1), (0,-1), (1,0), (-1,0), (1,1), (1,-1), (-1,1), (-1,-1)]
            cell = (row, col)
            for direction in directions:
                check_cell = (row + direction[0], col + direction[1])

                # Check to make sure the index is in range of our board.
                if max(check_cell) >= self.board.size or min(check_cell) < 0:
                    continue

                # Valid move condition #2: there is an adjacent cell with the other player's disk.
                if self.board.mat[check_cell[0]][check_cell[1]] == self.opponent:

                    # Increment the current cell in that direction.
                    cell = (cell[0] + direction[0], cell[1] + direction[1])
                    if max(cell) >= self.board.size or min(cell) < 0:
                        continue

                    # Valid move condition #3: the given direction contains another one of current player's
                    # disks further down the row (i.e. there is a valid disk sandwich).
                    next_cell = cell
                    while self.board.mat[next_cell[0]][next_cell[1]] == self.opponent:
                        next_cell = (next_cell[0] + direction[0], next_cell[1] + direction[1])
                        # Make sure that the incremented cell is still within board range.
                        if max(next_cell) >= self.board.size or min(next_cell) < 0:
                            self.is_valid = False
                            break
                        # If incremented cell is = player then move is valid.
                        elif self.board.mat[next_cell[0]][next_cell[1]] == player:
                            self.is_valid = True
                            break
                            
                    # When code reaches the end of the disk sandwich, it appends that direction to a list
                    if self.is_valid:
                        true_directions.append(direction)    
                cell = (row, col)
                self.is_valid = False
        else:
            return

        # Need to confirm if any valid directions exist for placing a disk    
        if true_directions != []:
            self.board.update_board(row, col, true_directions, player)
            self.is_valid = True
        return





