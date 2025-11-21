from pykn_nov_jam.entities.entity import Entity


class Globals:
    _instance: "Globals | None" = None
    fear_level: float = 0.0
    player_entity: Entity | None = None
    player_is_whistling: bool = False

    def __init__(self) -> None:
        if Globals._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            Globals._instance = self
            print("Globals singleton instance created.")

    def set_player_entity(self, entity: Entity) -> None:
        self.player_entity = entity

    def get_player_entity(self) -> Entity | None:
        if Globals._instance is None:
            print("Globals instance is not initialized.")
            return None
        else:
            return Globals._instance.player_entity
