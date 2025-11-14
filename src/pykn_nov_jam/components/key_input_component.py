import pykraken as kn
from entities.entity import Entity
from components.component import Component


class KeyInputComponent(Component):
    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.input_direction: kn.Vec2 = kn.Vec2(0, 0)

    def process_input(self) -> None:
        self.input_direction = kn.Vec2(0, 0)
        self.input_direction.y = kn.key.is_pressed(kn.K_s) - kn.key.is_pressed(kn.K_w)
        self.input_direction.x = kn.key.is_pressed(kn.K_d) - kn.key.is_pressed(kn.K_a)
        self.input_direction.normalize()
