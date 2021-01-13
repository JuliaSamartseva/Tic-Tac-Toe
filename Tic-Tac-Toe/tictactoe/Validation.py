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
        if first_player != "easy" and first_player != "medium" and first_player != "hard" and first_player != "user":
            return False
        if second_player != "easy" and second_player != "medium" and second_player != "hard" and second_player != "user":
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
