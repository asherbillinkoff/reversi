from model.player import Player
import sys

class HumanPlayer(Player):
    def __init__(self, name, symbol=1, colour='Blue'):
        super().__init__(name, colour)
        self.name = name
        self.symbol = symbol


    def get_move_human(self):
        while True:
            try:
                s = input('Enter your move (row, col):').split(',')
                if s[0] == 'e':
                    sys.exit('\nReversi has been exited. Thanks for playing!')
                row, col = int(s[0]), int(s[1])
                break
            except ValueError:
                print('Please enter an integer.')
            except IndexError:
                print('Number is out of range.')
        return row, col