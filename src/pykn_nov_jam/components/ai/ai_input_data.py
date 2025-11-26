import pykraken as kn
from dataclasses import dataclass

from pykn_nov_jam.spatial_hash import SpatialHash


@dataclass
class AiInputData:
    def __init__(self):
        self.whistle: bool = False
        self.player_position: kn.Vec2 = kn.Vec2(0, 0)
        self.fear_level: float = 0.0
        self.attention_level: float = 0.0
        self.spatial_hash: SpatialHash | None = None
        self.delta_time: float = 0.0
