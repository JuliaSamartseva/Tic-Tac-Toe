from enum import Enum


class Level(Enum):
    CUSTOM = "user"
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class State(Enum):
    X_WIN = "X wins"
    O_WIN = "O wins"
    DRAW = "Draw"
    NOT_FINISHED = "Game not finished"
