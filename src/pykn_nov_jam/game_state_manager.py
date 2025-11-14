from enum import Enum


class GameStates(Enum):
    MENU = 1
    CUTSCENE = 2
    DAY_PHASE = 3
    PREP_PHASE = 4
    NIGHT_PHASE = 5
    SLEEP_PHASE = 6
    GAME_OVER = 7


class GameStateManager:
    _instance: "GameStateManager | None" = None

    def __init__(self) -> None:
        if GameStateManager._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            GameStateManager._instance = self
            print("GameStateManager singleton instance created.")

        self.current_state = GameStates.MENU
        self.day_count = 0
        self.is_game_over = False

    def handle_game_state(self) -> None:
        match self.current_state:
            case GameStates.MENU:
                print("GameStateManager: Current State - CUTSCENE")
            case GameStates.DAY_PHASE:
                print("GameStateManager: Current State - DAY PHASE")
            case GameStates.PREP_PHASE:
                print("GameStateManager: Current State - PREP PHASE")
            case GameStates.NIGHT_PHASE:
                print("GameStateManager: Current State - NIGHT PHASE")
            case GameStates.SLEEP_PHASE:
                print("GameStateManager: Current State - SLEEP PHASE")
            case GameStates.CUTSCENE:
                print("GameStateManager: Current State - CUTSCENE")
            case _:
                print("Unhandled game state: ", self.current_state)
