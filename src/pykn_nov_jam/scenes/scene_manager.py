import os
import os.path as path
import csv
import json

import pykraken as kn

from pykn_nov_jam.entities.entity import Entity
from pykn_nov_jam.entities.entity_manager import EntityManager
from pykn_nov_jam.entities.entity_prefabs import EntityPrefabs
from pykn_nov_jam.globals import Globals
from pykn_nov_jam.scenes.scene import Scene
from pykn_nov_jam.scenes.level_data import LevelData


class SceneManager:
    _instance: "SceneManager | None" = None

    def __init__(self, world_path: str) -> None:
        SceneManager._instance = self
        self.scenes: dict[str, str] = self.get_scenes(
            world_path
        )  # (Scene Name, Scene Path)
        self.current_scene: Scene | None = None

    def load_scene(self, scene_name: str) -> Scene:
        level_data = LevelLoader.load_level_data(self.scenes[scene_name])
        return Scene(level_data)

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

    def get_current_scene(self) -> Scene | None:
        return getattr(self, "current_scene", None)


class LevelLoader:
    @staticmethod
    def load_level_data(scene_path: str) -> "LevelData":
        entities = []  # List of Entity objects
        sprite_layers = {}  # Dictionary mapping layer index to kn.Texture

        print(f"Loading scene from path: {scene_path}")

        # load level data from JSON
        print("---")
        data_path = path.join(scene_path, "data.json")
        print(f"Loading level data from: {data_path}")

        with open(data_path) as json_file:
            data = json.load(json_file)

            print("---\n ENTITIES:")
            entity_list: dict = data["entities"]

        for entity_type, entity_instances in entity_list.items():
            for i, entity_data in enumerate(entity_instances):
                print("Entity index:", i)
                entity_id = entity_data["id"]
                pos_x = entity_data["x"] * 2
                pos_y = entity_data["y"] * 2
                sprite_width = entity_data["width"]
                sprite_height = entity_data["height"]
                if entity_id == "Player":
                    accel = entity_data["customFields"]["accel"]
                    decel = entity_data["customFields"]["decel"]
                    max_speed = entity_data["customFields"]["max_speed"]
                    position = kn.Vec2(pos_x, pos_y)
                    print(
                        f"Entity parameters:\n Position: {position}\n Accel: {accel}\n Decel: {decel}\n Max Speed: {max_speed}\n Sprite Width: {sprite_width}\n Sprite Height: {sprite_height}"
                    )
                    global_singleton = Globals._instance
                    if global_singleton is None:
                        raise Exception(
                            "Globals singleton instance is not initialized."
                        )
                    entity_instance = EntityPrefabs.create_player(
                        position, global_singleton, accel, decel, max_speed
                    )
                    entities.append(entity_instance)
                elif entity_id == "Sheep":
                    position = kn.Vec2(pos_x, pos_y)
                    entity_instance = EntityPrefabs.create_sheep(position, None, False)
                    entities.append(entity_instance)

            print("--- BACKGROUND LAYERS:")
            background_layers = data["layers"]
            for layer in background_layers:
                layer_index = background_layers.index(layer)
                layer_path = path.join(scene_path, layer)
                texture = kn.Texture(layer_path)
                sprite_layers[layer_index] = texture
                print(f"Loaded sprite layer {layer_index} from path: {layer_path}")
            print("---")

        # generate collision blocks from collision map
        collision_map_path = path.join(scene_path, "Collision.csv")
        print(f"Loading collision map from: {collision_map_path}")
        collision_map: list[list[int]] = LevelLoader.parse_collision_map(
            collision_map_path
        )

        collision_blocks = LevelLoader.generate_collision_blocks(collision_map)
        entities.extend(collision_blocks)
        print("---")
        print(f"Generated {len(collision_blocks)} collision blocks.")
        print(f"Entities count: {len(entities)}")
        print("---")

        # load entities, sprite layers, and collision map ...
        level_data = LevelData(entities, sprite_layers)
        print(
            f"Level data loaded with {len(level_data.entities)} entities and {len(level_data.sprite_layers)} sprite layers."
        )

        return level_data

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
                    position = kn.Vec2(x * 16, y * 16)
                    block = EntityPrefabs.create_collision_block(
                        position, kn.Rect(position, 16, 16)
                    )
                    collision_blocks.append(block)
                    # print(f"Created collision block at position: {position}")
        return collision_blocks
