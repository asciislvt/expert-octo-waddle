import pykraken as kn
from dataclasses import dataclass


@dataclass
class AiInputData:
    def __init__(self):
        self.whistle: bool = False
        self.player_position: kn.Vec2 = kn.Vec2(0, 0)
        self.fear_level: float = 0.0
        self.attention_level: float = 0.0
