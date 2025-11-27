import pykraken as kn

from pykn_nov_jam.components.component import Component
from pykn_nov_jam.entities.entity import Entity


class GrazeableComponent(Component):
    def __init__(self, entity: Entity, eating_radius: float):
        super().__init__(entity)
        self.max_eating_radius: float = eating_radius
        self.min_eating_radius: float = eating_radius * 0.8
        self.nutrition_value: float = 0.5
        self.nutrition_remaining: float = 100.0

    def deplete_nutrition(self, amount: float) -> None:
        self.nutrition_remaining = max(0.0, self.nutrition_remaining - amount)

    # def process_draw(self) -> None:
    #     kn.draw.circle(
    #         kn.Circle(self.entity.position, self.eating_radius),
    #         kn.Color(0, 255, 0, 100),
    #     )
