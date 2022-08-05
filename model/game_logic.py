from model.game import Game

class GameLogic:
    def __init__(self):
        self.is_valid = False
        self.game = Game(board_size=8)

    def make_move(self, row, col):
        """ Method pass along a user move to the board to be updated."""
        self.game.board.update_cell(row, col, self.curr_player)

    def is_valid_move(self, row, col, player):
            ''' Function determines if the user move is valid. If the
            three condition checks pass then the recursive function is called to
            flip opponent disks.'''

            # Create a list of all directions in which a valid move exists.
            true_directions = []
            self.is_valid = False
            
            # Valid move condition #1: the cell is empty.
            if board.get_cell(row, col) == 0:
                directions = [(0,1), (0,-1), (1,0), (-1,0), (1,1), (1,-1), (-1,1), (-1,-1)]
                cell = (row, col)
                for direction in directions:
                    check_cell = (row + direction[0], col + direction[1])

                    # Check to make sure the index is in range of our board.
                    if max(check_cell) >= self.game.board.size or min(check_cell) < 0:
                        continue

                    # Valid move condition #2: there is an adjacent cell with the
                    # other player's disk.
                    if self.game.board.mat[check_cell[0]][check_cell[1]] == self.game.opponent:

                        # Increment the current cell in that direction.
                        cell = (cell[0] + direction[0], cell[1] + direction[1])
                        if max(cell) >= self.game.board.size or min(cell) < 0:
                            continue

                        # Valid move condition #3: the given direction contains
                        # another one of current player's disks further down the
                        # row (i.e. there is a valid disk sandwich).
                        next_cell = cell
                        while self.game.board.mat[next_cell[0]][next_cell[1]] == self.game.opponent:
                            next_cell = (next_cell[0] + direction[0],
                                        next_cell[1] + direction[1])
                            # Make sure that the incremented cell is still within
                            # board range.
                            if max(next_cell) >= self.game.board.size or min(next_cell) < 0:
                                self.is_valid = False
                                break
                            # If incremented cell is = player then move is valid.
                            elif self.game.board.mat[next_cell[0]][next_cell[1]] == player:
                                self.is_valid = True
                                break
                                
                        # When code reaches the end of the disk sandwich, it
                        # appends that direction to a list
                        if self.is_valid:
                            true_directions.append(direction)    
                    cell = (row, col)
                    self.is_valid = False
            else:
                return

            # Need to confirm if any valid directions exist for placing a disk    
            if true_directions != []:
                self.game.board.update_board(row, col, true_directions, player)
                self.is_valid = True
            return

