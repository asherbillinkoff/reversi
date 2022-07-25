class Board():
    EMPTY_CELL = 0

    def __init_(self, size):
        self.size = size

        # Create a matrix of zeroes for the Reversi board
        self.mat = [[self.EMPTY_CELL] * size for _ in range(size)]

    def get_cell(self, row, col):
        return self.mat[row][col]

    def update_cell(self, row, col, player):
        self.mat[row][col] = player
        
    # Function to update all disks which need to be flipped based on last move
    def update_board(self, row, col, directions, player):
        for direction in directions:
            for i in range