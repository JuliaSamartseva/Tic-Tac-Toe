from enums import Level, State
import random


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
        elif level == Level.HARD:
            move = self.get_minimax_move_coordinates(player)
            print('Making move level "hard"')
            self.make_move(move[0], move[1])

    def get_minimax_move_coordinates(self, player):
        if player.symbol == "X":
            (m, qx, qy) = self.min_alpha_beta(-2, 2)
            return qx, qy
        else:
            (m, qx, qy) = self.max_alpha_beta(-2, 2)
            return qx, qy

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

    def max_alpha_beta(self, alpha, beta):
        maxv = -2
        px = None
        py = None

        result = self.get_game_state()

        if result == State.X_WIN:
            return -1, 0, 0
        elif result == State.O_WIN:
            return 1, 0, 0
        elif result == State.DRAW:
            return 0, 0, 0

        for i in range(0, 3):
            for j in range(0, 3):
                if self.matrix[i][j] == " ":
                    self.matrix[i][j] = "O"
                    (m, min_i, in_j) = self.min_alpha_beta(alpha, beta)
                    if m > maxv:
                        maxv = m
                        px = i
                        py = j
                    self.matrix[i][j] = " "

                    if maxv >= beta:
                        return maxv, px, py

                    if maxv > alpha:
                        alpha = maxv

        return maxv, px, py

    def min_alpha_beta(self, alpha, beta):
        minv = 2
        qx = None
        qy = None

        result = self.get_game_state()

        if result == State.X_WIN:
            return -1, 0, 0
        elif result == State.O_WIN:
            return 1, 0, 0
        elif result == State.DRAW:
            return 0, 0, 0

        for i in range(0, 3):
            for j in range(0, 3):
                if self.matrix[i][j] == " ":
                    self.matrix[i][j] = "X"
                    (m, max_i, max_j) = self.max_alpha_beta(alpha, beta)
                    if m < minv:
                        minv = m
                        qx = i
                        qy = j
                    self.matrix[i][j] = " "

                    if minv <= alpha:
                        return minv, qx, qy

                    if minv < beta:
                        beta = minv

        return minv, qx, qy
