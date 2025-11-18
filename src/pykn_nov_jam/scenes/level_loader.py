class LevelLoader:
    _instance: "LevelLoader | None" = None

    def __init__(self):
        LevelLoader._instance = LevelLoader._instance

    def load_level(self, level_path: str) -> None:
        pass
