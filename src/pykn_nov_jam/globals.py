from entity import Entity
from player_entity import PlayerEntity


class Globals:
    _instance: "Globals | None" = None
    player_entity: PlayerEntity | None = None

    def __init__(self) -> None:
        if Globals._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            Globals._instance = self
            print("Globals singleton instance created.")

    def set_player_entity(self, entity: PlayerEntity) -> None:
        self.player_entity = entity

    def get_player_entity(self) -> Entity | None:
        if Globals._instance is None:
            print("Globals instance is not initialized.")
            return None
        else:
            return Globals._instance.player_entity
