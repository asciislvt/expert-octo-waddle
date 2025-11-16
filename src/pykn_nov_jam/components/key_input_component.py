from typing import override
import pykraken as kn
from pykn_nov_jam.entities.entity import Entity
from pykn_nov_jam.components.component import Component


class InputComponent(Component):
    def __init__(self, entity: Entity) -> None:
        super().__init__(entity)
        self.input_direction: kn.Vec2 = kn.Vec2(0, 0)

    @override
    def process_input(self) -> None:
        if self.enabled is False:
            return

        self.input_direction = kn.Vec2(0, 0)
        self.input_direction.y = kn.key.is_pressed(kn.K_s) - kn.key.is_pressed(kn.K_w)
        self.input_direction.x = kn.key.is_pressed(kn.K_d) - kn.key.is_pressed(kn.K_a)
        self.input_direction.normalize()
