import pykraken as kn
from pykn_nov_jam.entities.entity import Entity
from dataclasses import dataclass


@dataclass
class LevelData:
    entities: list[Entity]
    sprite_layers: dict[int, kn.Texture]
