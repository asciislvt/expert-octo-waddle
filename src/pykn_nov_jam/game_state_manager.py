from enum import Enum


class GameStates(Enum):
    MENU = 1
    DAY_PHASE = 2
    PREP_PHASE = 3
    NIGHT_PHASE = 4
    GAME_OVER = 5


class GameState:
    def __init__(self) -> None:
        pass
