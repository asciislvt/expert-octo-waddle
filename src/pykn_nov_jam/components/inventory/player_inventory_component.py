from pykn_nov_jam.components.component import Component
from pykn_nov_jam.entities.entity import Entity


class PlayerInventoryComponent(Component):
    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.items: dict[str, int] = {
            "Scrap Metal": 0,
            "Wood Plank": 0,
            "Fastener": 0,
            "Rope": 0,
            "Gunpowder": 0,
        }

    def add_item(self, item_name: str, quantity: int = 1) -> None:
        self.items[item_name] = self.items.get(item_name, 0) + quantity
        print(f"Added {quantity} x {item_name} to inventory.")
