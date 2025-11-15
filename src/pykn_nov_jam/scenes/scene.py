from entities.entity import Entity


class Scene:
    def __init__(self, name: str = "New Scene") -> None:
        self.entities: list[Entity] = []
        self.name: str = name

    def process_input(self) -> None:
        for entity in self.entities:
            for component in entity.component_collection.values():
                component.process_input()

    def process_update(self, delta_time: float) -> None:
        for entity in self.entities:
            for component in entity.component_collection.values():
                component.process_update(delta_time)

    def process_draw(self) -> None:
        for entity in self.entities:
            for component in entity.component_collection.values():
                component.process_draw()
