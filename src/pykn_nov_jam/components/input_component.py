import pykraken as kn

from pykn_nov_jam.components.component import Component
from pykn_nov_jam.entities.entity import Entity


class InputComponent(Component):
    def __init__(self, entity: Entity) -> None:
        super().__init__(entity)
        self.input_direction: kn.Vec2 = kn.Vec2(0, 0)

    def process_input(self) -> None:
        pass
