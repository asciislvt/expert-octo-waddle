from typing import Callable
from pykn_nov_jam.components.component import Component
from pykn_nov_jam.entities.entity import Entity


class InteractableComponent(Component):
    def __init__(
        self, entity: Entity, on_interact: Callable[..., None] | None = None
    ) -> None:
        super().__init__(entity)
        self.on_interact: Callable[..., None] = (
            on_interact if on_interact else lambda e: None
        )

    def interact(self) -> None:
        self.on_interact(self.entity)
