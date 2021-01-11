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
    def check_command_validity(command_name):
        # check exit
        if command_name == "exit":
            return True

        # check start
        try:
            name, first_player, second_player = command_name.split()
        except ValueError:
            print("Bad parameters!")
            return False

        if name != "start":
            return False
        if first_player != "easy" and first_player != "user":
            return False
        if second_player != "easy" and second_player != "user":
            return False
        return True

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


class Player:
    def __init__(self, option):
        # user or computer
        self.option = option

    def make_move(self, tictacgame):
        if self.option == "user":
            while True:
                coordinates = input("Enter the coordinates > ")
                if not Validation.check_move_validity(coordinates, tictacgame.matrix):
                    continue
                x, y = coordinates.split()
                x = int(x)
                y = int(y)
                tictacgame.make_move(x, y)
                tictacgame.output_board()
                break
        if self.option == "easy":
            tictacgame.make_computer_move()
            tictacgame.output_board()


while True:
    command = input("Input command: > ")

    if command == "exit":
        break
    if not Validation.check_command_validity(command):
        continue

    start, player_one_option, player_two_option = command.split()

    player_one = Player(player_one_option)
    player_two = Player(player_two_option)

    game = Game("_________", "easy")
    game.output_board()
    n_turns = 0
    # game running
    while True:
        if n_turns % 2 == 0:
            player_one.make_move(game)
        else:
            player_two.make_move(game)

        n_turns += 1
        if game.game_ended():
            print(game.state)
            print()
            break
