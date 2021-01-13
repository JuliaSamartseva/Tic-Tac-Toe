from game import Game
from validation import Validation
from player import Player
from enums import Level

while True:
    # parsing the command
    command = input("Input command: > ")

    # exit the loop if command is exit (stop the program)
    if command == "exit":
        break

    # repeat the loop if the command validation failed
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
