from re import X
from model.players import Player
from model.board import Board
from datetime import datetime

class Game():
    """ This class contains all the methods related to the game logic."""

    def __init__(self, board_size):
        """ Initializes the Game object by creating the board, setting the current player
        and intializing the valid move flag (is_valid).

            Args:
                board_size (int): Number is passed to the board object for initializing a board
                for the given size
        """
        self.board = Board(board_size)
        self.curr_player = Player.X
        self.opponent = Player.O
        self.is_valid = False

    def change_player(self):
        """ Method changes players after a turn and keeps track of who the opponent is."""
        self.curr_player, self.opponent = self.opponent, self.curr_player


    def make_move(self, row, col):
        """ Method pass along a user move to the board to be updated."""
        self.board.update_cell(row, col, self.curr_player)

    def sum_player_pts(self):
        """ Method keeps track of the by iterating over the game board and summing totals.
        
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
        """ Method checks for a winner by confirming if there are any remaining cells in the
        matrix with a zero value. If there are then the game has not yet concluded.

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
        """ This method performs three main checks to confirm if a user move is valid.
        It iterates over all possible directions for disk validity and appends the valid
        directions to a list. This list is then passed to another class to update the
        status of the board after the move.

            Args:
                row (int): Cell value for a given row.
                col (int): Cell value for a given column.
                player (int enum): Player responsible for the current move.

            Returns:

        """
        
        # Create a list of all directions in which a valid move exists.
        true_directions = []
        
        # Valid move condition #1: the cell is empty.
        if self.board.get_cell(row, col) == 0:
            directions = [(0,1), (0,-1), (1,0), (-1,0), (1,1), (1,-1), (-1,1), (-1,-1)]
            cell = (row, col)
            for direction in directions:
                check_cell = (row + direction[0], col + direction[1])

                # Check to make sure the index is in range of our board.
                if max(check_cell) >= self.board.size:
                    continue

                # Valid move condition #2: there is an adjacent cell with the other player's disk.
                if self.board.mat[check_cell[0]][check_cell[1]] == self.opponent:

                    # Increment the current cell in that direction.
                    cell = (cell[0] + direction[0], cell[1] + direction[1])
                    
                    # Valid move condition #3: the given direction contains another one of current player's
                    # disks further down the row (i.e. there is a valid disk sandwich).
                    while self.board.mat[cell[0]][cell[1]] != player:

                        # If the next cell is 0 then the move is invalidated
                        if self.board.mat[cell[0]][cell[1]] == 0:
                            break
                        else:
                            cell = (cell[0] + direction[0], cell[1] + direction[1])

                    # When code reaches the end of the disk sandwich, it appends that direction to a list
                    if self.board.mat[cell[0]][cell[1]] == player:
                        true_directions.append(direction)    
                cell = (row, col)
        else:
            return self.is_valid

        # Need to confirm if any valid directions exist for placing a disk    
        if true_directions != []:
            self.board.update_board(row, col, true_directions, player)
            self.is_valid = True
        else:
            return self.is_valid


    