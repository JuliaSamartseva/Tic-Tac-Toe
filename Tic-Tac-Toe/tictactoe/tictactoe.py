import random
from enum import Enum


class Level(Enum):
    CUSTOM = "user"
    EASY = "easy"
    MEDIUM = "medium"


class State(Enum):
    X_WIN = "X wins"
    O_WIN = "O wins"
    DRAW = "Draw"
    NOT_FINISHED = "Game not finished"


class Game:
    def __init__(self, symbols_list):
        self.state = State.NOT_FINISHED
        self.matrix = []
        self.create_board(symbols_list)

    def output(self):
        print("---------")
        for i in range(3):
            print("|", end=" ")
            print(" ".join(self.matrix[i]), end=" ")
            print("|")
        print("---------")

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

    def get_random_coordinates(self):
        empty_cells = list()
        for i in range(3):
            for j in range(3):
                if self.matrix[i][j] == " ":
                    empty_cells.append((i, j))
        # choose random cell from those empty ones
        return random.choice(empty_cells)

    def make_computer_move(self, level, player):
        if level == Level.EASY:
            # find all empty cells
            move = self.get_random_coordinates()
            print('Making move level "easy"')
            self.make_move(move[0], move[1])
        elif level == Level.MEDIUM:
            move = self.get_smart_move_coordinates(player)
            print('Making move level "medium"')
            self.make_move(move[0], move[1])

    def get_smart_move_coordinates(self, player):
        for i in range(3):
            for j in range(3):
                if self.matrix[i][j] == " ":
                    # check placing player symbol
                    self.matrix[i][j] = player.symbol
                    new_game_state = self.get_game_state()
                    self.matrix[i][j] = " "
                    if new_game_state == State(player.symbol + " wins"):
                        return i, j
                    # check placing opponent symbol
                    opponent = "X" if player.symbol == "O" else "X"
                    self.matrix[i][j] = opponent
                    self.matrix[i][j] = " "
                    if new_game_state == State(opponent + " wins"):
                        return i, j

        return self.get_random_coordinates()

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

        self.matrix[x_coordinate][y_coordinate] = user_symbol
        self.state = self.get_game_state()

    def check_rows_win(self):
        for i in range(3):
            previous_symbol = self.matrix[i][0]
            winning_combination = True
            for j in range(3):
                if self.matrix[i][j] != previous_symbol:
                    winning_combination = False
                    break
            if winning_combination and previous_symbol != " ":
                return State(previous_symbol + " wins")
        return State.NOT_FINISHED

    def check_columns_win(self):
        for j in range(3):
            previous_symbol = self.matrix[0][j]
            winning_combination = True
            for i in range(3):
                if self.matrix[i][j] != previous_symbol:
                    winning_combination = False
                    break
            if winning_combination and previous_symbol != " ":
                return State(previous_symbol + " wins")
        return State.NOT_FINISHED

    def check_diagonal_win(self):
        previous_symbol = self.matrix[0][0]
        winning_combination = True
        for i in range(3):
            if self.matrix[i][i] != previous_symbol:
                winning_combination = False
                break
        if winning_combination and previous_symbol != " ":
            return State(previous_symbol + " wins")

        previous_symbol = self.matrix[0][2]
        winning_combination = True
        for i in range(3):
            if self.matrix[i][2 - i] != previous_symbol:
                winning_combination = False
                break
        if winning_combination and previous_symbol != " ":
            return State(previous_symbol + " wins")

        return State.NOT_FINISHED

    def check_draw(self):
        for i in range(3):
            for j in range(3):
                if self.matrix[i][j] == " ":
                    return State.NOT_FINISHED
        return State.DRAW

    def get_game_state(self):
        wins = [self.check_rows_win(), self.check_columns_win(), self.check_diagonal_win()]
        if all(win is State.NOT_FINISHED for win in wins):
            return self.check_draw()
        else:
            for win in wins:
                if win is not State.NOT_FINISHED:
                    return win

    def game_ended(self):
        if self.state == State.NOT_FINISHED:
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
        if first_player != "easy" and first_player != "medium" and first_player != "user":
            return False
        if second_player != "easy" and second_player != "medium" and second_player != "user":
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
        elif self.option == Level.EASY or self.option == Level.MEDIUM:
            tictacgame.make_computer_move(self.option, self)
            tictacgame.output()


while True:
    # parsing the command
    command = input("Input command: > ")

    if command == "exit":
        break
    if not Validation.check_command_validity(command):
        continue

    start, player_one_option, player_two_option = command.split()

    # creating players
    player_one = Player(Level(player_one_option), "X")
    player_two = Player(Level(player_two_option), "O")

    # creating the game
    game = Game("_________")
    game.output()
    n_turns = 0

    # game running
    while True:
        if n_turns % 2 == 0:
            player_one.make_move(game)
        else:
            player_two.make_move(game)

        n_turns += 1
        if game.game_ended():
            print(game.state.value)
            print()
            break
