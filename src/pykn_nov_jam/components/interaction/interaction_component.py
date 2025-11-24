import pykraken as kn
from pykn_nov_jam.components.component import Component
from pykn_nov_jam.entities.entity import Entity


class InteractionComponent(Component):
    def __init__(self, entity: Entity, interaction_range: float = 32.0) -> None:
        super().__init__(entity)
        self.interaction_range: float = interaction_range
