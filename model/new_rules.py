from model.board import Board

class NewRules:

    def __init__(self, row, col):
        self.row = row
        self.col = col
    
    def is_valid_move(self, row, col, player):
        # Create a list of a all directions in which a valid move exists
        true_directions = []
        
        # Condition to confirm if the cell is empty before placement
        if self.board.get_cell(row, col) != 0:
            directions = [(0,1), (0,-1), (1,0), (-1,0), (1,1), (1,-1), (-1,1), (-1,-1)]
            self.curr_cell = (self.row, self.col)
            for direction in directions:
                self.curr_cell = (self.curr_cell + direction[0], self.curr_cell + direction[1])
                
                # If the adjacent cell in the given direction is from the other player then the move is valid
                # and we should append that direction to the true_directions list
                if self.board.get_cell(row, col) != player:
                    true_directions.append(direction)
                else:
                    pass
            return true_directions
        else:
            return f'Move is invalid.'
    