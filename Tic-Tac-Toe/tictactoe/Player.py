from enums import Level
from validation import Validation


class Player:
    def __init__(self, option, symbol):
        # user or computer
        self.option = option
        self.symbol = symbol

    def make_move(self, tictacgame):
        if self.option == Level.CUSTOM:
            while True:
                coordinates = input("Enter the coordinates > ")
                if not Validation.check_move_validity(coordinates, tictacgame.matrix):
                    continue
                x, y = coordinates.split()
                x = int(x)
                y = int(y)
                tictacgame.make_move(x - 1, y - 1)
                tictacgame.output()
                break
        elif self.option == Level.EASY or self.option == Level.MEDIUM or self.option == Level.HARD:
            tictacgame.make_computer_move(self.option, self)
            tictacgame.output()
