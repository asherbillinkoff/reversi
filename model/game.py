from re import X
from model.players import Player
from model.board import Board
from datetime import datetime

class Game():
    ''' This class handles all the logic for the game functions.'''
    def __init__(self, board_size):
        self.board = Board(board_size)
        self.curr_player = 1
        self.curr_name = Player.X
        self.is_valid = False

    def change_player(self):
        # Since the player numbers are 1 & 2, (3 - curr_player) will reliably givve us the value of
        # the next player.
        self.curr_player = 3 - self.curr_player
        self.curr_name = Player(self.curr_player).name

    def make_move(self, row, col):
        self.board.update_cell(row, col, self.curr_player)

    def sum_player_pts(self):
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
        # If there are any remaining cells in the matrix with a zero value then the game
        # has not yet concluded.
        for i in range(self.board.size):
            for j in range(self.board.size):
                if self.board.mat[i][j] == 0:
                    return False
                else:
                    pass
        return self.curr_player

    def record_winner(self, score, player):
        now = datetime.datetime
        with open('winner_records.txt', 'w') as f:
            print(now, player, score, file=f)

    def is_valid_move(self, row, col, player):
        # Create a list of all directions in which a valid move exists.
        true_directions = []
        
        # Valid move condition #1: the cell is empty.
        if self.board.get_cell(row, col) == 0:
            directions = [(0,1), (0,-1), (1,0), (-1,0), (1,1), (1,-1), (-1,1), (-1,-1)]
            self.curr_cell = (row, col)
            for direction in directions:
                if (row + direction[0]) <= self.board.size and (col + direction[1]) <= self.board.size:
                    self.curr_cell = (self.curr_cell[0] + direction[0], self.curr_cell[1] + direction[1])
                else:
                    break
                
                # Valid move condition #2: there is an adjacent cell with the other player's disk.
                if self.board.mat[self.curr_cell[0]][self.curr_cell[1]] == 3 - player:

                    # Increment the current cell in that direction.
                    self.curr_cell = (self.curr_cell[0] + direction[0], self.curr_cell[1] + direction[1])
                    
                    # Valid move condition #3: the given direction contains another one of current player's
                    # disks further down the row (i.e. there is a valid disk sandwich).
                    while self.board.mat[self.curr_cell[0]][self.curr_cell[1]] != player:

                        # If the next cell is 0 then the move is invalidated
                        if self.board.mat[self.curr_cell[0]][self.curr_cell[1]] == 0:
                            self.is_valid = False
                            break
                        else:
                            self.curr_cell = (self.curr_cell[0] + direction[0], self.curr_cell[1] + direction[1])

                    # When code reaches the end of the disk sandwich, it appends that direction to a list
                    if self.board.mat[self.curr_cell[0]][self.curr_cell[1]] == player:
                        true_directions.append(direction)    
                self.curr_cell = (row, col)
        else:
            return False

        # Need to confirm if any valid directions exist for placing a disk    
        if true_directions != []:
            self.board.update_board(row, col, true_directions, player)
            self.is_valid = True
        else:
            return self.is_valid


    