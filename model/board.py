from model.players import Player

class Board():
    EMPTY_CELL = 0

    def __init__(self, size=8):
        self.size = size
        # Create a matrix of zeroes for the Reversi board
        self.mat = [[self.EMPTY_CELL] * size for _ in range(size)]
        self.mat[size // 2 - 1][size // 2 - 1] = Player.X
        self.mat[size // 2][size // 2] = Player.X
        self.mat[size // 2 - 1][size // 2] = Player.O
        self.mat[size // 2][size // 2 - 1] = Player.O

    def get_cell(self, row, col):
        # Returns the requested cell value to the game
        return self.mat[row][col]

    def update_cell(self, row, col, player):
        # Updates individual cell on the board from latest move
        self.mat[row][col] = player
        
    def update_board(self, row, col, directions, player):
        # Function to update all disks which need to be flipped based on last move
        for direction in directions:
            while self.mat[row + direction[0]][col + direction[1]] == (3 - player):
                self.mat[row + direction[0]][col + direction[1]] = player
                row += direction[0]
                col += direction[1]
        return True

