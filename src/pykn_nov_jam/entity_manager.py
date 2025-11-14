import collections
from entities.entity import Entity


class EntityManager:
    def __init__(self):
        self.entities = collections.deque()

    def input(self) -> None:
        for entity in self.entities:
            entity.input()

    def update(self, dt: float) -> None:
        for entity in self.entities:
            entity.update(dt)

    def draw(self) -> None:
        for entity in self.entities:
            entity.draw()

    def add_entity(self, entity: Entity) -> None:
        self.entities.append(entity)

    def remove_entity(self, entity: Entity) -> None:
        self.entities.remove(entity)
