def is_valid_move(self, row, col, player):
        """ This method performs three main checks to confirm if a user move is
        valid. It iterates over all possible directions for disk validity and
        appends the valid directions to a list. This list is then passed to
        another class to update the status of the board after the move.

            Args:
                row (int): Cell value for a given row.
                col (int): Cell value for a given column.
                player (int enum): Player responsible for the current move.

            Returns:

        """
        
        # Create a list of all directions in which a valid move exists.
        true_directions = []
        is_valid = False
        
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
            return is_valid

        # Need to confirm if any valid directions exist for placing a disk    
        if true_directions != []:
            self.board.update_board(row, col, true_directions, player)
            is_valid = True
        return is_valid


        # RECURSIVE CODE

            #     directions = [(0,1), (0,-1), (1,0), (-1,0), (1,1), (1,-1), (-1,1), (-1,-1)]
    #     self.is_valid = False

    #     # 1. Check if the user move is within the board boundaries.
    #     if row >= self.board.size or col >= self.board.size:
    #         return self.is_valid

    #     # 2. Check if user move cell is empty.
    #     if self.board.get_cell(row, col) != 0:
    #         return self.is_valid

    #     # 3. Check if there are any neighbouring disks of the opponent. If True
    #     # recursive function is called.
    #     for direction in directions:
    #         check_cell = (row + direction[0], col + direction[1])
    #         if max(check_cell) >= self.board.size:
    #             pass
    #         elif self.board.mat[check_cell[0]][check_cell[1]] == self.opponent:
    #             self._flip_disks(row, col, direction, player)

    # def _flip_disks(self, row, col, direction, player):
    #     check_cell = (row + direction[0], col + direction[1])
    #     if self.board.get_cell(check_cell[0], check_cell[1]) == player:
    #         self.board.update_board(row, col, direction, player)
    #         self.is_valid = True
    #         return

    #     elif self.board.get_cell(check_cell[0], check_cell[1]) == self.opponent:
    #         row += direction[0]
    #         col += direction[1]
    #         self._flip_disks(row, col, direction, player)

    #     elif self.board.get_cell(check_cell[0], check_cell[1]) == False:
    #         return