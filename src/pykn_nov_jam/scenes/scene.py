from pykn_nov_jam.entities.entity_manager import EntityManager
from pykn_nov_jam.scenes.scene_manager import LevelData


class Scene:
    def __init__(self, level_data: LevelData) -> None:
        entity_manager = EntityManager()
        pass

    def process_scene(self, delta_time: float) -> None:
        pass
