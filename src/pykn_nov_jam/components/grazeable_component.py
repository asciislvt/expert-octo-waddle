from pykn_nov_jam.components.component import Component
from pykn_nov_jam.entities.entity import Entity


class GrazeableComponent(Component):
    def __init__(self, entity: Entity, eating_radius: float):
        super().__init__(entity)
        self.eating_radius: float = eating_radius
        self.nutrition_value: float = 20.0
