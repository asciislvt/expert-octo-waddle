import pykraken as kn
from pykn_nov_jam.components.ai.ai_steering_component import AiSteeringComponent
from pykn_nov_jam.components.component import Component
from pykn_nov_jam.entities.entity import Entity


class AiBrainComponent(Component):
    def __init__(self, entity: Entity) -> None:
        super().__init__(entity)
        self.steering: AiSteeringComponent = entity.get_component(AiSteeringComponent)  # type: ignore

    def process_update(self, delta_time: float) -> None:
        if self.enabled is False:
            return

        # Example AI logic: Wander around
        wander_radius = 50.0
        steering_vector = self.steering.wander(wander_radius)
        self.steering.input_direction = steering_vector
