import random
from pykn_nov_jam.components.component import Component
from pykn_nov_jam.components.inventory.player_inventory_component import (
    PlayerInventoryComponent,
)
from pykn_nov_jam.entities.entity import Entity


class RandomizedContainerComponent(Component):
    def __init__(self, entity: Entity) -> None:
        super().__init__(entity)
        self.possible_items: dict[str, float] = {
            "Scrap Metal": 0.5,
            "Wood Plank": 0.3,
            "Fastener": 0.2,
            "Rope": 0.2,
            "Gunpowder": 0.05,
        }
        self.uses: int = 3

    def is_empty(self) -> bool:
        if self.uses <= 0:
            return True
        return False

    def use_container(self) -> list[str]:
        if self.is_empty():
            print("The container is empty.")
            return []

        if self.uses > 0:
            found_items: list[str] = []
            for item, probability in self.possible_items.items():
                if random.randrange(0, 1) < probability:
                    found_items.append(item)

            self.uses -= 1
            print(f"Container used. Remaining uses: {self.uses}")
            return found_items
        print("The container is empty.")
        return []
