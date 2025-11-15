import pykraken as kn
from pykn_nov_jam.components.component import Component


class Entity:
    def __init__(
        self,
        position: kn.Vec2 = kn.Vec2(0, 0),
    ) -> None:
        self.position: kn.Vec2 = position
        self.component_collection: dict[type, Component] = {}

    def add_component(self, component: Component) -> None:
        self.component_collection.update({type(component): component})

    def has_component(self, component_type: type[Component]) -> bool:
        if component_type in self.component_collection.keys():
            return True

        for comp in self.component_collection.values():
            if isinstance(comp, component_type):
                return True

        return False

    def get_component(self, component_type: type[Component]) -> Component | None:
        if component_type in self.component_collection.keys():
            return self.component_collection.get(component_type)

        for comp in self.component_collection.values():
            if isinstance(comp, component_type):
                return comp

        return None
