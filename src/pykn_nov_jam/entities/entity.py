import pykraken as kn
from components.component import Component


class Entity:
    def __init__(
        self,
        position: kn.Vec2 = kn.Vec2(0, 0),
    ) -> None:
        self.position: kn.Vec2 = position
        self.component_collection: dict[type, Component] = {}

    def add_component(self, component: Component) -> None:
        self.component_collection.update({type(component): component})

    def get_component(self, component_type: type[Component]) -> Component | None:
        if component_type in self.component_collection.keys():
            return self.component_collection.get(component_type)

        for comp in self.component_collection.values():
            if isinstance(comp, component_type):
                return comp

        return None
