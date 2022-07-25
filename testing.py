from view.board_console_view import BoardConsoleView
from view.board_view import BoardView
from model.board import Board

board = Board()

x = BoardConsoleView(board)

x.draw_board()