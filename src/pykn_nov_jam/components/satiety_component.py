from pykn_nov_jam.components.component import Component
from pykn_nov_jam.entities.entity import Entity


class SatietyComponent(Component):
    def __init__(self, entity: Entity, initial_satiety: float = 100.0) -> None:
        super().__init__(entity)
        self.satiety: float = initial_satiety
        self.satiety_drained: float = 0.0
        self.max_satiety: float = 100.0
        self.drain_rate: float = 0.4  # per second
        self.recovery_rate: float = 0.8  # per second

    def process_update(self, delta_time: float) -> None:
        satiety_drain = self.drain_rate * delta_time
        self.satiety_drained += satiety_drain
        self.satiety = max(0.0, self.satiety - satiety_drain)
        # print(
        #     f"[SatietyComponent] Entity {self.entity} satiety drained by {satiety_drain:.2f}, new satiety: {self.satiety:.2f}"
        # )

    def recover_satiety(self, delta_time: float) -> None:
        satiety_recovery = self.recovery_rate * delta_time
        self.satiety_drained = 0.0
        self.satiety = min(self.max_satiety, self.satiety + satiety_recovery)
        print(f"Recovered satiety {satiety_recovery}")

    def is_hungry(self) -> bool:
        if self.satiety < (self.max_satiety * 0.92):
            print(
                f"[SatietyComponent] Entity {self.entity} is hungry (satiety: {self.satiety:.2f})"
            )
            return True
        return False
