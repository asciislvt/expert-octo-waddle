import os.path as path
from pykn_nov_jam.scenes.scene import Scene


class SceneManager:
    _instance: "SceneManager | None" = None

    def __init__(self, world_path: str) -> None:
        SceneManager._instance = self
        self.scenes: dict[str, "Scene"] = {}
        self.world_path: str = world_path
        self.current_scene: Scene | None = None

    def get_levels(self, world_path: str) -> list[str]:
        if path.exists("world_path"):
            print("World path exists, getting levels...")
        else:
            print("World path does not exist.")

        return []
