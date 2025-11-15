from pykn_nov_jam.scenes.scene import Scene


class SceneManager:
    def __init__(self) -> None:
        self.scenes: dict[str, "Scene"] = {}
        self.current_scene: Scene | None = None

    def add_scene(self, name, scene):
        self.scenes[name] = scene

    def set_scene(self, name):
        if name in self.scenes:
            self.current_scene = self.scenes[name]
        else:
            raise ValueError(f"Scene '{name}' does not exist.")

    def get_current_scene(self):
        return self.current_scene
