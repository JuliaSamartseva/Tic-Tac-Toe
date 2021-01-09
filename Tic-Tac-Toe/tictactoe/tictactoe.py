import random


class Game:

    def __init__(self, symbols_list, level):
        self.state = "Game not finished"
        self.matrix = []
        self.create_board(symbols_list)
        self.level = level

    def create_board(self, symbols_list):
        symbols_list_iterator = 0
        for i in range(3):
            self.matrix.append([])
            for j in range(3):
                symbol = symbols_list[symbols_list_iterator]
                symbols_list_iterator += 1
                if symbol == "_":
                    self.matrix[i].append(" ")
                else:
                    self.matrix[i].append(symbol)

    def output_board(self):
        print("---------")
        for i in range(3):
            print("|", end=" ")
            print(" ".join(self.matrix[i]), end=" ")
            print("|")
        print("---------")

    def make_computer_move(self):
        if self.level == "easy":
            # find all empty cells
            empty_cells = list()
            for i in range(3):
                for j in range(3):
                    if self.matrix[i][j] == " ":
                        empty_cells.append(str(i) + " " + str(j))
            move = random.choice(empty_cells)
            x_coordinate, y_coordinate = move.split()
            x_coordinate = int(x_coordinate)
            y_coordinate = int(y_coordinate)
            print('Making move level "easy"')
            self.make_move(x_coordinate + 1, y_coordinate + 1)

    def make_move(self, x_coordinate, y_coordinate):
        o_number = 0
        x_number = 0
        for i in range(3):
            for j in range(3):
                if self.matrix[i][j] == 'X':
                    x_number += 1
                elif self.matrix[i][j] == 'O':
                    o_number += 1
        if x_number == o_number:
            user_symbol = "X"
        else:
            user_symbol = "O"

        self.matrix[x_coordinate - 1][y_coordinate - 1] = user_symbol
        self.update_game_state()

    def check_rows_win(self):
        for i in range(3):
            previous_symbol = self.matrix[i][0]
            winning_combination = True
            for j in range(3):
                if self.matrix[i][j] != previous_symbol:
                    winning_combination = False
                    break
            if winning_combination and previous_symbol != " ":
                self.state = previous_symbol + " wins"
                return True
        return False

    def check_columns_win(self):
        for j in range(3):
            previous_symbol = self.matrix[0][j]
            winning_combination = True
            for i in range(3):
                if self.matrix[i][j] != previous_symbol:
                    winning_combination = False
                    break
            if winning_combination and previous_symbol != " ":
                self.state = previous_symbol + " wins"
                return True
        return False

    def check_diagonal_win(self):
        previous_symbol = self.matrix[0][0]
        winning_combination = True
        for i in range(3):
            if self.matrix[i][i] != previous_symbol:
                winning_combination = False
                break
        if winning_combination and previous_symbol != " ":
            self.state = previous_symbol + " wins"
            return True

        previous_symbol = self.matrix[0][2]
        winning_combination = True
        for i in range(3):
            if self.matrix[i][2 - i] != previous_symbol:
                winning_combination = False
                break
        if winning_combination and previous_symbol != " ":
            self.state = previous_symbol + " wins"
            return True

        return False

    def check_draw(self):
        for i in range(3):
            for j in range(3):
                if self.matrix[i][j] == " ":
                    return False
        self.state = "Draw"
        return True

    def update_game_state(self):
        if not self.check_rows_win() and not self.check_columns_win() and not self.check_diagonal_win():
            self.check_draw()

    def game_ended(self):
        if self.state == "Game not finished":
            return False
        return True


class Validation:

    @staticmethod
    def check_board_validity(symbols_list):
        if len(symbols_list) != 9:
            return False
        allowed_symbols = "XO_"
        for i in symbols_list:
            if i not in allowed_symbols:
                return False
        return True

    @staticmethod
    def check_move_validity(move, board):
        try:
            x_coordinate, y_coordinate = move.split()
            x_coordinate = int(x_coordinate)
            y_coordinate = int(y_coordinate)
        except ValueError:
            print("You should enter numbers!")
            return False

        if x_coordinate < 1 or x_coordinate > 3 or y_coordinate < 1 or y_coordinate > 3:
            print("Coordinates should be from 1 to 3!")
            return False

        if board[x_coordinate - 1][y_coordinate - 1] != " ":
            print("This cell is occupied! Choose another one!")
            return False

        return True


game = Game("_________", "easy")
game.output_board()

while True:
    coordinates = input("Enter the coordinates > ")
    if not Validation.check_move_validity(coordinates, game.matrix):
        continue
    x, y = coordinates.split()
    x = int(x)
    y = int(y)
    game.make_move(x, y)
    game.output_board()
    if game.game_ended():
        print(game.state)
        break
    game.make_computer_move()
    game.output_board()
    if game.game_ended():
        print(game.state)
        break
