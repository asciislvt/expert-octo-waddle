from entities.entity import Entity
from components.component import Component


class EntityManager:
    _instance: "EntityManager | None" = None

    def __init__(self):
        EntityManager._instance = self
        self.entities: list[Entity] = []

    def add_entity(self, entity: Entity) -> None:
        self.entities.append(entity)

    def remove_entity(self, entity: Entity) -> None:
        self.entities.remove(entity)

    def get_entities(self) -> list[Entity]:
        return self.entities

    def get_entities_with_component(
        self, component_type: type[Component]
    ) -> list[Entity]:
        result: list[Entity] = []

        for entity in self.entities:
            if component_type in entity.component_collection.keys():
                result.append(entity)

        return result
