import os
import os.path as path
import csv
from dataclasses import dataclass

import pykraken as kn

from pykn_nov_jam.entities.entity import Entity
from pykn_nov_jam.entities.entity_manager import EntityManager
from pykn_nov_jam.entities.entity_prefabs import EntityPrefabs
from pykn_nov_jam.scenes.scene import Scene


class SceneManager:
    _instance: "SceneManager | None" = None

    def __init__(self, world_path: str) -> None:
        SceneManager._instance = self
        self.scenes: dict[str, str] = self.get_scenes(
            world_path
        )  # (Scene Name, Scene Path)
        self.current_scene: Scene | None = None

    def load_scene(self, scene_name: str) -> None:
        scene_data = LevelLoader.load_level_data(self.scenes[scene_name])
        for entity in scene_data.entities:
            if EntityManager._instance is not None:
                print(f"Adding entity to EntityManager: {entity}")
                EntityManager._instance.add_entity(entity)

    def get_scenes(self, world_path: str) -> dict[str, str]:
        if path.exists(world_path):
            print("World path exists, getting scenes...")
            scene_path = path.join(world_path, "simplified")
            print(f"Checking for scenes in path: {scene_path}")
            if path.exists(scene_path):
                print("Levels exist, listing scenes...")
                scenes = os.listdir(scene_path)
                scene_paths = {}
                print("---")
                for scene in scenes:
                    path_string = f"{scene_path}/{scene}"
                    scene_paths[scene] = path_string
                    print(f"Found scenes | scene_paths[{scene}] = {path_string}")
                print("---")

                return scene_paths
        else:
            print("World path does not exist, returning empty dictionary.")

        return {}


class LevelLoader:
    @staticmethod
    def load_level_data(scene_path: str) -> "LevelData":
        # This function will parse the scene file and create entities, sprite layers, and collision map
        entities = []  # List of Entity objects
        sprite_layers = {}  # Dictionary mapping layer index to kn.Texture

        # Example loading logic (to be replaced with actual implementation)
        print(f"Loading scene from path: {scene_path}")

        collision_map_path = path.join(scene_path, "Collision.csv")
        collision_map: list[list[int]] = LevelLoader.parse_collision_map(
            collision_map_path
        )

        collision_blocks = LevelLoader.generate_collision_blocks(collision_map)
        entities.extend(collision_blocks)
        print("---")
        print(f"Generated {len(collision_blocks)} collision blocks.")
        print(f"Entities count: {len(entities)}")
        print("---")

        # ... load entities, sprite layers, and collision map ...
        data = LevelData(entities, sprite_layers)
        print(
            f"Level data loaded with {len(data.entities)} entities and {len(data.sprite_layers)} sprite layers."
        )

        return data

    @staticmethod
    def parse_collision_map(collision_map_path: str) -> list[list[int]]:
        collision_map = []
        with open(collision_map_path, newline="") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                # print(f"Parsing collision map row: {row}")
                collision_map.append(row)

        return collision_map

    @staticmethod
    def generate_collision_blocks(collision_map: list[list[int]]) -> list[Entity]:
        collision_blocks = []
        for y in range(len(collision_map)):
            for x in range(len(collision_map[y])):
                tile_value = collision_map[y][x]
                if tile_value == "1":
                    position = kn.Vec2(x * 16, y * 16)  # Assuming each tile is 16x16
                    block = EntityPrefabs.create_static_object(position, 16, 16)
                    collision_blocks.append(block)
                    # print(f"Created collision block at position: {position}")
        return collision_blocks


@dataclass
class LevelData:
    entities: list[Entity]
    sprite_layers: dict[int, kn.Texture]
